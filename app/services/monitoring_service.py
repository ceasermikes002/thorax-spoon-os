import os
import time
import asyncio
import requests
from typing import Any, Dict, List, Tuple

from .storage import list_contracts, record_event
from .breach_service import analyze_event_with_llm
from .email_service import EmailService
from app.utils.logging import get_logger
from app.utils.metrics import inc
from .tts_service import synthesize
from app.utils.log_stream import emit as emit_log


logger = get_logger("monitoring_service")


def _rpc_call(rpc_url: str, method: str, params: List[Any]) -> Dict[str, Any]:
    body = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    for attempt in range(2):
        try:
            resp = requests.post(rpc_url, json=body, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            logger.debug(f"rpc_status={resp.status_code} method={method}")
        except Exception as e:
            logger.debug(f"rpc_error method={method} err={e}")
        time.sleep(0.2)
    return {}


def _normalize_hash(h: str) -> str:
    return (h or "").lower().replace("0x", "")


def _reverse_hex(hex_str: str) -> str:
    pairs = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    return "".join(reversed(pairs))


async def _scan_once(rpc_url: str, last_block_seen: Dict[str, int]) -> Tuple[int, int]:
    events_recorded = 0
    scanned_blocks = 0
    mailer = EmailService()

    contracts = [c for c in await list_contracts() if c.get("active")]
    if not contracts:
        return scanned_blocks, events_recorded

    bc = _rpc_call(rpc_url, "getblockcount", [])
    height = int((bc.get("result") or 0))
    scan_back = int(os.getenv("MONITOR_SCAN_BACK_BLOCKS", "2000"))

    for c in contracts:
        chash_norm = _normalize_hash(str(c["contract_hash"]))
        start = last_block_seen.get(chash_norm, max(0, height - scan_back))
        if start < 0:
            start = 0
        for idx in range(start, max(start, height)):
            blk = _rpc_call(rpc_url, "getblock", [idx, 1])
            result = blk.get("result") or {}
            txs = result.get("tx") or []
            scanned_blocks += 1
            for t in txs:
                txid = t.get("hash")
                if not txid:
                    continue
                app_log = _rpc_call(rpc_url, "getapplicationlog", [txid])
                executions = (app_log.get("result") or {}).get("executions") or []
                for ex in executions:
                    notifs = ex.get("notifications") or []
                    for n in notifs:
                        contract_field = str(n.get("contract") or "").lower()
                        event_name = n.get("eventname") or ""
                        if not event_name:
                            continue
                        notif_norm = _normalize_hash(contract_field)
                        governance_names = {"upgrade", "upgradeto", "proposalcreated", "proposalexecuted", "contractupdated"}
                        governance_hit = any(g in (event_name or "").lower() for g in governance_names)
                        if notif_norm == chash_norm or notif_norm == _reverse_hex(chash_norm) or governance_hit:
                            if c.get("monitoring_events") and event_name not in c["monitoring_events"]:
                                if not governance_hit:
                                    continue
                            payload = {
                                "event_name": event_name,
                                "txid": txid,
                                "block": idx,
                                "notification": n,
                            }
                            if governance_hit:
                                payload["governance"] = True
                            decision = analyze_event_with_llm(payload, c)
                            rec = await record_event(
                                c["id"],
                                event_name,
                                int(time.time()),
                                payload,
                                decision.get("severity"),
                                bool(decision.get("breach_detected")),
                                decision.get("recommended_action"),
                            )
                            events_recorded += 1
                            inc("events_recorded")
                            try:
                                emit_log({
                                    "type": "event",
                                    "network": str(c.get("network") or "testnet"),
                                    "contract_id": c["id"],
                                    "event_name": event_name,
                                    "severity": decision.get("severity"),
                                    "breach_detected": bool(decision.get("breach_detected")),
                                    "txid": txid,
                                    "block": idx,
                                })
                            except Exception:
                                pass
                            if decision.get("breach_detected"):
                                inc("breaches_detected")
                                subject = f"AOL Alert: {c.get('contract_name') or c['contract_hash']} - {event_name}"
                                body = (
                                    f"Breach detected on contract {c['contract_hash']}\n"
                                    f"Event: {event_name}\n"
                                    f"Severity: {decision.get('severity')}\n"
                                    f"Reason: {decision.get('reason')}\n"
                                    f"Recommended Action: {decision.get('recommended_action')}\n"
                                )
                                audio_text = (
                                    f"Alert. Contract {c.get('contract_name') or c['contract_hash']} emitted {event_name}. "
                                    f"Severity {decision.get('severity')}. {decision.get('reason')}. "
                                    f"Recommended action: {decision.get('recommended_action')}"
                                )
                                audio_path = synthesize(audio_text)
                                if audio_path:
                                    body += f"\nVoice explanation saved: {audio_path}\n"
                                mailer.send(c["owner_email"], subject, body)
        last_block_seen[chash_norm] = height

    return scanned_blocks, events_recorded


async def monitor_loop():
    interval = int(os.getenv("MONITOR_INTERVAL_SECONDS", "30"))
    rpc_default = os.getenv("NEO_RPC_URL", "https://mainnet1.neo.coz.io:443")
    rpc_testnet = os.getenv("NEO_RPC_URL_TESTNET", rpc_default)
    rpc_mainnet = os.getenv("NEO_RPC_URL_MAINNET", rpc_default)
    last_seen_by_network: Dict[str, Dict[str, int]] = {"testnet": {}, "mainnet": {}}
    while True:
        try:
            contracts = [c for c in await list_contracts() if c.get("active") and (c.get("chain") or "neo") == "neo"]
            groups: Dict[str, List[Dict[str, Any]]] = {"testnet": [], "mainnet": []}
            for c in contracts:
                net = str(c.get("network") or "testnet").lower()
                if net not in groups:
                    groups[net] = []
                    if net not in last_seen_by_network:
                        last_seen_by_network[net] = {}
                groups[net].append(c)
            for net, group in groups.items():
                if not group:
                    continue
                rpc_url = rpc_testnet if net == "testnet" else rpc_mainnet
                # Temporarily scan all contracts via shared RPC; _scan_once pulls contracts itself
                await _scan_once(rpc_url, last_seen_by_network.get(net, {}))
        except Exception:
            pass
        await asyncio.sleep(interval)


async def monitor_once() -> Dict[str, int]:
    rpc_default = os.getenv("NEO_RPC_URL", "https://mainnet1.neo.coz.io:443")
    rpc_testnet = os.getenv("NEO_RPC_URL_TESTNET", rpc_default)
    rpc_mainnet = os.getenv("NEO_RPC_URL_MAINNET", rpc_default)
    scanned_total = 0
    recorded_total = 0
    for rpc_url in (rpc_testnet, rpc_mainnet):
        try:
            scanned, recorded = await _scan_once(rpc_url, {})
            scanned_total += scanned
            recorded_total += recorded
        except Exception:
            pass
    return {"scanned_blocks": scanned_total, "events_recorded": recorded_total}


def start_monitoring_background():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.create_task(monitor_loop())

import os
import time
import asyncio
from typing import Any, Dict, List

import requests
from .storage import list_contracts, record_event
from .breach_service import analyze_event_with_llm
from .email_service import EmailService


def _rpc(provider: str, method: str, params: List[Any]) -> Dict[str, Any]:
    try:
        resp = requests.post(provider, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=15)
        return resp.json()
    except Exception:
        return {}


def _hex_to_int(h: Any) -> int:
    if isinstance(h, int):
        return h
    try:
        return int(str(h), 16)
    except Exception:
        return 0


def _int_to_hex(n: int) -> str:
    return hex(n)


async def evm_monitor_loop():
    provider = os.getenv("WEB3_PROVIDER_URL")
    if not provider:
        return
    last_seen: Dict[str, int] = {}
    interval = int(os.getenv("EVM_MONITOR_INTERVAL_SECONDS", os.getenv("MONITOR_INTERVAL_SECONDS", "30")))
    scan_back = int(os.getenv("EVM_SCAN_BACK_BLOCKS", "100"))
    mailer = EmailService()
    while True:
        try:
            latest_hex = _rpc(provider, "eth_blockNumber", [])
            latest = _hex_to_int(latest_hex.get("result"))
            contracts = [c for c in await list_contracts() if c.get("active") and (c.get("chain") or "neo") == "evm" and c.get("contract_hash")]
            for c in contracts:
                addr = (c.get("contract_hash") or "").lower()
                start = last_seen.get(addr, max(0, latest - scan_back))
                if start < 0:
                    start = 0
                logs_resp = _rpc(provider, "eth_getLogs", [{"fromBlock": _int_to_hex(start), "toBlock": _int_to_hex(latest), "address": addr}])
                logs: List[Dict[str, Any]] = logs_resp.get("result") or []
                for log in logs:
                    blk_num = _hex_to_int(log.get("blockNumber"))
                    block_resp = _rpc(provider, "eth_getBlockByNumber", [log.get("blockNumber"), False])
                    blk = block_resp.get("result") or {}
                    ts = _hex_to_int(blk.get("timestamp")) or int(time.time())
                    txh = log.get("transactionHash") or ""
                    payload = {
                        "event_name": "Log",
                        "address": addr,
                        "block": blk_num,
                        "txid": txh,
                        "topics": [t for t in (log.get("topics") or [])],
                        "data": log.get("data", ""),
                    }
                    decision = analyze_event_with_llm(payload, c)
                    await record_event(
                        c["id"],
                        payload["event_name"],
                        ts,
                        payload | {"ai_message": decision.get("ai_message")},
                        decision.get("severity"),
                        bool(decision.get("breach_detected")),
                        decision.get("recommended_action"),
                    )
                    if decision.get("breach_detected"):
                        subject = f"AOL Alert: {c.get('contract_name') or c['contract_hash']} - {payload['event_name']}"
                        body = (
                            f"Breach detected on contract {c['contract_hash']}\n"
                            f"Event: {payload['event_name']}\n"
                            f"Severity: {decision.get('severity')}\n"
                            f"Reason: {decision.get('reason')}\n"
                            f"Recommended Action: {decision.get('recommended_action')}\n"
                        )
                        mailer.send(c["owner_email"], subject, body)
                last_seen[addr] = latest
        except Exception:
            pass
        await asyncio.sleep(interval)


def start_evm_monitoring_background():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.create_task(evm_monitor_loop())

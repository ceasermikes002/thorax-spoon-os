import json
from typing import Any, Dict, List


def _calculate_risk_from_abi(abi: Dict[str, Any]) -> int:
    risk = 0
    privileged = ["mint", "pause", "freeze", "burn", "setowner", "destroy", "upgrade", "upgradeto", "setimplementation"]
    methods = [m.get("name", "").lower() for m in (abi.get("methods") or [])]
    for name in methods:
        if any(p in name for p in privileged):
            risk += 2
    admin_events = ["ownershiptransferred", "paused", "adminchanged", "contractupdated"]
    events = [e.get("name", "").lower() for e in (abi.get("events") or [])]
    for en in events:
        if any(a in en for a in admin_events):
            risk += 1
    risk += 1
    return min(risk, 10)


def _identify_vectors_from_abi(abi: Dict[str, Any]) -> List[str]:
    methods = [m.get("name", "").lower() for m in (abi.get("methods") or [])]
    vectors: List[str] = []
    if any("mint" in n for n in methods):
        vectors.append("unlimited_minting")
    if any("pause" in n for n in methods):
        vectors.append("contract_pause")
    if any("freeze" in n for n in methods):
        vectors.append("address_freezing")
    if any("transfer" in n and "owner" in n for n in methods):
        vectors.append("ownership_takeover")
    if any("destroy" in n or "kill" in n for n in methods):
        vectors.append("contract_destruction")
    if any("upgrade" in n or "upgradeto" in n or "setimplementation" in n for n in methods):
        vectors.append("unchecked_upgrade_risk")
    return vectors if vectors else ["standard_contract_risks"]


def _format_report_abi(abi: Dict[str, Any], risk_level: int, breach_vectors: List[str]) -> str:
    methods_list = "\n".join(
        f"  • {m.get('name','unknown')}({', '.join([p.get('name','') for p in (m.get('parameters') or [])])})"
        for m in (abi.get("methods") or [])
    ) or "  • No public methods"
    events_list = "\n".join(
        f"  • {e.get('name','unknown')}({', '.join([p.get('name','') for p in (e.get('parameters') or [])])})"
        for e in (abi.get("events") or [])
    ) or "  • No events defined"
    breach_list = "\n".join(f"  • {v.replace('_',' ').title()}" for v in breach_vectors)
    risk_emoji = "🔴" if risk_level >= 7 else "🟡" if risk_level >= 4 else "🟢"
    risk_text = "HIGH RISK" if risk_level >= 7 else "MEDIUM RISK" if risk_level >= 4 else "LOW RISK"
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 AOL CONTRACT ABI ANALYSIS (NEO)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{risk_emoji} Risk Level: {risk_level}/10 - {risk_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ METHODS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{methods_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 EVENTS TO MONITOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{events_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 POTENTIAL BREACH VECTORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{breach_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def analyze_neo_abi(abi: Dict[str, Any]) -> Dict[str, Any]:
    risk = _calculate_risk_from_abi(abi)
    vectors = _identify_vectors_from_abi(abi)
    report = _format_report_abi(abi, risk, vectors)
    monitoring_events = [e.get("name", "") for e in (abi.get("events") or [])]
    return {
        "risk_level": risk,
        "breach_vectors": vectors,
        "monitoring_events": monitoring_events,
        "formatted_report": report,
    }


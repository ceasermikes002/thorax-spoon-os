import os
import json
import requests
from typing import Any, Dict, List, Optional
from app.utils.logging import get_logger


logger = get_logger("legal_service")


def _spoon_llm(prompt: str) -> str | None:
    try:
        from spoon_ai.chat import ChatBot
        provider = os.getenv("SPOON_LLM_PROVIDER", os.getenv("DEFAULT_LLM_PROVIDER", "google"))
        model = os.getenv("SPOON_MODEL", os.getenv("DEFAULT_MODEL", "gemini-2.5-pro"))
        bot = ChatBot(model_name=model, llm_provider=provider)
        return bot.run(prompt)
    except Exception:
        return None


def _gemini_llm(prompt: str) -> str | None:
    provider = os.getenv("DEFAULT_LLM_PROVIDER", "gemini").lower()
    model = os.getenv("DEFAULT_MODEL", "gemini-2.5-pro")
    api_key = os.getenv("GOOGLE_API_KEY")
    if provider != "gemini" or not api_key:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
    try:
        resp = requests.post(url, json=body, timeout=20)
        if resp.status_code != 200:
            return None
        data = resp.json()
        candidates = (data.get("candidates") or [])
        if candidates:
            parts = (candidates[0].get("content", {}).get("parts") or [])
            if parts and parts[0].get("text"):
                return parts[0]["text"]
        return None
    except Exception:
        return None


def _heuristics(abi: Dict[str, Any], source: Optional[str]) -> List[str]:
    flags: List[str] = []
    methods = [m.get("name", "").lower() for m in (abi.get("methods") or [])]
    check_names = [
        "rescuefunds",
        "withdrawall",
        "emergencywithdraw",
        "setadmin",
        "upgrade",
        "upgradeto",
        "setimplementation",
        "pause",
        "transferownership",
    ]
    for name in methods:
        for needle in check_names:
            if needle in name:
                flags.append(f"method:{name}")
    if source:
        lowered = source.lower()
        keywords = ["rescuefunds", "rug", "seize", "emergencywithdraw", "upgradeto", "proxy", "timelock"]
        for k in keywords:
            if k in lowered:
                flags.append(f"source:{k}")
    return list(set(flags))


def analyze_legal(abi: Dict[str, Any], source: Optional[str] = None) -> Dict[str, Any]:
    flags = _heuristics(abi, source)
    prompt = (
        "You are a contract lawyer agent. Detect legal unfairness in an RWA token smart contract. "
        "Given ABI and optional source hints, identify clauses enabling admin asset seizure, unrestricted upgrades, or pause-without-timelock. "
        "Return JSON with keys: unfair (bool), severity (low/medium/high/critical), reasons (array of strings), recommendation (string).\n\n"
        f"ABI: {json.dumps(abi, ensure_ascii=False)}\n"
        f"Flags: {json.dumps(flags, ensure_ascii=False)}\n"
        f"SourceHints: {json.dumps(source or '', ensure_ascii=False)}\n"
    )
    text = _spoon_llm(prompt) or _gemini_llm(prompt)
    result = None
    if isinstance(text, str):
        try:
            result = json.loads(text)
        except Exception:
            result = None
    if not result or not isinstance(result, dict):
        severity = "low"
        if any("rescuefunds" in f or "withdrawall" in f or "upgradeto" in f for f in flags):
            severity = "high"
        return {
            "unfair": bool(flags),
            "severity": severity,
            "reasons": flags,
            "recommendation": "Avoid or require timelock and DAO approval",
        }
    return {
        "unfair": bool(result.get("unfair")),
        "severity": str(result.get("severity") or "low"),
        "reasons": list(result.get("reasons") or flags),
        "recommendation": str(result.get("recommendation") or ""),
    }


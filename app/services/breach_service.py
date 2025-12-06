import os
import json
import time
import requests
from typing import Any, Dict
from app.utils.logging import get_logger
from app.utils.metrics import inc


def _heuristic_reason(event: Dict[str, Any]) -> Dict[str, Any]:
    name = (event.get("event_name") or event.get("event") or "").lower()
    breach = False
    severity = "low"
    reason = "Routine event"
    action = "Monitor"
    if "ownership" in name and "transfer" in name:
        breach = True
        severity = "critical"
        reason = "Ownership transferred; potential takeover risk."
        action = "Pause contract and verify owner keys."
    elif "pause" in name:
        breach = True
        severity = "high"
        reason = "Contract paused unexpectedly."
        action = "Investigate caller; restore operations if safe."
    elif "mint" in name:
        breach = True
        severity = "medium"
        reason = "Mint operation detected; check limits and roles."
        action = "Audit recent mints and role assignments."
    return {
        "breach_detected": breach,
        "severity": severity,
        "reason": reason,
        "recommended_action": action,
    }


logger = get_logger("breach_service")


def _spoon_llm(prompt: str) -> str | None:
    try:
        from spoon_ai.chat import ChatBot
        provider = os.getenv("SPOON_LLM_PROVIDER", os.getenv("DEFAULT_LLM_PROVIDER", "google"))
        model = os.getenv("SPOON_MODEL", os.getenv("DEFAULT_MODEL", "gemini-2.5-pro"))
        bot = ChatBot(model_name=model, llm_provider=provider)
        return bot.run(prompt)
    except Exception as e:
        logger.debug(f"spoon_llm_unavailable: {e}")
        return None


def _gemini_llm(prompt: str) -> str | None:
    provider = os.getenv("DEFAULT_LLM_PROVIDER", "gemini").lower()
    model = os.getenv("DEFAULT_MODEL", "gemini-2.5-pro")
    max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "20000"))
    if provider != "gemini":
        return None
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.2},
    }
    try:
        resp = requests.post(url, json=body, timeout=20)
        if resp.status_code != 200:
            logger.debug(f"gemini_http_status={resp.status_code}")
            return None
        data = resp.json()
        candidates = (data.get("candidates") or [])
        if candidates:
            parts = (candidates[0].get("content", {}).get("parts") or [])
            if parts and parts[0].get("text"):
                return parts[0]["text"]
        return None
    except Exception as e:
        logger.debug(f"gemini_http_error: {e}")
        return None


def analyze_event_with_llm(event: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
    prompt = (
        "You are a breach-detection agent for Neo smart contracts. "
        "Given the contract metadata and a single emitted event, decide if it indicates a malicious or risky action. "
        "Return a JSON with keys: breach_detected (bool), severity (low/medium/high/critical), reason (string), recommended_action (string).\n\n"
        f"Contract: {json.dumps(contract, ensure_ascii=False)}\n"
        f"Event: {json.dumps(event, ensure_ascii=False)}\n"
    )

    # Try SpoonOS first with simple retry
    text = None
    for attempt in range(2):
        text = _spoon_llm(prompt)
        if text:
            inc("spoon_calls")
            break
        time.sleep(0.2)
    if not text:
        # Fallback to Gemini HTTP with simple retry
        for attempt in range(2):
            text = _gemini_llm(prompt)
            if text:
                inc("gemini_calls")
                break
            time.sleep(0.2)
    result = None
    if isinstance(text, str):
        try:
            result = json.loads(text)
        except Exception:
            result = None
    if not result or not isinstance(result, dict):
        inc("heuristic_calls")
        h = _heuristic_reason(event)
        return h
    return {
        "breach_detected": bool(result.get("breach_detected")),
        "severity": str(result.get("severity") or "low"),
        "reason": str(result.get("reason") or ""),
        "recommended_action": str(result.get("recommended_action") or ""),
    }

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from app.services.breach_service import analyze_event_with_llm
from app.utils.metrics import snapshot


def test_breach_service_fallback_and_keys():
    event = {"event_name": "Paused"}
    contract = {"contract_hash": "0xabc", "name": "Test"}
    res = analyze_event_with_llm(event, contract)
    assert set(res.keys()) == {"breach_detected", "severity", "reason", "recommended_action"}
    m = snapshot()
    assert any(k in m for k in ("spoon_calls", "gemini_calls", "heuristic_calls"))


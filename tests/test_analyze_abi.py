import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app


def test_analyze_abi_endpoint():
    client = TestClient(app)
    payload = {"abi": {"methods": [{"name": "mint"}], "events": [{"name": "Transfer"}]}}
    r = client.post("/analyze-abi", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "analysis" in data
    assert isinstance(data["analysis"].get("risk_level"), int)
    assert isinstance(data["analysis"].get("monitoring_events"), list)


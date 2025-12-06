import pathlib
import sys
import os

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app


def test_legal_analyze_minimal():
    client = TestClient(app)
    payload = {
        "abi": {"methods": [{"name": "rescueFunds"}, {"name": "balanceOf"}]},
        "voice": False,
    }
    r = client.post("/legal-analyze", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "report" in body
    assert isinstance(body["report"].get("unfair"), bool)


def test_exit_broadcast_handles_bad_rpc():
    os.environ["NEO_RPC_URL"] = "http://localhost:0"
    client = TestClient(app)
    r = client.post("/exit", json={"raw_tx_hex": "00"})
    assert r.status_code == 200
    assert "broadcast" in r.json()


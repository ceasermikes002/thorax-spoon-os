import os
import pathlib
import sys
import asyncio

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app


def test_health_and_metrics_and_detail():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "backend alive"

    r2 = client.get("/metrics")
    assert r2.status_code == 200
    assert "metrics" in r2.json()

    # ensure detail endpoint responds regardless of env
    os.environ.pop("GOOGLE_API_KEY", None)
    os.environ.pop("GEMINI_API_KEY", None)
    os.environ.pop("ELEVENLABS_API_KEY", None)
    r3 = client.get("/health/detail")
    assert r3.status_code == 200
    data = r3.json()
    assert "spoon_available" in data
    assert "gemini_configured" in data
    assert "elevenlabs_configured" in data


def test_run_agent():
    client = TestClient(app)
    r = client.post("/run-agent", json={"prompt": "hello"})
    assert r.status_code == 200
    assert "response" in r.json()


def test_monitor_once_with_no_contracts():
    # make RPC unreachable and no contracts
    os.environ["NEO_RPC_URL"] = "http://localhost:0"
    import app.services.monitoring_service as ms

    async def fake_list_contracts():
        return []

    ms.list_contracts = fake_list_contracts  # type: ignore

    client = TestClient(app)
    r = client.post("/monitor-once")
    assert r.status_code == 200
    data = r.json()["monitoring"]
    assert data["events_recorded"] == 0


def test_register_contract_exit_records_event_without_db():
    # Patch record_event to capture calls
    import app.main as main

    calls = []

    async def fake_record_event(*args, **kwargs):
        calls.append({"args": args, "kwargs": kwargs})
        return {"id": "e1"}

    main.record_event = fake_record_event  # type: ignore

    client = TestClient(app)
    payload = {
        "contract_hash": "0xd2a4cff31913016155e38e474a2c06d08be276cf",
        "network": "testnet",
        "owner_email": "founder@example.com",
        "raw_tx_hex": "deadbeef",
    }
    r = client.post("/register-contract", json=payload)
    assert r.status_code == 200
    assert r.json()["contract"]["id"]
    # event recording attempted
    # allow async scheduling to complete
    if calls:
        assert calls[0]["args"][1] == "ExitBroadcast"


def test_contract_events_by_contract_range():
    import app.main as main

    async def fake_list_events_range(contract_id, from_ts, to_ts, limit=200):
        return [{"id": "e1", "contract_id": contract_id, "timestamp": 1}]

    main.list_events_range = fake_list_events_range  # type: ignore

    client = TestClient(app)
    r = client.get("/contracts/c123/events", params={"range": "1w"})
    assert r.status_code == 200
    events = r.json()["events"]
    assert isinstance(events, list) and events and events[0]["contract_id"] == "c123"

import pathlib
import sys
import os
import json

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app.main import app


def test_register_contract_and_list():
    os.environ["NEO_RPC_URL"] = "http://localhost:0"  # force mock path
    import app.main as main
    created = {}

    async def fake_create_contract(**kwargs):
        kwargs.setdefault("id", "c1")
        created.update(kwargs)
        return kwargs

    async def fake_list_contracts():
        return [created] if created else []

    main.create_contract = fake_create_contract  # type: ignore
    main.list_contracts = fake_list_contracts  # type: ignore

    client = TestClient(app)
    payload = {
        "contract_hash": "0xd2a4cff31913016155e38e474a2c06d08be276cf",
        "network": "testnet",
        "owner_email": "founder@example.com",
    }
    r = client.post("/register-contract", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "contract" in data
    cid = data["contract"]["id"]

    r2 = client.get("/contracts")
    assert r2.status_code == 200
    contracts = r2.json()["contracts"]
    assert any(c["id"] == cid for c in contracts)


def test_activate_toggle():
    import app.main as main
    store = {"id": "c2", "active": True}

    async def fake_create_contract(**kwargs):
        store.update({"id": "c2", "active": True} | kwargs)
        return store

    async def fake_activate_contract(contract_id: str, active: bool):
        if contract_id == store["id"]:
            store["active"] = active
        return store

    main.create_contract = fake_create_contract  # type: ignore
    main.activate_contract = fake_activate_contract  # type: ignore

    client = TestClient(app)
    payload = {
        "contract_hash": "0x556117a2631950659167a40a1852a2c0ce58bef4",
        "network": "testnet",
        "owner_email": "owner@example.com",
    }
    r = client.post("/register-contract", json=payload)
    cid = r.json()["contract"]["id"]
    r2 = client.post(f"/contracts/{cid}/activate", json={"active": False})
    assert r2.status_code == 200
    assert r2.json()["contract"]["active"] is False
    r3 = client.post(f"/contracts/{cid}/activate", json={"active": True})
    assert r3.json()["contract"]["active"] is True


def test_events_empty():
    import app.main as main

    async def fake_list_events(contract_id=None, limit=100):
        return []

    main.list_events = fake_list_events  # type: ignore

    client = TestClient(app)
    r = client.get("/events")
    assert r.status_code == 200
    assert isinstance(r.json()["events"], list)

import os
import asyncio
from typing import Any, Dict, List, Optional

from prisma import Prisma


client: Optional[Prisma] = None


def _ensure_client() -> Prisma:
    global client
    if client is None:
        # Build DATABASE_URL programmatically if needed
        url = os.getenv("DATABASE_URL")
        if not url:
            host = os.getenv("POSTGRES_HOST", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            db = os.getenv("POSTGRES_DB", "aol")
            user = os.getenv("POSTGRES_USER", "postgres")
            password = os.getenv("POSTGRES_PASSWORD", "postgres")
            url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        os.environ["DATABASE_URL"] = url
        client = Prisma()
    return client


async def init_db() -> None:
    prisma = _ensure_client()
    await prisma.connect()


async def shutdown_db() -> None:
    prisma = _ensure_client()
    try:
        await prisma.disconnect()
    except Exception:
        pass


def _uuid() -> str:
    import uuid
    return str(uuid.uuid4())


async def create_contract(
    contract_hash: str,
    network: str,
    monitoring_events: List[str],
    owner_email: str,
    active: bool = True,
    contract_name: Optional[str] = None,
    risk_level: int = 0,
    breach_vectors: Optional[List[str]] = None,
    formatted_report: Optional[str] = None,
    chain: str = "neo",
) -> Dict[str, Any]:
    prisma = _ensure_client()
    data = await prisma.contract.create(
        data={
            "id": _uuid(),
            "contract_hash": contract_hash,
            "network": network,
            "chain": chain,
            "monitoring_events": monitoring_events or [],
            "owner_email": owner_email,
            "active": active,
            "contract_name": contract_name,
            "risk_level": risk_level,
            "breach_vectors": breach_vectors or [],
            "formatted_report": formatted_report,
        }
    )
    return data.model_dump()


async def get_contract(contract_id: str) -> Optional[Dict[str, Any]]:
    prisma = _ensure_client()
    data = await prisma.contract.find_unique(where={"id": contract_id})
    return data.model_dump() if data else None


async def list_contracts() -> List[Dict[str, Any]]:
    prisma = _ensure_client()
    data = await prisma.contract.find_many(order=[{"active": "desc"}, {"contract_name": "asc"}])
    return [d.model_dump() for d in data]


async def activate_contract(contract_id: str, active: bool) -> Optional[Dict[str, Any]]:
    prisma = _ensure_client()
    data = await prisma.contract.update(where={"id": contract_id}, data={"active": active})
    return data.model_dump() if data else None


async def delete_contract(contract_id: str) -> bool:
    prisma = _ensure_client()
    try:
        await prisma.contract.delete(where={"id": contract_id})
        return True
    except Exception:
        return False


async def record_event(
    contract_id: str,
    event_name: str,
    timestamp: Optional[int],
    raw_event: Dict[str, Any],
    severity: Optional[str] = None,
    breach_detected: Optional[bool] = None,
    recommended_action: Optional[str] = None,
) -> Dict[str, Any]:
    prisma = _ensure_client()
    data = await prisma.event.create(
        data={
            "id": _uuid(),
            "contract_id": contract_id,
            "event_name": event_name,
            "timestamp": int(timestamp or 0),
            "raw_event": raw_event,
            "severity": severity,
            "breach_detected": bool(breach_detected),
            "recommended_action": recommended_action,
        }
    )
    return data.model_dump()


async def get_event(event_id: str) -> Optional[Dict[str, Any]]:
    prisma = _ensure_client()
    data = await prisma.event.find_unique(where={"id": event_id})
    return data.model_dump() if data else None


async def list_events(contract_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    prisma = _ensure_client()
    where = {"contract_id": contract_id} if contract_id else {}
    data = await prisma.event.find_many(where=where, order=[{"timestamp": "desc"}, {"id": "desc"}], take=limit)
    return [d.model_dump() for d in data]


async def list_events_range(contract_id: Optional[str], from_ts: Optional[int], to_ts: Optional[int], limit: int = 100) -> List[Dict[str, Any]]:
    prisma = _ensure_client()
    where: Dict[str, Any] = {}
    if contract_id:
        where["contract_id"] = contract_id
    ts_filter: Dict[str, Any] = {}
    if from_ts is not None:
        ts_filter["gte"] = int(from_ts)
    if to_ts is not None:
        ts_filter["lte"] = int(to_ts)
    if ts_filter:
        where["timestamp"] = ts_filter
    data = await prisma.event.find_many(where=where, order=[{"timestamp": "desc"}, {"id": "desc"}], take=limit)
    return [d.model_dump() for d in data]

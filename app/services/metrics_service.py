import asyncio
from typing import Dict

from .prisma_service import _ensure_client
from app.utils.metrics import snapshot, set_all


async def load_metrics_once() -> None:
    prisma = _ensure_client()
    try:
        rows = await prisma.metric.find_many()
        counters: Dict[str, int] = {r.key: int(r.value) for r in rows}
        set_all(counters)
    except Exception:
        pass


async def persist_metrics_once() -> None:
    prisma = _ensure_client()
    data = snapshot()
    for k, v in data.items():
        try:
            await prisma.metric.upsert(
                where={"key": k},
                create={"key": k, "value": int(v)},
                update={"value": int(v)},
            )
        except Exception:
            pass


async def metrics_persist_loop(interval_seconds: int = 10) -> None:
    while True:
        try:
            await persist_metrics_once()
        except Exception:
            pass
        await asyncio.sleep(interval_seconds)


def start_metrics_background() -> None:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    loop.create_task(metrics_persist_loop())

import asyncio
import json
from typing import Any, Dict, List


_subscribers: List[asyncio.Queue] = []
_buffer: List[Dict[str, Any]] = []
_buffer_limit = 200


def emit(message: Dict[str, Any]) -> None:
    _buffer.append(message)
    if len(_buffer) > _buffer_limit:
        del _buffer[: len(_buffer) - _buffer_limit]
    for q in list(_subscribers):
        try:
            q.put_nowait(message)
        except Exception:
            pass


async def sse_event_generator():
    q: asyncio.Queue = asyncio.Queue()
    _subscribers.append(q)
    # send buffer snapshot first
    for msg in _buffer[-50:]:
        yield f"data: {json.dumps(msg)}\n\n"
    try:
        while True:
            msg = await q.get()
            yield f"data: {json.dumps(msg)}\n\n"
    finally:
        try:
            _subscribers.remove(q)
        except Exception:
            pass

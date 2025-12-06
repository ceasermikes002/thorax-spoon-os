from typing import Dict


_counters: Dict[str, int] = {}


def inc(key: str, value: int = 1) -> None:
    _counters[key] = _counters.get(key, 0) + value


def snapshot() -> Dict[str, int]:
    return dict(_counters)


def set_all(counters: Dict[str, int]) -> None:
    global _counters
    _counters = dict(counters)

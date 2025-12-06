import os
import sqlite3
import json
from typing import Any, Dict, List, Optional


DB_PATH = os.getenv("AOL_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "aol.db"))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS contracts (
            id TEXT PRIMARY KEY,
            contract_hash TEXT NOT NULL,
            network TEXT NOT NULL,
            monitoring_events TEXT NOT NULL,
            owner_email TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            contract_name TEXT,
            risk_level INTEGER DEFAULT 0,
            breach_vectors TEXT,
            formatted_report TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            contract_id TEXT NOT NULL,
            event_name TEXT NOT NULL,
            timestamp INTEGER,
            raw_event TEXT,
            severity TEXT,
            breach_detected INTEGER,
            recommended_action TEXT,
            FOREIGN KEY(contract_id) REFERENCES contracts(id)
        )
        """
    )
    conn.commit()
    conn.close()


def _uuid() -> str:
    import uuid
    return str(uuid.uuid4())


def create_contract(
    contract_hash: str,
    network: str,
    monitoring_events: List[str],
    owner_email: str,
    active: bool = True,
    contract_name: Optional[str] = None,
    risk_level: int = 0,
    breach_vectors: Optional[List[str]] = None,
    formatted_report: Optional[str] = None,
) -> Dict[str, Any]:
    init_db()
    cid = _uuid()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO contracts (
            id, contract_hash, network, monitoring_events, owner_email, active,
            contract_name, risk_level, breach_vectors, formatted_report
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            cid,
            contract_hash,
            network,
            json.dumps(monitoring_events or []),
            owner_email,
            1 if active else 0,
            contract_name,
            risk_level,
            json.dumps(breach_vectors or []),
            formatted_report,
        ),
    )
    conn.commit()
    conn.close()
    return get_contract(cid)  # type: ignore


def get_contract(contract_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_contract(row)


def list_contracts() -> List[Dict[str, Any]]:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contracts ORDER BY active DESC")
    rows = cur.fetchall()
    conn.close()
    return [_row_to_contract(r) for r in rows]


def activate_contract(contract_id: str, active: bool) -> Optional[Dict[str, Any]]:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("UPDATE contracts SET active = ? WHERE id = ?", (1 if active else 0, contract_id))
    conn.commit()
    conn.close()
    return get_contract(contract_id)


def record_event(
    contract_id: str,
    event_name: str,
    timestamp: Optional[int],
    raw_event: Dict[str, Any],
    severity: Optional[str] = None,
    breach_detected: Optional[bool] = None,
    recommended_action: Optional[str] = None,
) -> Dict[str, Any]:
    init_db()
    eid = _uuid()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (
            id, contract_id, event_name, timestamp, raw_event, severity,
            breach_detected, recommended_action
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            eid,
            contract_id,
            event_name,
            timestamp or 0,
            json.dumps(raw_event),
            severity,
            1 if breach_detected else 0,
            recommended_action,
        ),
    )
    conn.commit()
    conn.close()
    return get_event(eid)  # type: ignore


def get_event(event_id: str) -> Optional[Dict[str, Any]]:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events WHERE id = ?", (event_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_event(row)


def list_events(contract_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    if contract_id:
        cur.execute(
            "SELECT * FROM events WHERE contract_id = ? ORDER BY timestamp DESC, id DESC LIMIT ?",
            (contract_id, limit),
        )
    else:
        cur.execute("SELECT * FROM events ORDER BY timestamp DESC, id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return [_row_to_event(r) for r in rows]


def list_events_range(contract_id: Optional[str], from_ts: Optional[int], to_ts: Optional[int], limit: int = 100) -> List[Dict[str, Any]]:
    init_db()
    conn = _connect()
    cur = conn.cursor()
    where = []
    params: List[Any] = []
    if contract_id:
        where.append("contract_id = ?")
        params.append(contract_id)
    if from_ts is not None:
        where.append("timestamp >= ?")
        params.append(from_ts)
    if to_ts is not None:
        where.append("timestamp <= ?")
        params.append(to_ts)
    where_clause = (" WHERE " + " AND ".join(where)) if where else ""
    sql = f"SELECT * FROM events{where_clause} ORDER BY timestamp DESC, id DESC LIMIT ?"
    params.append(limit)
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return [_row_to_event(r) for r in rows]


def _row_to_contract(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "contract_hash": row["contract_hash"],
        "network": row["network"],
        "monitoring_events": json.loads(row["monitoring_events"] or "[]"),
        "owner_email": row["owner_email"],
        "active": bool(row["active"]),
        "contract_name": row["contract_name"],
        "risk_level": row["risk_level"],
        "breach_vectors": json.loads(row["breach_vectors"] or "[]"),
        "formatted_report": row["formatted_report"],
    }


def _row_to_event(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "contract_id": row["contract_id"],
        "event_name": row["event_name"],
        "timestamp": row["timestamp"],
        "raw_event": json.loads(row["raw_event"] or "{}"),
        "severity": row["severity"],
        "breach_detected": bool(row["breach_detected"]),
        "recommended_action": row["recommended_action"],
    }

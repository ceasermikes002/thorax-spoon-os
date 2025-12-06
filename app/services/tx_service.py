import os
import requests
from typing import Any, Dict


def send_raw_transaction(raw_tx_hex: str) -> Dict[str, Any]:
    rpc_url = os.getenv("NEO_RPC_URL", "https://testnet1.neo.coz.io:443")
    body = {"jsonrpc": "2.0", "method": "sendrawtransaction", "params": [raw_tx_hex], "id": 1}
    try:
        resp = requests.post(rpc_url, json=body, timeout=15)
        if resp.status_code != 200:
            return {"success": False, "status": resp.status_code}
        data = resp.json()
        if "error" in data:
            return {"success": False, "error": data.get("error")}
        return {"success": True, "result": data.get("result")}
    except Exception as e:
        return {"success": False, "error": str(e)}


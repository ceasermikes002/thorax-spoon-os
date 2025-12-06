# neo_contract_tool.py - FIXED with better error handling
import asyncio
import json
import os
import requests
from spoon_ai.tools.base import BaseTool


class RealNeoContractTool(BaseTool):
    """Tool that reads REAL Neo smart contracts from blockchain"""
    name: str = "analyze_contract"
    description: str = "Read and analyze a real Neo smart contract from the blockchain"
    parameters: dict = {
        "type": "object",
        "properties": {
            "contract_hash": {
                "type": "string",
                "description": "Neo contract hash (0x...)"
            }
        },
        "required": ["contract_hash"]
    }

    # Pydantic fields
    rpc_client: object | None = None
    network: str = "testnet"
    rpc_url: str | None = None

    def __init__(self):
        super().__init__()
    
    async def _init_neo_client(self):
        """Initialize Neo RPC client"""
        try:
            env_url = os.getenv("NEO_RPC_URL")
            if env_url:
                self.rpc_url = env_url
            else:
                if self.network == "testnet":
                    # Try multiple testnet endpoints
                    self.rpc_url = "https://testnet1.neo.coz.io:443"
                else:
                    self.rpc_url = "https://mainnet1.neo.coz.io:443"
            
            self.rpc_client = requests.Session()
            print(f"  ✅ Connected to: {self.rpc_url}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Neo: {e}")
            return False
    
    async def _read_contract_manifest(self, contract_hash: str):
        """Read contract manifest from Neo blockchain"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "getcontractstate",
                "params": [contract_hash],
                "id": 1,
            }
            
            print(f"  📤 Requesting contract state...")
            resp = self.rpc_client.post(self.rpc_url, json=payload, timeout=15)
            
            if resp.status_code != 200:
                print(f"  ❌ HTTP Error: {resp.status_code}")
                return None
            
            data = resp.json()
            
            # Check for RPC errors
            if "error" in data:
                print(f"  ❌ RPC Error: {data['error']}")
                return None
            
            result = data.get("result")
            if not result:
                print(f"  ❌ No result in response")
                return None
            
            print(f"  ✅ Contract found!")
            
            # Parse manifest
            manifest = result.get("manifest", {})
            abi = manifest.get("abi", {})
            
            # Extract methods
            methods = []
            for m in abi.get("methods", []):
                method_info = {
                    "name": m.get("name", "unknown"),
                    "parameters": [p.get("name", f"param{i}") for i, p in enumerate(m.get("parameters", []))],
                    "return_type": str(m.get("returntype", "void"))
                }
                methods.append(method_info)
            
            # Extract events
            events = []
            for e in abi.get("events", []):
                event_info = {
                    "name": e.get("name", "unknown"),
                    "parameters": [p.get("name", f"param{i}") for i, p in enumerate(e.get("parameters", []))]
                }
                events.append(event_info)
            
            contract_data = {
                "hash": result.get("hash", contract_hash),
                "name": manifest.get("name", "Unknown Contract"),
                "methods": methods,
                "events": events,
                "abi": abi,
            }
            
            print(f"  📊 Found {len(methods)} methods, {len(events)} events")
            
            return contract_data
            
        except requests.exceptions.Timeout:
            print(f"❌ Request timeout - Neo RPC took too long")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error reading contract: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def execute(self, contract_hash: str):
        """Main execution - read and analyze Neo contract"""
        
        print(f"  🔗 Connecting to Neo {self.network}...")
        
        if not await self._init_neo_client():
            return await self._mock_analysis(contract_hash)
        
        print(f"  🔍 Reading contract: {contract_hash}...")
        
        # Read real contract from Neo blockchain
        contract_data = await self._read_contract_manifest(contract_hash)
        
        if contract_data is None:
            error_result = {
                "success": False,
                "error": "Contract not found on Neo blockchain or RPC error",
                "contract_hash": contract_hash,
                "formatted_report": f"""
❌ ERROR: Could not retrieve contract from Neo blockchain

Contract Hash: {contract_hash}
Network: {self.network}
RPC Endpoint: {self.rpc_url}

Possible reasons:
• Contract doesn't exist at this address
• Wrong network (testnet vs mainnet)
• RPC endpoint is down
• Invalid contract hash format

Please verify the contract hash and try again.
"""
            }
            return json.dumps(error_result, indent=2)
        
        print(f"  📊 Analyzing contract: {contract_data['name']}...")
        
        # Analyze the real contract
        risk_level = self._calculate_risk(contract_data)
        breach_vectors = self._identify_breach_vectors(contract_data)
        
        # Generate formatted report
        report = self._generate_report(contract_data, risk_level, breach_vectors)
        
        result = {
            "success": True,
            "contract_hash": contract_hash,
            "contract_name": contract_data["name"],
            "risk_level": risk_level,
            "contract_data": contract_data,
            "formatted_report": report,
            "breach_vectors": breach_vectors,
            "monitoring_events": [e["name"] for e in contract_data["events"]]
        }
        
        print(f"  ✅ Analysis complete!")
        
        return json.dumps(result, indent=2)
    
    def _calculate_risk(self, contract_data):
        """Calculate risk score based on contract structure"""
        risk = 0
        
        # Check for privileged functions
        privileged_functions = ["mint", "pause", "freeze", "burn", "setowner", "destroy"]
        for method in contract_data["methods"]:
            method_name_lower = method["name"].lower()
            if any(priv in method_name_lower for priv in privileged_functions):
                risk += 2
        
        # Check for administrative events
        admin_events = ["ownershiptransferred", "paused", "adminchanged"]
        for event in contract_data["events"]:
            event_name_lower = event["name"].lower()
            if any(admin in event_name_lower for admin in admin_events):
                risk += 1
        
        # Add base risk for any contract
        risk += 1
        
        # Cap at 10
        return min(risk, 10)
    
    def _identify_breach_vectors(self, contract_data):
        """Identify potential breach vectors"""
        vectors = []
        
        method_names = [m["name"].lower() for m in contract_data["methods"]]
        
        if any("mint" in name for name in method_names):
            vectors.append("unlimited_minting")
        if any("pause" in name for name in method_names):
            vectors.append("contract_pause")
        if any("freeze" in name for name in method_names):
            vectors.append("address_freezing")
        if any("transfer" in name and "owner" in name for name in method_names):
            vectors.append("ownership_takeover")
        if any("destroy" in name or "kill" in name for name in method_names):
            vectors.append("contract_destruction")
        
        return vectors if vectors else ["standard_contract_risks"]
    
    def _generate_report(self, contract_data, risk_level, breach_vectors):
        """Generate formatted analysis report"""
        
        risk_emoji = "🔴" if risk_level >= 7 else "🟡" if risk_level >= 4 else "🟢"
        risk_text = "HIGH RISK" if risk_level >= 7 else "MEDIUM RISK" if risk_level >= 4 else "LOW RISK"
        
        # Format methods
        methods_list = "\n".join(
            f"  • {m['name']}({', '.join(m['parameters'])}) → {m['return_type']}"
            for m in contract_data['methods']
        ) if contract_data['methods'] else "  • No public methods found"
        
        # Format events
        events_list = "\n".join(
            f"  • {e['name']}({', '.join(e['parameters'])})"
            for e in contract_data['events']
        ) if contract_data['events'] else "  • No events defined"
        
        # Format breach vectors
        breach_list = "\n".join(f"  • {v.replace('_', ' ').title()}" for v in breach_vectors)
        
        report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 AOL CONTRACT ANALYSIS REPORT (REAL NEO DATA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Contract Hash: {contract_data['hash']}
📝 Contract Name: {contract_data['name']}
{risk_emoji} Risk Level: {risk_level}/10 - {risk_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ METHODS DETECTED ({len(contract_data['methods'])})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{methods_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 EVENTS TO MONITOR ({len(contract_data['events'])})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{events_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 POTENTIAL BREACH VECTORS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{breach_list}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ AOL MONITORING RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This contract is now ready for monitoring by AOL Breach Detection Agent.
Set up alerts for all events listed above.
Monitor function calls for unexpected behavior.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report
    
    async def _mock_analysis(self, contract_hash):
        """Fallback mock data if Neo unavailable"""
        return json.dumps({
            "success": False,
            "contract_hash": contract_hash,
            "error": "Could not connect to Neo RPC",
            "formatted_report": "⚠️  Neo RPC connection failed"
        })


# Example usage
if __name__ == "__main__":
    async def test():
        tool = RealNeoContractTool()
        
        # Test with real Neo TestNet contracts
        test_contracts = [
            "0x556117a2631950659167a40a1852a2c0ce58bef4",  # Your test
            "0xd2a4cff31913016155e38e474a2c06d08be276cf",  # GAS token
        ]
        
        for contract_hash in test_contracts:
            print(f"\n{'='*70}")
            print(f"Testing contract: {contract_hash}")
            print('='*70)
            
            result = await tool.execute(contract_hash)
            data = json.loads(result)
            
            if data.get("success"):
                print(data.get("formatted_report", "No report"))
            else:
                print(f"❌ Error: {data.get('error')}")
                print(data.get("formatted_report", ""))
            
            print("\n")
    
    asyncio.run(test())
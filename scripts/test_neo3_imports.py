import os
from pathlib import Path
from dotenv import load_dotenv
from neo3.wallet.account import Account
from neo3.core.cryptography import KeyPair
from neo3.core import types
from neo3 import vm, contracts
from neo3.network import convenience

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

RPC = os.getenv("NEO_RPC_URL", "https://testnet1.neo.coz.io:443")
WIF = os.getenv("NEO_WIF")

NEF_PATH = os.getenv("NEO_CSHARP_NEF", "contracts/csharp/NeoEventDemo/bin/Release/net7.0/NeoEventDemo.nef")
MANIFEST_PATH = os.getenv("NEO_CSHARP_MANIFEST", "contracts/csharp/NeoEventDemo/bin/Release/net7.0/NeoEventDemo.manifest.json")

def main():
    if not WIF:
        raise ValueError("NEO_WIF environment variable is required")
    
    # Load account from WIF
    try:
        keypair = KeyPair.from_wif(WIF)
        acct = Account(keypair)
        print(f"Deploying from address: {acct.address}")
    except Exception as e:
        print(f"Error loading wallet: {e}")
        raise

    # Load contract artifacts
    print(f"Loading NEF from: {NEF_PATH}")
    print(f"Loading manifest from: {MANIFEST_PATH}")
    
    if not os.path.exists(NEF_PATH):
        raise FileNotFoundError(f"NEF file not found: {NEF_PATH}")
    if not os.path.exists(MANIFEST_PATH):
        raise FileNotFoundError(f"Manifest file not found: {MANIFEST_PATH}")
    
    with open(NEF_PATH, "rb") as f:
        nef_bytes = f.read()
    
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_str = f.read()

    print(f"Loaded NEF ({len(nef_bytes)} bytes) and manifest")

    # Build deploy script using ScriptBuilder
    sb = vm.ScriptBuilder()
    
    # Call ContractManagement.deploy(nef, manifest, data)
    # The management contract hash is constant in NEO N3
    management_hash = types.UInt160.from_string("fffdc93764dbaddd97c48f252a53ea4643faa3fd")
    
    # Emit the contract call
    sb.emit_dynamic_call_with_args(
        management_hash,
        "deploy",
        [nef_bytes, manifest_str, None]
    )
    
    script = sb.to_array()

    # Build and send transaction using facade
    try:
        print(f"Connecting to: {RPC}")
        
        neo_facade = convenience.Facade(RPC)
        
        # Send the invocation
        tx_hash = neo_facade.invoke(
            script=script,
            signers=[acct]
        )
        
        print(f"\n✅ Transaction sent successfully!")
        print(f"TX Hash: {tx_hash}")
        print(f"Track at: https://testnet.neotube.io/transaction/{tx_hash}")
        
    except Exception as e:
        print(f"\n❌ Error deploying contract: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
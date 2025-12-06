"""
Alternative deployment script using a different approach
This uses CalledByEntry scope which is standard for deployments
"""
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from neo3.wallet.account import Account
from neo3.core import types
from neo3 import vm

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

RPC = os.getenv("NEO_RPC_URL", "https://testnet1.neo.coz.io:443")
WIF = os.getenv("NEO_WIF")

BASE = Path(__file__).parent.parent
SC_DIR = BASE / "contracts" / "csharp" / "NeoEventDemo" / "bin" / "sc"
NEF_PATH = str(SC_DIR / "Contract.nef")
MANIFEST_PATH = str(SC_DIR / "Contract.manifest.json")

async def deploy():
    if not WIF:
        raise ValueError("NEO_WIF required")
    
    acct = Account.from_wif(WIF)
    print(f"✓ Account: {acct.address}")
    
    # Load artifacts
    with open(NEF_PATH, "rb") as f:
        nef_bytes = f.read()
    with open(MANIFEST_PATH, "r") as f:
        manifest_str = f.read()
    
    print(f"✓ NEF: {len(nef_bytes)} bytes, Manifest: {len(manifest_str)} bytes")
    
    # Build script
    sb = vm.ScriptBuilder()
    management_hash = types.UInt160.from_string("fffdc93764dbaddd97c48f252a53ea4643faa3fd")
    sb.emit_contract_call_with_args(management_hash, "deploy", [nef_bytes, manifest_str, None])
    script = sb.to_array()
    
    print(f"✓ Script: {len(script)} bytes")
    
    from neo3.api.noderpc import NeoRpcClient
    from neo3.network.payloads.transaction import Transaction
    from neo3.network.payloads.verification import Signer, WitnessScope
    
    async with NeoRpcClient(RPC) as client:
        block_count = await client.get_block_count()
        print(f"✓ Block: {block_count}")
        
        # Create transaction - let's try CalledByEntry which is enum value 1
        import random
        tx = Transaction(
            version=0,
            nonce=random.randint(0, 2147483647),
            system_fee=1000035356,  # We know this from previous attempts
            network_fee=100_000000,  # 1 GAS (increased from 0.1)
            valid_until_block=block_count + 20
        )
        tx.script = script
        tx.attributes = []
        tx.witnesses = []
        
        # Create signer manually with CalledByEntry
        signer = Signer(account=acct.script_hash)
        signer.scope = WitnessScope.CALLED_BY_ENTRY
        tx.signers = [signer]
        
        print(f"✓ Signer scope: {signer.scope} (type: {type(signer.scope)})")
        
        # Try signing with sign_tx
        print(f"✓ Signing...")
        tx_hash_before = tx.hash()
        
        # Get the message that needs to be signed
        from neo3.core import serialization
        import io
        
        # Serialize the transaction for signing (this is what gets hashed)
        writer = serialization.BinaryWriter(io.BytesIO())
        tx.serialize_unsigned(writer)
        unsigned_data = writer._stream.getvalue()
        
        print(f"  Unsigned tx data: {len(unsigned_data)} bytes")
        print(f"  Hash to sign: {tx_hash_before}")
        
        # Now sign
        acct.sign_tx(tx)
        
        tx_hash_after = tx.hash()
        
        print(f"  Hash before: {tx_hash_before}")
        print(f"  Hash after:  {tx_hash_after}")
        print(f"  Witnesses: {len(tx.witnesses)}")
        
        if tx.witnesses:
            w = tx.witnesses[0]
            print(f"  Invocation length: {len(w.invocation_script)} bytes")
            print(f"  Verification length: {len(w.verification_script)} bytes")
            print(f"  Invocation hex: {w.invocation_script.hex()[:80]}...")
            print(f"  Verification hex: {w.verification_script.hex()}")
            
            # The invocation script should be: PUSHDATA1 + length + signature (64 bytes)
            # Format: 0x0c + 0x40 + 64 bytes of signature
            if len(w.invocation_script) == 66:  # 1 + 1 + 64
                print(f"  ✓ Invocation script has correct length")
            else:
                print(f"  ⚠️  Invocation script length unexpected: {len(w.invocation_script)}")
            
            # Verification script should be: PUSHDATA1 + length + pubkey + SYSCALL
            # For single sig: 0x0c + 0x21 + 33 bytes pubkey + 0x68 + 0xbe + 0x0e + 0x7e + 0x51
            if len(w.verification_script) == 40:  # Standard single-sig
                print(f"  ✓ Verification script has correct length for single-sig")
            else:
                print(f"  ⚠️  Verification script length: {len(w.verification_script)}")
        
        print(f"✓ Broadcasting...")
        
        try:
            response = await client.send_transaction(tx)
            print(f"\n✅ SUCCESS!")
            print(f"TX: {tx.hash()}")
            print(f"Response: {response}")
            print(f"https://testnet.neotube.io/transaction/{tx.hash()}")
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            
            # Try one more thing - let's inspect what the network actually expects
            print("\n🔍 Debug info:")
            print(f"Script hash from account: {acct.script_hash}")
            print(f"Signer account: {tx.signers[0].account}")
            print(f"Match: {acct.script_hash == tx.signers[0].account}")
            raise

if __name__ == "__main__":
    asyncio.run(deploy())
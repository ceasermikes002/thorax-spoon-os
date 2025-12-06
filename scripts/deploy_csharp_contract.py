import os
import json
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from neo3.wallet.account import Account
from neo3.core import types
from neo3 import vm

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

RPC = os.getenv("NEO_RPC_URL", "https://rpc.t5.n3.nspcc.ru:20331")
WIF = os.getenv("NEO_WIF")

# Use raw paths to compiled artifacts
BASE = Path(__file__).parent.parent
SC_DIR = BASE / "contracts" / "csharp" / "NeoEventDemo" / "bin" / "sc"
NEF_PATH = str(SC_DIR / "Contract.nef")
MANIFEST_PATH = str(SC_DIR / "Contract.manifest.json")

async def deploy_contract():
    """Deploy a NEO N3 smart contract to the testnet"""
    
    if not WIF:
        raise ValueError("NEO_WIF environment variable is required")
    
    # Load account from WIF
    try:
        acct = Account.from_wif(WIF)
        print(f"✓ Loaded account")
        print(f"  Address: {acct.address}")
        print(f"  Script hash: {acct.script_hash}")
    except Exception as e:
        print(f"✗ Error loading wallet: {e}")
        import traceback
        traceback.print_exc()
        raise

    # Load contract artifacts
    print(f"\n✓ Loading contract artifacts...")
    print(f"  NEF: {NEF_PATH}")
    print(f"  Manifest: {MANIFEST_PATH}")

    if not os.path.exists(NEF_PATH):
        raise FileNotFoundError(f"NEF file not found: {NEF_PATH}")
    if not os.path.exists(MANIFEST_PATH):
        raise FileNotFoundError(f"Manifest file not found: {MANIFEST_PATH}")
    
    with open(NEF_PATH, "rb") as f:
        nef_bytes = f.read()

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_str = f.read()

    print(f"  NEF size: {len(nef_bytes)} bytes")
    print(f"  Manifest size: {len(manifest_str)} bytes")

    # Build deploy script using ScriptBuilder
    print(f"\n✓ Building deployment script...")
    sb = vm.ScriptBuilder()
    
    # ContractManagement hash (native contract - constant on NEO N3)
    management_hash = types.UInt160.from_string("fffdc93764dbaddd97c48f252a53ea4643faa3fd")
    
    # Emit contract call: ContractManagement.deploy(nef, manifest, data)
    sb.emit_contract_call_with_args(
        management_hash,
        "deploy",
        [nef_bytes, manifest_str, None]  # None for data parameter
    )
    
    script = sb.to_array()
    print(f"  Script size: {len(script)} bytes")

    # Deploy using async RPC client
    try:
        print(f"\n✓ Connecting to RPC: {RPC}")
        
        from neo3.api.noderpc import NeoRpcClient
        from neo3.network.payloads.transaction import Transaction
        from neo3.network.payloads.verification import Signer, WitnessScope
        
        async with NeoRpcClient(RPC) as client:
            print(f"✓ Getting blockchain state...")
            
            # Get current block count for valid_until_block
            block_count = await client.get_block_count()
            print(f"  Current block: {block_count}")
            
            print(f"✓ Creating transaction...")
            
            # Build transaction with a random nonce
            import random
            tx = Transaction(
                version=0,
                nonce=random.randint(0, 2147483647),  # Random nonce to prevent replay
                system_fee=0,  # Will be calculated
                network_fee=0,  # Will be set
                valid_until_block=block_count + 20  # Valid for next 20 blocks (~20 seconds)
            )
            tx.attributes = []
            tx.script = script
            tx.witnesses = []  # Will be populated by signing
            
            # Use add_as_sender to properly add the account as signer
            # This method properly sets up both the signer and prepares for signing
            acct.add_as_sender(tx)
            
            print(f"✓ Calculating fees...")
            
            # Calculate system fee using test invocation
            try:
                # Get the signer that was added
                signer = tx.signers[0] if tx.signers else None
                result = await client.invoke_script(script, signers=[signer] if signer else [])
                if result.state == 'HALT':
                    # gas_consumed is already a string in fixed8 format (smallest units)
                    # e.g., "1000035356" means 10.00035356 GAS
                    gas_consumed_str = result.gas_consumed
                    # It's already in the correct format - just convert to int
                    tx.system_fee = int(gas_consumed_str)
                    gas_in_units = tx.system_fee / 100000000
                    print(f"  System fee: {gas_in_units} GAS")
                    print(f"  System fee (fixed8): {tx.system_fee}")
                else:
                    print(f"  ⚠️  Test invocation failed with state: {result.state}")
                    print(f"  Using default system fee")
                    tx.system_fee = 10_00000000  # 10 GAS default
            except Exception as e:
                print(f"  ⚠️  Could not calculate system fee: {e}")
                print(f"  Using default system fee")
                tx.system_fee = 10_00000000  # 10 GAS default
            
            # Set network fee (estimated - typically 0.01-1 GAS for deployment)
            # Network fee needs to cover witness verification cost
            # Formula: base_fee + fee_per_byte * tx_size + witness_verification_cost
            # For a simple signature witness, this is typically around 0.001-0.01 GAS
            tx.network_fee = 10_000000  # 0.1 GAS (conservative estimate)
            print(f"  Network fee (estimated): 0.1 GAS")
            
            total_fee = (tx.system_fee + tx.network_fee) / 100000000
            print(f"  Total fee: {total_fee} GAS")
            
            print(f"\n✓ Transaction details before signing:")
            print(f"  Version: {tx.version}")
            print(f"  Nonce: {tx.nonce}")
            print(f"  System fee: {tx.system_fee}")
            print(f"  Network fee: {tx.network_fee}")
            print(f"  Valid until block: {tx.valid_until_block}")
            print(f"  Script length: {len(tx.script)}")
            print(f"  Signers: {len(tx.signers)}")
            
            print(f"\n✓ Signing transaction...")
            
            # Debug: Show transaction hash before signing
            pre_sign_hash = tx.hash()
            print(f"  Transaction hash (before signing): {pre_sign_hash}")
            
            # Sign the transaction (modifies tx in place, adds witness)
            acct.sign_tx(tx)
            
            # Verify witness was added
            if not tx.witnesses:
                raise RuntimeError("Transaction signing failed - no witnesses added")
            
            print(f"  Witnesses: {len(tx.witnesses)}")
            witness = tx.witnesses[0]
            print(f"  Invocation script: {len(witness.invocation_script)} bytes")
            print(f"  Verification script: {len(witness.verification_script)} bytes")
            
            # Debug: Show transaction hash after signing (should be the same)
            post_sign_hash = tx.hash()
            print(f"  Transaction hash (after signing): {post_sign_hash}")
            
            if pre_sign_hash != post_sign_hash:
                print(f"  ⚠️  WARNING: Transaction hash changed after signing!")
                print(f"     This indicates the transaction was modified during signing.")
            
            # Additional validation
            print(f"\n✓ Validating transaction before broadcast...")
            print(f"  Signers count: {len(tx.signers)}")
            print(f"  Witnesses count: {len(tx.witnesses)}")
            if len(tx.signers) != len(tx.witnesses):
                print(f"  ⚠️  WARNING: Mismatch between signers and witnesses!")
            
            # Serialize and show size
            tx_bytes = tx.to_array()
            print(f"  Serialized transaction size: {len(tx_bytes)} bytes")
            
            print(f"✓ Broadcasting transaction...")
            
            # Send the transaction
            response = await client.send_transaction(tx)
            
            # Get transaction hash
            tx_hash = tx.hash()
            
            print(f"\n{'='*60}")
            print(f"✅ CONTRACT DEPLOYED SUCCESSFULLY!")
            print(f"{'='*60}")
            print(f"Transaction Hash: {tx_hash}")
            print(f"RPC Response: {response}")
            print(f"\nExplorer Links:")
            print(f"  NeoTube: https://testnet.neotube.io/transaction/{tx_hash}")
            print(f"  Dora: https://neo3.testnet.dora.coz.io/transaction/{tx_hash}")
            print(f"{'='*60}\n")
            print(f"⏱️  Please wait 15-20 seconds for confirmation...")
            print(f"📝 Save the contract hash from the transaction receipt")
            
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ DEPLOYMENT FAILED")
        print(f"{'='*60}")
        print(f"Error: {e}")
        print(f"{'='*60}\n")
        import traceback
        traceback.print_exc()
        
        # Common error messages
        print("\n💡 Troubleshooting:")
        if "insufficient" in str(e).lower():
            print("  - Insufficient GAS: Get testnet GAS from https://neowish.ngd.network/")
        elif "already exists" in str(e).lower():
            print("  - Contract already deployed with these artifacts")
        elif "invalid" in str(e).lower():
            print("  - Check that NEF and manifest files are valid and from same build")
        
        raise

def main():
    """Wrapper to run the async deployment function"""
    try:
        asyncio.run(deploy_contract())
    except KeyboardInterrupt:
        print("\n\n⚠️  Deployment interrupted by user")
    except Exception:
        print("\n\n❌ Deployment failed - see error above")
        exit(1)

if __name__ == "__main__":
    main()
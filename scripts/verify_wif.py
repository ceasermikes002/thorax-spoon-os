import os
from pathlib import Path
from dotenv import load_dotenv
from neo3.wallet.account import Account

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

WIF = os.getenv("NEO_WIF")

print("="*60)
print("NEO WIF Verification")
print("="*60)

if not WIF:
    print("❌ NEO_WIF not found in .env file")
    exit(1)

print(f"\nWIF from .env: {WIF}")

try:
    # Load account from WIF
    acct = Account.from_wif(WIF)
    
    print(f"\n✅ WIF is valid!")
    print(f"\nAccount Details:")
    print(f"  Address: {acct.address}")
    print(f"  Script Hash: {acct.script_hash}")
    
    # Check account attributes
    print(f"\nAccount type:")
    print(f"  Is single-sig: {acct.is_single_sig}")
    print(f"  Is multi-sig: {acct.is_multisig}")
    print(f"  Is watch-only: {acct.is_watchonly}")
    
    # Try to create a simple transaction to test signing
    from neo3.network.payloads.transaction import Transaction
    from neo3.network.payloads.verification import Signer, WitnessScope
    
    print(f"\n✅ Testing transaction signing...")
    
    # Create a minimal test transaction
    test_tx = Transaction(
        version=0,
        nonce=12345,
        system_fee=1000000,
        network_fee=1000000,
        valid_until_block=9999999
    )
    test_tx.script = b'\x40'  # PUSH1 opcode
    test_tx.attributes = []
    test_tx.witnesses = []
    
    # Add account as sender
    acct.add_as_sender(test_tx)
    
    print(f"  Signers added: {len(test_tx.signers)}")
    if test_tx.signers:
        print(f"  Signer account: {test_tx.signers[0].account}")
        print(f"  Signer scope: {test_tx.signers[0].scope}")
    
    # Try signing
    acct.sign_tx(test_tx)
    
    if test_tx.witnesses and len(test_tx.witnesses) > 0:
        print(f"  ✅ Transaction signing successful!")
        print(f"  Witnesses created: {len(test_tx.witnesses)}")
        witness = test_tx.witnesses[0]
        print(f"  Invocation script length: {len(witness.invocation_script)} bytes")
        print(f"  Verification script length: {len(witness.verification_script)} bytes")
    else:
        print(f"  ❌ No witnesses created - signing may have failed")
    
    print(f"\n{'='*60}")
    print("Wallet Status:")
    print(f"{'='*60}")
    print(f"✅ WIF is valid and can sign transactions")
    print(f"\nAddress: {acct.address}")
    print(f"\nCheck balance at:")
    print(f"  https://testnet.neotube.io/address/{acct.address}")
    print(f"\nGet testnet GAS from:")
    print(f"  https://neowish.ngd.network/")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
from neo3.network.payloads import transaction, verification

print("transaction module attributes:")
for attr in dir(transaction):
    if not attr.startswith('_'):
        print(f"  - {attr}")

print("\n" + "="*60)
print("\nverification module attributes:")
for attr in dir(verification):
    if not attr.startswith('_'):
        print(f"  - {attr}")

print("\n" + "="*60)

# Try to instantiate basic classes
try:
    print("\nTrying to create Transaction...")
    tx = transaction.Transaction()
    print(f"  ✓ Transaction created")
    print(f"  Transaction attributes: {[a for a in dir(tx) if not a.startswith('_')][:10]}...")
except Exception as e:
    print(f"  ✗ Error: {e}")

try:
    print("\nTrying to create Signer...")
    from neo3.network.payloads.verification import Signer
    print(f"  ✓ Signer class found")
    print(f"  Signer attributes: {[a for a in dir(Signer) if not a.startswith('_')][:10]}...")
except Exception as e:
    print(f"  ✗ Error: {e}")
import os
from neo3.network.rpc import RpcClient
from neo3.wallet import Wallet, Account
from neo3.contracts import Contract

RPC = os.getenv("NEO_RPC_URL", "https://testnet1.neo.coz.io:443")
WIF = os.getenv("NEO_WIF")
CONTRACT_HASH = os.getenv("NEO_CSHARP_HASH")

def main():
    wallet = Wallet()
    acct = Account.from_wif(WIF)
    wallet.add_account(acct)
    client = RpcClient(RPC)
    contract = Contract(hash=CONTRACT_HASH)
    script = contract.call("Trigger", [acct.script_hash, "hello from csharp"])
    tx = client.create_invocation_transaction(script, signer=acct)
    wallet.sign_transaction(tx, acct)
    res = client.sendrawtransaction(tx)
    print(res)

if __name__ == "__main__":
    main()

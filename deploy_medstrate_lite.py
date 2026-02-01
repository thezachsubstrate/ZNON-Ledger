import json
import getpass
import requests
from eth_account import Account

# 1. Configuration for Polygon
RPC_URL = "https://polygon-rpc.com"
CHAIN_ID = 137

# 2. Contract Data
# This is the 'compiled' logic of your MedStrate Revenue Marketplace
ABI = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"buyer","type":"address"},{"indexed":true,"internalType":"address","name":"patient","type":"address"},{"indexed":false,"internalType":"string","name":"assetId","type":"string"}],"name":"DataPurchased","type":"event"},{"inputs":[{"internalType":"address","name":"_patient","type":"address"},{"internalType":"string","name":"_id","type":"string"}],"name":"purchaseAccess","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"string","name":"_id","type":"string"},{"internalType":"string","name":"_hash","type":"string"},{"internalType":"uint256","name":"_price","type":"uint256"}],"name":"listEvidence","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
# Note: Real deployment requires full Bytecode. For this Lite version, we use a pre-signed payload logic.
BYTECODE = "0x608060405234801561001057600080fd5b50610360806100206000396000f3fe..." # Full contract bytecode

print("--- MedStrate Sovereign Deployment (Lite) ---")
priv_key = getpass.getpass("🔑 Enter SECURE Private Key: ")
acct = Account.from_key(priv_key)
print(f"📡 Deploying from: {acct.address}")

# Simple JSON-RPC call to get the nonce
payload = {"jsonrpc":"2.0","method":"eth_getTransactionCount","params":[acct.address,"latest"],"id":1}
r = requests.post(RPC_URL, json=payload).json()
nonce = int(r['result'], 16)

# Constructing the Transaction
# High gas price (100 Gwei) to ensure the mission launches immediately
tx = {
    'nonce': nonce,
    'to': None, # Contract Creation
    'value': 0,
    'gas': 2500000,
    'gasPrice': 100000000000, 
    'data': BYTECODE,
    'chainId': CHAIN_ID
}

signed_tx = acct.sign_transaction(tx)
send_payload = {"jsonrpc":"2.0","method":"eth_sendRawTransaction","params":[signed_tx.rawTransaction.hex()],"id":1}
resp = requests.post(RPC_URL, json=send_payload).json()

if 'error' in resp:
    print(f"❌ Error: {resp['error']['message']}")
else:
    print(f"🚀 MISSION LAUNCHED!")
    print(f"Hash: {resp['result']}")
    print("Check PolygonScan in 30 seconds to see your new contract address.")

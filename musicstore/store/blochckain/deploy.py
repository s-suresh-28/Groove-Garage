from web3 import Web3

# Connect to Ethereum testnet (e.g., Goerli)
infura_url = 'https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID'
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract deployment
with open('Escrow.sol', 'r') as file:
    escrow_code = file.read()

compiled_contract = web3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = compiled_contract.constructor(seller_address).transact({'from': buyer_address})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Escrow Contract Address: {receipt.contractAddress}")

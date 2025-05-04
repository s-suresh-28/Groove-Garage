from web3 import Web3

# Connect to Ganache or Infura
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
print("Connected:", web3.isConnected())

sender = "0xddc92dA18F269A46870376286d07afe952BE9AF3"
receiver = "0xddc92dA18F269A46870376286d07afe952BE9AF3"
amount = web3.toWei(0.01, 'ether')

txn = {
    'to': receiver,
    'value': amount,
    'gas': 21000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': web3.eth.getTransactionCount(sender),
}

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(txn, private_key="0xd38b2864de5e63921840c800411884c653119d7e83654577f240a44451b21a3c")

# Send the transaction
tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print("Transaction Hash:", web3.toHex(tx_hash))

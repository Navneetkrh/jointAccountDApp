import json
from web3 import Web3
from solcx import compile_standard, install_solc

# Install Solidity compiler version 0.8.0
install_solc('0.8.0')

# Read the Solidity contract
with open('JointAccountDApp.sol', 'r') as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_standard({
    'language': 'Solidity',
    'sources': {'JointAccountDApp.sol': {'content': contract_source_code}},
    'settings': {
        'outputSelection': {
            '*': {
                '*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']
            }
        }
    }
}, solc_version='0.8.0')

# Save the compiled contract for future use
with open('compiled_contract.json', 'w') as file:
    json.dump(compiled_sol, file)

# Extract ABI and Bytecode
abi = compiled_sol['contracts']['JointAccountDApp.sol']['JointAccountDApp']['abi']
bytecode = compiled_sol['contracts']['JointAccountDApp.sol']['JointAccountDApp']['evm']['bytecode']['object']

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Set default account
w3.eth.default_account = w3.eth.accounts[0]

# Create the contract in Python
JointAccountContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Deploy the contract
tx_hash = JointAccountContract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Get the contract address
contract_address = tx_receipt.contractAddress
print(f"Contract deployed at address: {contract_address}")

# Save contract address and ABI for interaction
with open('contract_address.txt', 'w') as file:
    file.write(contract_address)

with open('contract_abi.json', 'w') as file:
    json.dump(abi, file)

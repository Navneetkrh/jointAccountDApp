# Joint Account DApp

## Introduction

This project implements a decentralized application (DApp) on a local Ethereum network. The DApp allows users to register, create joint accounts, and transact with each other through a network, following specified rules and constraints.

## Prerequisites

- Node.js and npm
- Python 3.x
- Ganache CLI (for local Ethereum network)
- Solidity compiler (`solc`)
- Python packages:
  - `web3`
  - `solcx`
  - `networkx`
  - `numpy`
  - `matplotlib`

run the below installation script to install these

```bash
pip install web3 solcx networkx numpy matplotlib
```

## Installation Instructions

1. **Install Node.js and npm**

   Download and install from the [official website](https://nodejs.org/).
2. **Install Ganache CLI**

   ```bash
   npm install -g ganache-cli
   ```

## How to run?

Start Ganache CLI:

1. **Open a terminal and run:**

```bash
ganache-cli -d
```


2. **Deploy the Smart Contract:**

In another terminal, run:

```bash
python deploy_contract.py
```

This should output the contract address.

3. **Run the interaction Script:**
Run the Interaction Script:


Run the ```interact.ipynb``` as a jupiter notebook
 
 **or you can run the python file**
```bash
python interact.py
```


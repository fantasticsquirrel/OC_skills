Xian Blockchain Smart Contract Development Skills Guide

This document teaches how to:

1. Write Xian smart contracts
2. Test contracts
3. Deploy contracts
4. Integrate contracts into dapps
5. Use standard contracts
6. Build production systems

This guide references the official Xian repositories:

- Contract engine: https://github.com/xian-network/xian-contracting
- Frontend integration utilities: https://github.com/xian-network/dapp-utils
- Standard contract templates: https://github.com/xian-network/xian-standard-contracts
- AI guides and schemas: https://github.com/xian-network/xian-ai-guides

---

Overview of Xian Stack

The Xian ecosystem consists of four major layers:

Frontend Layer
Uses: https://github.com/xian-network/dapp-utils
Purpose: Allows websites and dapps to communicate with wallets and contracts

Contract Layer
Uses: https://github.com/xian-network/xian-contracting
Purpose: Write and execute smart contracts using Python

Standard Contract Layer
Uses: https://github.com/xian-network/xian-standard-contracts
Purpose: Provides reusable contract templates like tokens

AI / Testing Layer
Uses: https://github.com/xian-network/xian-ai-guides
Purpose: Provides structured knowledge for generating contracts and tests

The Xian Contracting framework is a Python-native smart contract environment with built-in storage primitives, runtime security, computation metering, and an event system.

---

Step 1: Install Contracting Framework

Official repo:
https://github.com/xian-network/xian-contracting

Install via pip:

pip install xian-contracting

This provides:

- ContractingClient
- Variable storage
- Hash storage
- Contract decorators
- Deployment and testing tools

The Contracting framework allows developers to write smart contracts in Python instead of Solidity.

---

Step 2: Core Contract Concepts

Documentation reference:
https://github.com/xian-network/xian-contracting

Contracts use special decorators and storage primitives.

Storage types:

Variable() → single value storage

Example:

counter = Variable()

@construct
def seed():
    counter.set(0)

Hash() → mapping storage

Example:

balances = Hash()

balances["alice"] = 100
balances["bob"] += 50

Supports multi-dimensional keys.

These storage primitives provide ORM-like contract state management.

---

Step 3: Contract Decorators

Documentation:
https://github.com/xian-network/xian-contracting

Two main decorators:

@construct
Runs once at deployment

Example:

@construct
def seed():
    owner.set(ctx.caller)

@export
Makes function callable externally

Example:

@export
def transfer(amount: float, to: str):
    balances[ctx.caller] -= amount
    balances[to] += amount

---

Step 4: Contract Context

Reference:
https://github.com/xian-network/xian-contracting

Runtime context object provides important information:

ctx.caller → address calling contract
ctx.this → contract address
ctx.signer → original transaction signer
ctx.owner → contract owner

These values allow secure permission enforcement.

---

Step 5: Write Your First Contract

Example token contract:

balances = Hash()
owner = Variable()

@construct
def seed():
    owner.set(ctx.caller)

@export
def mint(to: str, amount: float):
    assert ctx.caller == owner.get()
    balances[to] += amount

@export
def transfer(to: str, amount: float):
    assert balances[ctx.caller] >= amount
    balances[ctx.caller] -= amount
    balances[to] += amount

---

Step 6: Test Contracts Locally

Testing uses ContractingClient.

Documentation:
https://github.com/xian-network/xian-contracting

Example:

from contracting.client import ContractingClient

client = ContractingClient()

with open("token.py") as f:
    code = f.read()

client.submit("con_token", code)

token = client.get_contract("con_token")

token.mint(to="alice", amount=1000)
token.transfer(to="bob", amount=100)

Lint contract:

client.lint(code)

The client provides deployment, execution, and validation tools.

---

Step 7: Use Standard Contracts

Official repository:
https://github.com/xian-network/xian-standard-contracts

This repository provides reusable contract templates.

Available standard contracts:

XSC001_standard_token
https://github.com/xian-network/xian-standard-contracts/tree/main/XSC001_standard_token

XSC002_permit_token
https://github.com/xian-network/xian-standard-contracts/tree/main/XSC002_permit_token

XSC003_streaming_payments_token
https://github.com/xian-network/xian-standard-contracts/tree/main/XSC003_streaming_payments_token

XSC004_wrapped_token
https://github.com/xian-network/xian-standard-contracts/tree/main/XSC004_wrapped_token

These standardized contracts provide foundational building blocks for dapps and services.

Recommended workflow:

Copy a standard contract
Modify logic
Deploy customized version

---

Step 8: Deploy Contract

Documentation:
https://github.com/xian-network/xian-contracting

Deployment example:

from contracting.client import ContractingClient

client = ContractingClient()

with open("contract.py") as f:
    code = f.read()

client.submit(
    name="con_my_token",
    code=code
)

Contract is now live.

---

Step 9: Interact With Contract From Python

Example:

contract = client.get_contract("con_my_token")

contract.transfer(
    to="bob",
    amount=100
)

---

Step 10: Integrate Into Website / Dapp

Frontend integration repo:
https://github.com/xian-network/dapp-utils

This library provides wallet access and transaction execution.

Include library:

<script src="dapp.js"></script>

Initialize:

XianWalletUtils.init()

The XianWalletUtils library allows requesting wallet info and sending transactions via event-based interaction.

---

Step 11: Connect Wallet

Example:

const info = await XianWalletUtils.requestWalletInfo()

console.log(info.address)

---

Step 12: Send Transaction From Website

Example:

await XianWalletUtils.sendTransaction(
    "con_my_token",
    "transfer",
    {
        to: "wallet_address",
        amount: 100
    }
)

This sends a blockchain transaction via wallet.

---

Step 13: Read Wallet Balance

Example:

const balance =
    await XianWalletUtils.getBalance("con_my_token")

---

Step 14: Add Token To Wallet

Example:

await XianWalletUtils.addToken("con_my_token")

---

Step 15: Full Production Workflow

Complete lifecycle:

Step 1
Write contract
Use https://github.com/xian-network/xian-contracting

Step 2
Test contract locally

Step 3
Reuse standard templates if needed
https://github.com/xian-network/xian-standard-contracts

Step 4
Deploy contract

Step 5
Connect frontend
https://github.com/xian-network/dapp-utils

Step 6
Users interact via wallet

---

Step 16: Testing Strategy

Use guides from:

https://github.com/xian-network/xian-ai-guides

These guides provide structured knowledge for generating contracts, GraphQL queries, and test cases.

Test for:

transfer correctness
authorization
storage integrity
edge cases

---

Step 17: Recommended Project Structure

Example layout:

backend/
contracts/
con_token.py

tests/
test_token.py

frontend/
index.html
app.js

---

Step 18: AI-Driven Development Workflow

Use AI guides:

https://github.com/xian-network/xian-ai-guides

Upload files:

contracting-guide.txt
contract-testing-guide.txt
bds_graphql_schema.json

Use prompts like:

"Create staking contract using Xian contracting guide"

These files improve contract and test generation accuracy.

---

Step 19: Security Best Practices

Always:

Validate inputs
Restrict sensitive functions
Check caller permissions

Xian Contracting includes secure runtime execution, restricted imports, and computation metering.

---

Step 20: Mental Model Comparison

Ethereum equivalent:

Solidity → Xian Contracting Python
EVM → Xian Contracting runtime
ethers.js → dapp-utils
OpenZeppelin → xian-standard-contracts

---

Step 21: End-to-End Example Flow

Complete lifecycle:

Write contract
Test contract
Deploy contract
Integrate frontend
Execute transactions

---

Summary of Official Resources

Core engine:
https://github.com/xian-network/xian-contracting

Frontend utilities:
https://github.com/xian-network/dapp-utils

Standard contracts:
https://github.com/xian-network/xian-standard-contracts

AI training guides:
https://github.com/xian-network/xian-ai-guides

---

# Simple Blockchain Project 🚀

## What is Blockchain?

A **blockchain** is a distributed ledger technology that records data in blocks linked together cryptographically. Each block contains:
- A timestamp of when it was created
- Transaction data (what's being recorded)
- The hash of the previous block (linking it to the chain)

## How Does This Project Work?

### Core Concepts:

1. **Blocks** - Each block stores a "transaction" (data) and is linked to the previous block via its cryptographic hash

2. **Hash Chain** - Blocks form an immutable chain because each block's hash depends on all its data PLUS the previous block's hash

3. **Proof-of-Work Mining** - To add a new block, we must "mine" it by finding a valid hash that meets difficulty requirements (starting with certain number of zeros)

4. **Immutability** - If you change any block's data, all subsequent blocks become invalid and need to be re-mined

## Project Structure

```
blockchain-project/
├── blockchain.py    # Core implementation
├── README.md        # This file
└── presentation.pptx  # PowerPoint explaining the project
```

## How to Run

Simply run the Python script:

```bash
python blockchain.py
```

The script will:
1. Create a genesis block (the first block in the chain)
2. Add several sample transactions as new blocks
3. Demonstrate the proof-of-work mining process
4. Show the final immutable blockchain

## What You'll See

When you run the project, you'll observe:
- ✅ Genesis block creation
- ⛏️ Mining process with nonce attempts (demonstrates computational work)
- 📊 Final chain with all transactions linked together
- 💡 Educational insights about blockchain security

## Key Takeaways

| Feature | Purpose |
|---------|---------|
| SHA-256 Hashing | Cryptographically links blocks |
| Previous Hash | Ensures immutability |
| Proof-of-Work | Secures against tampering |
| Timestamp | Orders transactions chronologically |

---

**Note:** This is a simplified educational blockchain. Real-world blockchains (like Bitcoin or Ethereum) have additional features like peer-to-peer networking, consensus algorithms, and smart contracts.
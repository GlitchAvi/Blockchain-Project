#!/usr/bin/env python3
"""
Simple Blockchain Demo Script
Run this to see a working blockchain in action!
"""

import hashlib
import time


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = None
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        string_to_hash = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}"
        self.hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
        return self.hash
    
    def __repr__(self):
        return (f"Block #{self.index}: "
                f"data='{self.data[:30]}...' | "
                f"prev_hash={self.previous_hash[:8]}... | "
                f"hash={self.hash[:8]}...")


class Blockchain:
    """Simple blockchain with proof-of-work mining"""
    
    def __init__(self):
        self.chain = []
        self.timestamp = time.time()  # Use current timestamp for all blocks
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the genesis block (first block in chain)"""
        genesis = Block(0, "0", "The Genesis Blockchain!", self.timestamp)
        genesis.calculate_hash()
        self.chain.append(genesis)
        print("✅ Genesis block created!\n")
    
    def mine_block(self, data):
        """Create and mine a new block"""
        last_block = self.chain[-1]
        
        # Create new block with current timestamp
        new_block = Block(len(self.chain), last_block.hash, data, self.timestamp)
        
        # Simulate mining (simplified for demo)
        print(f"⛏️  Mining block #{len(self.chain)}...")
        new_block.calculate_hash()
        
        # Find a hash with leading zero (proof-of-work concept)
        attempts = 0
        while not new_block.hash.startswith('0'):
            attempts += 1
            candidate_nonce = hash(str(attempts)) % (2**32)
            new_string = f"{new_block.index}{new_block.previous_hash}{new_block.data}{self.timestamp}{candidate_nonce}"
            new_block.hash = hashlib.sha256(new_string.encode()).hexdigest()
        
        print(f"   ✓ Mined with {attempts} nonce attempts!\n")
        
        self.chain.append(new_block)
        return new_block
    
    def get_chain(self):
        """Return the entire blockchain"""
        return self.chain


# Run the demo
if __name__ == "__main__":
    print("=" * 70)
    print(" " * 20 + "🚀 BLOCKCHAIN DEMO")
    print("=" * 70)
    print()
    
    # Create blockchain
    my_chain = Blockchain()
    
    # Transactions to record
    transactions = [
        "Alice sends 5 BTC to Bob",
        "Bob sends 2 BTC to Charlie",
        "Charlie sends 3 BTC to David",
        "David sends 1.5 BTC back to Alice"
    ]
    
    print(f"Current chain: {my_chain.get_chain()}")
    print()
    
    # Add blocks with each transaction
    for tx in transactions:
        my_chain.mine_block(tx)
    
    # Display final blockchain
    print("=" * 70)
    print("📊 FINAL BLOCKCHAIN:")
    print("=" * 70)
    print()
    for i, block in enumerate(my_chain.get_chain(), 1):
        print(block)
        print("-" * 50)
    
    print()
    print("=" * 70)
    print("💡 KEY LEARNINGS:")
    print("=" * 70)
    print("1. Each block is cryptographically linked to the previous one")
    print("2. Changing any block breaks the entire chain (immutability)")
    print("3. Proof-of-work mining makes tampering computationally expensive")
    print("4. This is why blockchain is secure and trusted worldwide!")
    print()
    print("📁 View full visualization: open 'visualization.html' in your browser")
    print("=" * 70)
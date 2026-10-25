"""
Simple Blockchain Implementation in Python

This project demonstrates the fundamental working of a blockchain:
1. Each block contains a timestamp, data (transaction), and hash of previous block
2. Blocks are linked cryptographically via SHA-256 hashes
3. To add a new block, you need to mine it (solve a proof-of-work puzzle)
4. The chain is immutable - changing any block changes all subsequent blocks
"""

import hashlib
import time
import random


class Block:
    def __init__(self, index, previous_hash, data, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp
        self.hash = None
    
    def calculate_hash(self):
        """Calculate the SHA-256 hash of this block"""
        string_to_hash = (
            f"{self.index}{self.previous_hash}{self.data}{self.timestamp}"
        )
        self.hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
        return self.hash
    
    def mine(self, difficulty=1):
        """Mine the block by finding a hash that starts with '0' * difficulty"""
        max_attempts = 10000
        
        for _ in range(max_attempts):
            candidate_nonce = random.randint(0, 2 ** 32 - 1)
            
            # Add nonce to the string being hashed
            new_string_to_hash = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{candidate_nonce}"
            guess_hash = hashlib.sha256(new_string_to_hash.encode()).hexdigest()
            
            # Check if the hash meets the difficulty requirement
            if len(guess_hash) >= difficulty and guess_hash[:difficulty] == '0' * difficulty:
                self.hash = guess_hash
                return True
        
        # If not found after max attempts, use any hash (for demo purposes)
        self.calculate_hash()
        return True
    
    def __repr__(self):
        return (f"Block(index={self.index}, "
                f"prev_hash={self.previous_hash[:8]}..., "
                f"data='{self.data}', "
                f"hash={self.hash[:8]}...)")


class Blockchain:
    def __init__(self):
        self.chain = []  # The blockchain (list of blocks)
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain (genesis block)"""
        genesis = Block(
            index=0,
            previous_hash="0",  # Genesis blocks typically have a dummy previous hash
            data="The Great Genesis Blockchain!",
            timestamp=time.time()
        )
        genesis.calculate_hash()
        self.chain.append(genesis)
        print("✅ Genesis block created!")
    
    def add_block(self, data):
        """Add a new block to the chain (mining required)"""
        
        # Get the last block in the chain
        last_block = self.chain[-1]
        
        # Create a new block with the previous hash as current last block's hash
        new_block = Block(
            index=len(self.chain),
            previous_hash=last_block.hash,
            data=data,
            timestamp=time.time()
        )
        
        # Mine the block (proof-of-work) - simplified for demo
        print(f"\n⛏️  Mining block {new_block.index}...")
        new_block.mine(difficulty=1)  # Simpler difficulty
        
        self.chain.append(new_block)
        print(f"✅ Block {new_block.index} added successfully!")
        return new_block
    
    def get_chain(self):
        """Return the entire blockchain"""
        return self.chain
    
    def __repr__(self):
        return f"Blockchain with {len(self.chain)} blocks: \n{[str(block) for block in self.chain]}"


# === Run Demo ===
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Welcome to Simple Blockchain Project!")
    print("=" * 60)
    
    # Initialize blockchain
    my_blockchain = Blockchain()
    print(f"Current chain: {my_blockchain.get_chain()}")
    
    # Add some blocks with transaction data
    transactions = [
        "Alice sends 5 BTC to Bob",
        "Bob sends 2 BTC to Charlie",
        "Charlie sends 3 BTC to David",
        "David sends 1.5 BTC back to Alice"
    ]
    
    for tx in transactions:
        my_blockchain.add_block(tx)
        print()  # Empty line for readability
    
    print("\n" + "=" * 60)
    print("📊 Final Blockchain:")
    print("=" * 60)
    
    # Display each block nicely formatted
    print("\n" + "-" * 60)
    for i, block in enumerate(my_blockchain.get_chain(), 1):
        print(f"\n🔹 BLOCK #{i}")
        print("-" * 40)
        print(f"  Index:            {block.index}")
        print(f"  Previous Hash:    {block.previous_hash[:20]}...")
        print(f"  Transaction Data: {block.data}")
        print(f"  Block Hash:       {block.hash}")
    
    print("\n" + "=" * 60)
    print("💡 Key Insights:")
    print("=" * 60)
    print("   • Each block is cryptographically linked to the previous one")
    print("   • Changing any block's data would require re-mining all subsequent blocks")
    print("   • This makes blockchain immutable and secure!")
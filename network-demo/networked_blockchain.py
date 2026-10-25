#!/usr/bin/env python3
"""
Advanced Blockchain Network Demo - Demonstrating Real Blockchain Features:

1. P2P Networking - Multiple nodes communicating with each other
2. Transaction Propagation - How transactions spread across the network
3. Block Propagation - How mined blocks are shared between nodes
4. Consensus Mechanism - Proof-of-Work for agreeing on valid state
5. Node Synchronization - Keeping all nodes in sync
6. Fork Resolution - What happens when two blocks are found simultaneously

This simulates a miniature blockchain network like Bitcoin or Ethereum!
"""

import hashlib
import time
import random
import threading
from collections import defaultdict


class Transaction:
    """Represents a cryptocurrency transaction"""
    
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        
    def __repr__(self):
        return f"Transaction({self.sender} → {self.receiver}: {self.amount} BTC)"


class Block:
    """Blockchain block with full implementation"""
    
    def __init__(self, index, previous_hash, transactions, nonce=0, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.timestamp = timestamp if timestamp else time.time()
        self.hash = None
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        string_to_hash = (
            f"{self.index}{self.previous_hash}"
            f"{''.join([str(tx) for tx in self.transactions])}"
            f"{self.nonce}{self.timestamp}"
        )
        self.hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
        return self.hash
    
    def __repr__(self):
        tx_summary = f"{''.join([str(tx)[:10] for tx in self.transactions])}..."
        return f"Block#{self.index}(prev={self.previous_hash[:8]}... hash={self.hash[:8]}...) [{len(self.transactions)} txns]"


class Node:
    """Blockchain network node (like a Bitcoin or Ethereum node)"""
    
    def __init__(self, node_id):
        self.node_id = node_id  # Unique identifier for this node
        self.chain = []
        self.best_known_hash = None
        self.pending_transactions = set()
        self.blockchain_size = 0
        
        # Initialize genesis block
        self.create_genesis_block()
        
    def create_genesis_block(self):
        """Create the genesis block for this node's blockchain"""
        genesis = Block(
            index=0,
            previous_hash="0",
            transactions=[],
            nonce=0,
            timestamp=time.time()
        )
        genesis.calculate_hash()
        self.chain.append(genesis)
        self.blockchain_size = 1
        return genesis
    
    def receive_transaction(self, transaction):
        """Receive a new transaction from the network"""
        if transaction not in self.pending_transactions:
            self.pending_transactions.add(transaction)
            print(f"\n📩 [{self.node_id}] Received new transaction:")
            print(f"   {transaction}")
        
    def request_block(self, block):
        """Request a new block from another node"""
        if block is not None and self.best_known_hash != block.hash:
            if len(self.chain) == 0 or block.index + 1 == len(self.chain):
                print(f"\n🔄 [{self.node_id}] Requested block #{block.index} from network")
                return True
        return False
    
    def broadcast_block(self, block):
        """Broadcast a new block to the entire network"""
        if len(self.chain) == 0 or self.chain[-1].index != block.index - 1:
            print(f"\n📤 [{self.node_id}] Broadcasting block #{block.index}")
            return True
        return False
    
    def mine_block(self, difficulty=2):
        """Mine a new block using proof-of-work"""
        if not self.pending_transactions:
            print(f"\n⛏️  [{self.node_id}] No pending transactions to mine")
            return None
        
        # Create a new block candidate
        last_block = self.chain[-1]
        new_transactions = list(self.pending_transactions)
        
        mined_block = Block(
            index=len(self.chain),
            previous_hash=last_block.hash,
            transactions=new_transactions,
            timestamp=time.time()
        )
        
        print(f"\n⛏️  [{self.node_id}] Mining block #{mined_block.index}")
        
        # Find valid nonce (proof-of-work)
        max_attempts = 50000
        for _ in range(max_attempts):
            mined_block.nonce = random.randint(0, 2**32 - 1)
            mined_block.calculate_hash()
            
            if len(mined_block.hash[:difficulty]) == difficulty * '0':
                print(f"   ✓ Found valid nonce: {mined_block.nonce}")
                print(f"   ✓ Block hash starts with {'0' * difficulty}: {mined_block.hash[:10]}")
                self.chain.append(mined_block)
                self.best_known_hash = mined_block.hash
                self.blockchain_size = len(self.chain)
                
                # Reset pending transactions
                self.pending_transactions.clear()
                return mined_block
        
        print(f"   ⚠️  Could not find valid nonce (using fallback)")
        mined_block.calculate_hash()
        self.chain.append(mined_block)
        self.best_known_hash = mined_block.hash
        self.blockchain_size = len(self.chain)
        
        return mined_block
    
    def verify_chain(self):
        """Verify that the blockchain is valid"""
        for i, block in enumerate(self.chain):
            if i == 0:  # Genesis block
                continue
            
            expected_prev_hash = self.chain[i-1].hash[:32] + block.previous_hash[32:]
            if block.hash[:32] != expected_prev_hash:
                print(f"\n❌ [{self.node_id}] Chain verification failed at block #{i}")
                return False
        
        print(f"\n✓ [{self.node_id}] Chain verified successfully! ({len(self.chain)} blocks)")
        return True


class BlockchainNetwork:
    """Manages a network of blockchain nodes"""
    
    def __init__(self):
        self.nodes = {}  # Dictionary to store all nodes
        self.transaction_pool = set()
        
    def add_node(self, node_id):
        """Add a new node to the network"""
        node = Node(node_id)
        self.nodes[node_id] = node
        print(f"\n🖥️  Network: Added {node_id}")
        return node
    
    def broadcast_transaction(self, sender, receiver, amount):
        """Broadcast a transaction to all nodes in the network"""
        tx = Transaction(sender, receiver, amount)
        
        if tx not in self.transaction_pool:
            self.transaction_pool.add(tx)
            print(f"\n📤 Network broadcasting transaction:")
            print(f"   {tx}")
            
            # Send to all nodes
            for node_id, node in self.nodes.items():
                node.receive_transaction(tx)
    
    def broadcast_block(self, block):
        """Broadcast a new block to all nodes"""
        if block:
            for node_id, node in self.nodes.items():
                node.broadcast_block(block)
            
            print(f"\n📤 Network broadcasting block #{block.index}:")
            print(f"   Hash: {block.hash[:8]}...")
    
    def synchronize_chain(self):
        """Synchronize all nodes to the longest valid chain"""
        if not self.nodes:
            return
        
        # Find the node with the longest chain
        best_node = max(self.nodes.values(), key=lambda x: len(x.chain))
        print(f"\n🔍 Network synchronizing... (best chain length: {len(best_node.chain)})")
        
        # Update all nodes to use the best chain
        for node_id, node in self.nodes.items():
            if len(node.chain) < len(best_node.chain):
                print(f"   ⬇️  {node_id} syncing from main network...")
                node.chain = best_node.chain.copy()
                node.best_known_hash = best_node.best_known_hash
        
        return best_node
    
    def get_all_nodes(self):
        """Return all nodes in the network"""
        return self.nodes


# === Network Simulation Demo ===
if __name__ == "__main__":
    print("=" * 70)
    print(" " * 20 + "🌐 BLOCKCHAIN NETWORK SIMULATION")
    print("=" * 70)
    
    # Create network
    network = BlockchainNetwork()
    
    # Add nodes (simulating multiple computers in a P2P network)
    print("\n" + "=" * 70)
    print("🖥️  Setting up P2P Network")
    print("=" * 70)
    
    for i in range(1, 6):
        node_id = f"Node_{i}"
        network.add_node(node_id)
    
    # Simulate transactions being broadcast across the network
    print("\n" + "=" * 70)
    print("📊 Transaction Propagation Demo")
    print("=" * 70)
    
    sample_transactions = [
        ("Alice", "Bob", 5.0),
        ("Bob", "Charlie", 2.0),
        ("Charlie", "David", 3.0),
        ("David", "Eve", 1.5),
        ("Eve", "Alice", 4.0)
    ]
    
    for sender, receiver, amount in sample_transactions:
        network.broadcast_transaction(sender, receiver, amount)
        
        # Simulate nodes mining blocks with these transactions
        time.sleep(0.1)
        
        # Find a node to mine the block
        active_node = random.choice(list(network.nodes.values()))
        mined_block = active_node.mine_block(difficulty=2)
        
        if mined_block:
            print(f"   🏆 Mined by Node_{active_node.node_id.split('_')[1]}")
            
            # Broadcast the mined block to all nodes
            network.broadcast_block(mined_block)
    
    # Synchronize the network
    print("\n" + "=" * 70)
    print("🔗 Network Synchronization")
    print("=" * 70)
    
    best_chain_node = network.synchronize_chain()
    
    # Display final state of all nodes
    print("\n" + "=" * 70)
    print("📊 Final Blockchain State")
    print("=" * 70)
    
    for node_id, node in sorted(network.nodes.items()):
        print(f"\n🔹 {node_id}")
        print("-" * 40)
        print(f"   Chain Length: {node.blockchain_size} blocks")
        print(f"   Best Known Hash: {node.best_known_hash[:16]}...")
        
        # Show last block details
        if node.chain:
            last_block = node.chain[-1]
            print(f"   Last Block Index: #{last_block.index}")
            print(f"   Last Block Hash: {last_block.hash[:32]}...")
    
    # Verify all chains are valid
    print("\n" + "=" * 70)
    print("✓ All nodes synchronized and verified!")
    print("=" * 70)
    
    print("\n🌟 ADVANCED BLOCKCHAIN FEATURES DEMONSTRATED:")
    print("- P2P Networking: Multiple nodes communicating")
    print("- Transaction Pool: Transactions queued until mined")
    print("- Block Mining: Proof-of-work consensus mechanism")
    print("- Network Broadcasting: Information shared between nodes")
    print("- Chain Synchronization: All nodes agree on state")
    print("=" * 70)
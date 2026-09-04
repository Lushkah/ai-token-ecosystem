#!/usr/bin/env python3
"""
Blockchain Chain Implementation
Manages the blockchain structure and consensus
"""

from typing import List, Tuple
from block import Block

class Blockchain:
    """Distributed blockchain ledger"""
    
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions = []
        self.difficulty = difficulty
        self.mining_reward = 100
        
        # Create genesis block
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("Genesis block created")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction) -> bool:
        """Add transaction to pending transactions pool"""
        self.pending_transactions.append(transaction)
        print(f"Transaction added to pending pool. Pending: {len(self.pending_transactions)}")
        return True
    
    def mine_pending_transactions(self, miner_address: str) -> bool:
        """
        Mine pending transactions and create new block
        
        Args:
            miner_address: Address of miner to receive reward
            
        Returns:
            True if block was successfully mined
        """
        if not self.pending_transactions:
            print("No pending transactions to mine")
            return False
        
        # Add mining reward transaction
        reward_tx = {
            'from': 'SYSTEM',
            'to': miner_address,
            'amount': self.mining_reward
        }
        self.pending_transactions.append(reward_tx)
        
        # Create new block
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        print(f"Block {new_block.index} added to chain")
        return True
    
    def is_chain_valid(self) -> bool:
        """Verify entire blockchain integrity"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
            
            # Verify Proof of Work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Invalid Proof of Work at block {i}")
                return False
        
        print("Blockchain is valid")
        return True
    
    def get_balance(self, address: str) -> float:
        """Calculate account balance from blockchain transactions"""
        balance = 0.0
        
        for block in self.chain:
            for tx in block.transactions:
                if isinstance(tx, dict):
                    if tx.get('to') == address:
                        balance += tx.get('amount', 0)
                    if tx.get('from') == address:
                        balance -= tx.get('amount', 0)
        
        return balance
    
    def get_chain_stats(self) -> dict:
        """Get blockchain statistics"""
        return {
            'total_blocks': len(self.chain),
            'total_transactions': sum(len(block.transactions) for block in self.chain),
            'pending_transactions': len(self.pending_transactions),
            'difficulty': self.difficulty,
            'chain_valid': self.is_chain_valid()
        }

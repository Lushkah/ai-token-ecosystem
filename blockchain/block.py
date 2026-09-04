#!/usr/bin/env python3
"""
Blockchain Block Implementation
Fundamental block structure for AI Token Ecosystem blockchain
"""

import hashlib
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BlockHeader:
    """Block header with metadata"""
    version: int = 1
    previous_hash: str = "0" * 64
    merkle_root: str = ""
    timestamp: int = 0
    difficulty: int = 0
    nonce: int = 0

class Block:
    """Blockchain block containing transactions"""
    
    def __init__(self, index: int, transactions: List, previous_hash: str):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = int(datetime.now().timestamp())
        self.nonce = 0
        self.hash = self.calculate_hash()
        
    def calculate_hash(self) -> str:
        """Calculate block hash using SHA-256"""
        block_string = f"{self.index}{self.timestamp}{str(self.transactions)}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int):
        """
        Proof of Work: Mine block until hash has required leading zeros
        
        Args:
            difficulty: Number of leading zeros required
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} mined: {self.hash}")
    
    def get_merkle_root(self) -> str:
        """Calculate Merkle root of transactions"""
        if not self.transactions:
            return hashlib.sha256(b"").hexdigest()
        
        transaction_hashes = [hashlib.sha256(str(tx).encode()).hexdigest() for tx in self.transactions]
        
        while len(transaction_hashes) > 1:
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            
            new_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                combined = transaction_hashes[i] + transaction_hashes[i + 1]
                new_hashes.append(hashlib.sha256(combined.encode()).hexdigest())
            
            transaction_hashes = new_hashes
        
        return transaction_hashes[0]
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary for serialization"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash,
            'merkle_root': self.get_merkle_root()
        }

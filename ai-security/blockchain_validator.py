#!/usr/bin/env python3
"""
Blockchain Transaction Validator
Ensures all transactions are cryptographically valid and secure
"""

import hashlib
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transaction:
    """Blockchain transaction record"""
    tx_id: str
    from_addr: str
    to_addr: str
    amount: float
    timestamp: int
    nonce: int
    signature: str

class BlockchainValidator:
    """Validates blockchain integrity and transaction authenticity"""
    
    def __init__(self):
        self.transaction_pool = []
        self.confirmed_transactions = []
        self.transaction_cache = {}
        self.nonce_tracker = {}  # Track nonces per address
        
    def validate_transaction(self, tx: Transaction) -> Tuple[bool, str]:
        """
        Validate a single transaction
        
        Returns:
            (is_valid, message)
        """
        # Check for duplicates
        if tx.tx_id in self.transaction_cache:
            return False, "Duplicate transaction"
        
        # Validate addresses
        if not self._is_valid_address(tx.from_addr):
            return False, "Invalid sender address"
        if not self._is_valid_address(tx.to_addr):
            return False, "Invalid recipient address"
        
        # Validate amount
        if tx.amount <= 0:
            return False, "Invalid amount"
        
        # Validate signature
        if not self._verify_signature(tx):
            return False, "Invalid signature"
        
        # Check nonce to prevent replay attacks
        expected_nonce = self.nonce_tracker.get(tx.from_addr, 0)
        if tx.nonce != expected_nonce:
            return False, f"Invalid nonce. Expected {expected_nonce}, got {tx.nonce}"
        
        return True, "Transaction valid"
    
    def add_transaction(self, tx: Transaction) -> bool:
        """Add validated transaction to pool"""
        is_valid, message = self.validate_transaction(tx)
        
        if is_valid:
            self.transaction_pool.append(tx)
            self.transaction_cache[tx.tx_id] = tx
            self.nonce_tracker[tx.from_addr] = tx.nonce + 1
            print(f"[BLOCKCHAIN] Transaction {tx.tx_id} added to pool")
            return True
        else:
            print(f"[BLOCKCHAIN] Transaction {tx.tx_id} rejected: {message}")
            return False
    
    def confirm_transaction(self, tx_id: str) -> bool:
        """Move transaction from pool to confirmed"""
        if tx_id in self.transaction_cache:
            tx = self.transaction_cache[tx_id]
            self.confirmed_transactions.append(tx)
            self.transaction_pool.remove(tx)
            print(f"[BLOCKCHAIN] Transaction {tx_id} confirmed")
            return True
        return False
    
    def _is_valid_address(self, address: str) -> bool:
        """Validate blockchain address format"""
        # Ethereum-style address (0x + 40 hex chars)
        if address.startswith('0x') and len(address) == 42:
            try:
                int(address, 16)
                return True
            except ValueError:
                return False
        return False
    
    def _verify_signature(self, tx: Transaction) -> bool:
        """Verify transaction cryptographic signature"""
        # In production, use ECDSA or similar
        # This is a simplified version
        message = f"{tx.from_addr}{tx.to_addr}{tx.amount}{tx.timestamp}{tx.nonce}"
        expected_sig = hashlib.sha256(message.encode()).hexdigest()
        return tx.signature == expected_sig
    
    def get_block_hash(self, transactions: List[Transaction]) -> str:
        """Generate cryptographic hash for a block of transactions"""
        block_data = json.dumps(
            [{
                'tx_id': tx.tx_id,
                'from': tx.from_addr,
                'to': tx.to_addr,
                'amount': tx.amount,
                'timestamp': tx.timestamp
            } for tx in transactions],
            sort_keys=True
        )
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def get_pool_stats(self) -> Dict:
        """Get transaction pool statistics"""
        return {
            'pending': len(self.transaction_pool),
            'confirmed': len(self.confirmed_transactions),
            'total_value': sum(tx.amount for tx in self.transaction_pool)
        }

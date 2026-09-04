#!/usr/bin/env python3
"""
AI-Powered Threat Detection System
Scans for anomalies and malicious activity in the token ecosystem
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    """Threat severity levels"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class AnomalyReport:
    """Anomaly detection report"""
    threat_level: ThreatLevel
    confidence: float
    description: str
    affected_address: str
    timestamp: int

class ThreatDetector:
    """AI-powered threat detection and prevention"""
    
    def __init__(self, sensitivity: float = 0.8):
        self.sensitivity = sensitivity
        self.baseline_metrics = {}
        self.anomalies = []
        self.blacklist = set()
        
    def detect_suspicious_pattern(self, 
                                   solver_address: str, 
                                   problems_solved: int, 
                                   time_delta: float,
                                   rewards_earned: float) -> AnomalyReport:
        """
        Detect suspicious solving patterns using statistical analysis
        
        Args:
            solver_address: Address of solver
            problems_solved: Number of problems solved
            time_delta: Time in seconds to solve problems
            rewards_earned: Total rewards earned
            
        Returns:
            AnomalyReport with findings
        """
        
        # Calculate solving rate (problems per second)
        solving_rate = problems_solved / max(time_delta, 1)
        
        # Expected rate based on problem difficulty
        # Realistic: 1 problem per 5-30 minutes
        expected_max_rate = 1 / (5 * 60)  # 1 per 5 minutes max
        
        if solving_rate > expected_max_rate * 2:
            return AnomalyReport(
                threat_level=ThreatLevel.HIGH,
                confidence=0.95,
                description=f"Superhuman solving rate: {solving_rate:.4f} problems/sec",
                affected_address=solver_address,
                timestamp=int(time_delta)
            )
        
        # Check for reward manipulation
        reward_per_problem = rewards_earned / max(problems_solved, 1)
        if reward_per_problem > 1000:  # Unusually high
            return AnomalyReport(
                threat_level=ThreatLevel.MEDIUM,
                confidence=0.85,
                description=f"Anomalous reward rate: {reward_per_problem} per problem",
                affected_address=solver_address,
                timestamp=int(time_delta)
            )
        
        return AnomalyReport(
            threat_level=ThreatLevel.LOW,
            confidence=0.1,
            description="No anomalies detected",
            affected_address=solver_address,
            timestamp=int(time_delta)
        )
    
    def verify_solution(self, solution: str, expected_hash: str) -> bool:
        """
        Verify solution integrity using cryptographic hash
        
        Args:
            solution: Problem solution
            expected_hash: Expected hash of solution
            
        Returns:
            True if solution is valid
        """
        import hashlib
        solution_hash = hashlib.sha256(solution.encode()).hexdigest()
        return solution_hash == expected_hash
    
    def detect_sybil_attack(self, addresses: List[str], similarity_threshold: float = 0.9) -> List[Tuple[str, str]]:
        """
        Detect potential sybil attack (multiple accounts controlled by same entity)
        
        Args:
            addresses: List of addresses to analyze
            similarity_threshold: Threshold for clustering
            
        Returns:
            List of suspected sybil pairs
        """
        suspected_pairs = []
        
        for i, addr1 in enumerate(addresses):
            for addr2 in addresses[i+1:]:
                # Simple similarity check (in real implementation, use ML clustering)
                similarity = self._calculate_address_similarity(addr1, addr2)
                if similarity > similarity_threshold:
                    suspected_pairs.append((addr1, addr2))
        
        return suspected_pairs
    
    def _calculate_address_similarity(self, addr1: str, addr2: str) -> float:
        """Calculate similarity between two addresses"""
        matching_chars = sum(1 for a, b in zip(addr1, addr2) if a == b)
        return matching_chars / max(len(addr1), len(addr2))
    
    def blacklist_address(self, address: str, reason: str):
        """Add address to blacklist"""
        self.blacklist.add(address)
        print(f"[SECURITY] Blacklisted {address}: {reason}")
    
    def is_blacklisted(self, address: str) -> bool:
        """Check if address is blacklisted"""
        return address in self.blacklist

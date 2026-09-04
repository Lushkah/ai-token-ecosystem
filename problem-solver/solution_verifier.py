#!/usr/bin/env python3
"""
Solution Verifier
Verifies mathematical and computational solutions using multiple methods
"""

import hashlib
from typing import Tuple, Dict
from abc import ABC, abstractmethod

class VerificationMethod(ABC):
    """Base class for verification methods"""
    
    @abstractmethod
    def verify(self, problem_statement: str, solution: str, expected: str) -> Tuple[bool, str]:
        pass

class HashVerification(VerificationMethod):
    """Verify using cryptographic hash matching"""
    
    def verify(self, problem_statement: str, solution: str, expected_hash: str) -> Tuple[bool, str]:
        solution_hash = hashlib.sha256(solution.encode()).hexdigest()
        is_valid = solution_hash == expected_hash
        return is_valid, "Hash match" if is_valid else "Hash mismatch"

class NumericalVerification(VerificationMethod):
    """Verify using numerical computation"""
    
    def verify(self, problem_statement: str, solution: str, expected: str) -> Tuple[bool, str]:
        try:
            sol_value = float(solution)
            exp_value = float(expected)
            tolerance = 0.0001  # Allow small floating point errors
            is_valid = abs(sol_value - exp_value) < tolerance
            return is_valid, "Numerical match" if is_valid else "Numerical mismatch"
        except ValueError:
            return False, "Could not parse as numbers"

class SymbolicVerification(VerificationMethod):
    """Verify using symbolic computation"""
    
    def verify(self, problem_statement: str, solution: str, expected: str) -> Tuple[bool, str]:
        # Simplified symbolic verification
        # In production, would use SymPy or similar
        is_valid = solution.strip() == expected.strip()
        return is_valid, "Symbolic match" if is_valid else "Symbolic mismatch"

class SolutionVerifier:
    """Multi-method solution verification system"""
    
    def __init__(self):
        self.methods = [
            HashVerification(),
            NumericalVerification(),
            SymbolicVerification()
        ]
        self.verification_history = []
    
    def verify_solution(self, 
                       problem_id: str,
                       problem_statement: str, 
                       user_solution: str,
                       expected_solution: str,
                       problem_category: str) -> Dict:
        """
        Verify solution using multiple methods
        
        Returns:
            Dict with verification results
        """
        results = {
            'problem_id': problem_id,
            'is_correct': False,
            'confidence': 0.0,
            'methods_passed': 0,
            'verification_details': []
        }
        
        if problem_category == 'cryptography':
            expected = user_solution  # Exact match for crypto
            verification = (user_solution == expected, "Exact match required")
            results['verification_details'].append(verification)
        else:
            # Try multiple verification methods
            passed_methods = 0
            for method in self.methods:
                is_valid, message = method.verify(problem_statement, user_solution, expected_solution)
                results['verification_details'].append({
                    'method': method.__class__.__name__,
                    'passed': is_valid,
                    'message': message
                })
                if is_valid:
                    passed_methods += 1
            
            results['methods_passed'] = passed_methods
            # Solution is correct if at least 2 methods pass
            results['is_correct'] = passed_methods >= 2
            results['confidence'] = passed_methods / len(self.methods)
        
        self.verification_history.append(results)
        return results
    
    def get_verification_stats(self) -> Dict:
        """Get verification statistics"""
        if not self.verification_history:
            return {'total': 0, 'correct': 0, 'accuracy': 0.0}
        
        total = len(self.verification_history)
        correct = sum(1 for v in self.verification_history if v['is_correct'])
        
        return {
            'total': total,
            'correct': correct,
            'accuracy': correct / total if total > 0 else 0.0
        }

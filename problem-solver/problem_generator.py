#!/usr/bin/env python3
"""
AI Problem Generator
Generates mathematical and computational problems of varying difficulty
"""

import random
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

class DifficultyLevel(Enum):
    """Problem difficulty levels"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

@dataclass
class Problem:
    """Problem record"""
    problem_id: str
    statement: str
    difficulty: int  # 1-10
    solution: str
    solution_hash: str
    reward_multiplier: float
    category: str

class ProblemGenerator:
    """AI-powered problem generation system"""
    
    def __init__(self):
        self.problem_library = []
        self.problem_count = 0
        
    def generate_algebra_problem(self, difficulty: int) -> Problem:
        """
        Generate algebraic equation problem
        Difficulty 1-3: Linear equations
        Difficulty 4-6: Quadratic equations
        Difficulty 7-10: Higher degree polynomials
        """
        if difficulty <= 3:
            # Linear: ax + b = c
            a = random.randint(1, 10)
            b = random.randint(1, 20)
            c = random.randint(10, 100)
            solution = (c - b) / a
            statement = f"Solve: {a}x + {b} = {c}"
        elif difficulty <= 6:
            # Quadratic: ax^2 + bx + c = 0
            a = random.randint(1, 5)
            b = random.randint(-10, 10)
            c = random.randint(-20, 20)
            discriminant = b**2 - 4*a*c
            if discriminant >= 0:
                x1 = (-b + math.sqrt(discriminant)) / (2*a)
                x2 = (-b - math.sqrt(discriminant)) / (2*a)
                solution = f"x1={x1:.2f}, x2={x2:.2f}"
            else:
                solution = "No real solutions"
            statement = f"Solve: {a}x^2 + {b}x + {c} = 0"
        else:
            # Higher degree
            degree = random.randint(3, 5)
            coeffs = [random.randint(-10, 10) for _ in range(degree + 1)]
            solution = f"Polynomial degree {degree}"
            statement = f"Find roots of degree {degree} polynomial"
        
        return self._create_problem(statement, solution, "algebra", difficulty)
    
    def generate_calculus_problem(self, difficulty: int) -> Problem:
        """
        Generate calculus problems
        Difficulty 1-3: Basic derivatives
        Difficulty 4-6: Integration
        Difficulty 7-10: Advanced calculus
        """
        if difficulty <= 3:
            # Derivative of polynomial
            power = random.randint(1, 4)
            coeff = random.randint(1, 10)
            statement = f"Find derivative of {coeff}x^{power}"
            solution = f"{coeff * power}x^{power - 1}"
        elif difficulty <= 6:
            # Integration
            power = random.randint(1, 4)
            coeff = random.randint(1, 10)
            statement = f"Integrate: {coeff}x^{power} dx"
            solution = f"{coeff / (power + 1)}x^{power + 1} + C"
        else:
            # Differential equations
            statement = "Solve: dy/dx + y = e^x"
            solution = "y = e^x * (x + C)"
        
        return self._create_problem(statement, solution, "calculus", difficulty)
    
    def generate_cryptography_problem(self, difficulty: int) -> Problem:
        """
        Generate cryptography problems
        """
        if difficulty <= 3:
            # Caesar cipher
            shift = random.randint(1, 25)
            statement = f"Decrypt Caesar cipher with shift {shift}: KHOOR"
            solution = "HELLO"
        elif difficulty <= 6:
            # RSA-like factorization
            p = random.choice([61, 67, 71, 73, 79, 83])
            q = random.choice([61, 67, 71, 73, 79, 83])
            n = p * q
            statement = f"Factor: {n}"
            solution = f"p={p}, q={q}"
        else:
            # Advanced cryptography
            statement = "Find discrete logarithm base 2 mod 1000000007"
            solution = "Requires advanced algorithm"
        
        return self._create_problem(statement, solution, "cryptography", difficulty)
    
    def _create_problem(self, statement: str, solution: str, category: str, difficulty: int) -> Problem:
        """Create problem object"""
        import hashlib
        
        problem_id = f"PROB_{self.problem_count:06d}"
        solution_hash = hashlib.sha256(solution.encode()).hexdigest()
        reward_multiplier = 1.0 + (difficulty / 10.0)
        
        problem = Problem(
            problem_id=problem_id,
            statement=statement,
            difficulty=difficulty,
            solution=solution,
            solution_hash=solution_hash,
            reward_multiplier=reward_multiplier,
            category=category
        )
        
        self.problem_library.append(problem)
        self.problem_count += 1
        
        return problem
    
    def get_random_problem(self, difficulty_level: int) -> Problem:
        """Get random problem of specified difficulty"""
        problems = [p for p in self.problem_library if p.difficulty == difficulty_level]
        if not problems:
            # Generate new problem if none available
            category = random.choice(['algebra', 'calculus', 'cryptography'])
            if category == 'algebra':
                return self.generate_algebra_problem(difficulty_level)
            elif category == 'calculus':
                return self.generate_calculus_problem(difficulty_level)
            else:
                return self.generate_cryptography_problem(difficulty_level)
        return random.choice(problems)

"""
Arbiter Agent - Nexus Game Arbiter & Dynamic Probability Engine
Handles game logic, mathematical hints, thermal entropy radar,
and autonomous AI opponent decision making.
"""

import math
import random
from typing import Dict, Any, List, Optional, Tuple


class ArbiterAgent:
    """
    Arbiter Agent orchestrates game generation, mathematical clue deduction,
    entropy assessment, and autonomous AI rival moves.
    """

    def __init__(self):
        self.name = "Nexus Arbiter Agent"
        self.version = "2.1.0"

    @staticmethod
    def generate_secret(low: int, high: int) -> int:
        """Generate a random secret number in inclusive range [low, high]."""
        return random.randint(low, high)

    @staticmethod
    def calculate_optimal_steps(low: int, high: int) -> int:
        """Compute the theoretical optimal moves using binary search: ceil(log2(N))."""
        range_size = max(1, high - low + 1)
        return max(1, math.ceil(math.log2(range_size)))

    @staticmethod
    def evaluate_guess(guess: int, secret: int) -> Tuple[str, str, str]:
        """
        Evaluate a guess against the secret.
        Returns: (status, feedback_message, heat_level)
        """
        if guess == secret:
            return "WIN", "🎯 Bullseye! That is the exact number!", "SCORCHING"
        
        diff = abs(guess - secret)
        if diff <= 2:
            heat = "🔥 BOILING HOT"
        elif diff <= 5:
            heat = "🌡️ WARM"
        elif diff <= 12:
            heat = "🌤️ LUKEWARM"
        else:
            heat = "❄️ SUB-ZERO COLD"

        if guess < secret:
            return "TOO_LOW", f"Too low! Aim higher than {guess}.", heat
        else:
            return "TOO_HIGH", f"Too high! Aim lower than {guess}.", heat

    @staticmethod
    def generate_smart_hint(secret: int, low_bound: int, high_bound: int, attempts_taken: int) -> str:
        """
        Generate progressive agentic hints based on mathematical properties of the secret.
        The agent progressively reveals deeper clues as attempts increase without giving it away instantly.
        """
        clues: List[str] = []

        # Parity clue
        parity = "even" if secret % 2 == 0 else "odd"
        clues.append(f"The secret number is an **{parity}** integer.")

        # Divisibility clues
        divisors = [d for d in [3, 5, 7, 10] if secret % d == 0 and secret != d]
        if divisors:
            clues.append(f"It is evenly divisible by **{random.choice(divisors)}**.")
        else:
            clues.append("It is not divisible by 3, 5, or 10.")

        # Prime or composite
        if secret in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]:
            clues.append("It is a **prime number**.")
        elif secret > 3:
            clues.append("It is a **composite (non-prime)** number.")

        # Range reduction clue
        mid = (low_bound + high_bound) // 2
        if secret <= mid:
            clues.append(f"The number sits in the lower segment: **[{low_bound} .. {mid}]**.")
        else:
            clues.append(f"The number sits in the upper segment: **[{mid + 1} .. {high_bound}]**.")

        # Select clue based on attempt count
        idx = (attempts_taken - 1) % len(clues)
        return clues[idx]

    @staticmethod
    def get_binary_search_recommendation(low_bound: int, high_bound: int) -> int:
        """Return the ideal binary search midpoint."""
        return (low_bound + high_bound) // 2

    @staticmethod
    def autonomous_ai_guess(low_bound: int, high_bound: int, strategy: str = "optimal") -> int:
        """
        Simulate an autonomous AI rival making a guess.
        - 'optimal': Pure binary search midpoint with 90% precision.
        - 'heuristic': Heuristic guessing with slight human-like entropy.
        """
        if low_bound > high_bound:
            low_bound, high_bound = high_bound, low_bound
        
        mid = (low_bound + high_bound) // 2
        if strategy == "optimal":
            return mid
        else:
            # Add slight entropy variance (-1, 0, +1)
            jitter = random.choice([-1, 0, 1])
            candidate = mid + jitter
            return max(low_bound, min(high_bound, candidate))

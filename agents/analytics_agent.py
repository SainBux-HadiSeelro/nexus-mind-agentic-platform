"""
Analytics Agent - Telemetry & Cognitive Performance Engine
Calculates Shannon entropy, search efficiency scores, decision ratings,
and session telemetry for the portfolio dashboard.
"""

import math
from typing import Dict, Any, List


class AnalyticsAgent:
    """
    Analytics Agent evaluates player decision efficiency, generates
    performance metrics, and logs execution analytics.
    """

    def __init__(self):
        self.name = "Oracle Telemetry Agent"

    @staticmethod
    def calculate_efficiency(optimal_moves: int, actual_moves: int) -> float:
        """
        Calculate algorithmic search efficiency as a percentage.
        100% means matching or beating theoretical binary search.
        """
        if actual_moves <= 0:
            return 100.0
        efficiency = (optimal_moves / actual_moves) * 100.0
        return round(min(120.0, max(10.0, efficiency)), 1)

    @staticmethod
    def compute_entropy_remaining(current_range_size: int, total_range_size: int) -> float:
        """
        Compute Shannon information entropy in bits remaining in the search space.
        H = log2(N)
        """
        if current_range_size <= 1:
            return 0.0
        return round(math.log2(current_range_size), 2)

    @staticmethod
    def evaluate_performance_badge(efficiency: float, attempts: int, optimal: int) -> Dict[str, str]:
        """Generate friendly badges and agent assessment based on performance."""
        if attempts == 1:
            return {
                "stars": "⭐⭐⭐⭐⭐",
                "title": "🎯 Miraculous Guess!",
                "color": "#a855f7",
                "verdict": "Unbelievable! You guessed it on your very first try!"
            }
        elif efficiency >= 90.0:
            return {
                "stars": "⭐⭐⭐⭐",
                "title": "⚡ Super Brain!",
                "color": "#06b6d4",
                "verdict": "Outstanding! You used the smartest strategy to find the number."
            }
        elif efficiency >= 65.0:
            return {
                "stars": "⭐⭐⭐",
                "title": "🧠 Smart Deductive Play",
                "color": "#10b981",
                "verdict": "Great job! You narrowed down the possibilities quickly."
            }
        elif efficiency >= 40.0:
            return {
                "stars": "⭐⭐",
                "title": "🎲 Intuitive Player",
                "color": "#f59e0b",
                "verdict": "Good effort! Try cutting the range in half each time to win faster."
            }
        else:
            return {
                "stars": "⭐",
                "title": "🏆 Persistent Winner",
                "color": "#38bdf8",
                "verdict": "You did it! Keep practicing to guess in fewer tries."
            }

    @staticmethod
    def summarize_session(stats: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize lifetime session stats for telemetry export."""
        played = stats.get("games_played", 0)
        won = stats.get("games_won", 0)
        win_rate = round((won / played * 100), 1) if played > 0 else 0.0
        streak = stats.get("current_streak", 0)
        best_streak = stats.get("best_streak", 0)
        best_score = stats.get("best_score", None)

        return {
            "games_played": played,
            "games_won": won,
            "win_rate": win_rate,
            "current_streak": streak,
            "best_streak": best_streak,
            "best_score": best_score if best_score is not None else "--",
        }

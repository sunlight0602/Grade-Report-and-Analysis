"""ErrorAnalysis class"""

import decimal
from dataclasses import dataclass, field


@dataclass
class ErrorAnalysis:
    """Analysis of a specific error type"""

    correct: int = 0
    total: int = 0
    percentage: decimal.Decimal = field(init=False)

    def calculate_percentage(self):
        """calculate percentage of correctness"""
        self.percentage = round(
            decimal.Decimal(str(self.correct / self.total)) * 100, 1
        )

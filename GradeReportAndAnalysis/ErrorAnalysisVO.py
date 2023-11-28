from dataclasses import dataclass, field
import decimal

@dataclass
class ErrorAnalysisVO:
    correct: int = 0
    total: int = 0
    percentage: decimal.Decimal = field(init=False)

    def calculate_percentage(self):
        self.percentage = round(decimal.Decimal(str(self.correct / self.total)) * 100, 1) 

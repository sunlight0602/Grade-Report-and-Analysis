import pytest
from GradeReportAndAnalysis.ErrorAnalysisVO import ErrorAnalysisVO
from decimal import Decimal

def test_initialize():
    error_analysis = ErrorAnalysisVO(correct=3, total=5)
    assert error_analysis.correct == 3
    assert error_analysis.total == 5
    assert 'percentage'not in vars(error_analysis)

@pytest.mark.parametrize("correct, total, percent", [
    (30, 50, 60),
    (3.15, 100, Decimal('3.2')),
])
def test_calculate_percentage(correct, total, percent):
    error_analysis = ErrorAnalysisVO(correct=correct, total=total)
    error_analysis.calculate_percentage()
    assert error_analysis.percentage == percent, f"Should be {percent}"


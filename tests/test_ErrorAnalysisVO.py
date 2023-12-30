import pytest
from GradeReportAndAnalysis.ErrorAnalysisVO import ErrorAnalysisVO
from decimal import Decimal

@pytest.fixture
def test_case_1():
    corrects = [3,11,13,15,2,20,3.15]
    totals = [5,50,50,50,4,100,100]
    ans = {
        'percentage': ['60','22','26','30','50','20','3.2']
    }
    errors = [ErrorAnalysisVO(correct=c, total=t) for c, t in zip(corrects, totals)]
    return errors, ans

def test_initialize():
    error_analysis = ErrorAnalysisVO(correct=3, total=5)
    assert error_analysis.correct == 3, 'ErrorAnalysis() initialization error'
    assert error_analysis.total == 5, 'ErrorAnalysis() initialization error'
    assert 'percentage' not in vars(error_analysis), 'ErrorAnalysis() initialization error'

def test_calculate_percentage(test_case_1):
    errors, ans = test_case_1
    for idx, error in enumerate(errors):
        error.calculate_percentage()
        assert error.percentage == Decimal(ans['percentage'][idx]), 'ErrorAnalysis percentage calculation error'

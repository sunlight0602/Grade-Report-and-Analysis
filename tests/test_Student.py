import pytest
from decimal import Decimal
from GradeReportAndAnalysis.Student import Student
from GradeReportAndAnalysis.ErrorAnalysisVO import ErrorAnalysisVO

def test_initialize():
    student = Student(name='沈小魚')
    assert student.name == '沈小魚', f"Should be 沈小魚"

@pytest.mark.parametrize("name, expected_masked_name", [
    ('沈健康的魚', '沈ＯＯＯ魚'),
    ('沈健康魚', '沈ＯＯ魚'),
    ('沈小魚', '沈Ｏ魚'),
    ('沈魚', '沈Ｏ'),
    ('魚', '魚'),
])
def test_mask_name(name, expected_masked_name):
    student = Student(name)
    assert student.masked_name == expected_masked_name, f"Should be {expected_masked_name}"

def test_error_analysis_percentage():
    error_dict = {
        '形音義': ErrorAnalysisVO(correct=5, total=8),
        '詞語使用': ErrorAnalysisVO(correct=4, total=8),
        '成語運用': ErrorAnalysisVO(correct=6, total=8),
    }
    expected_percentages = [Decimal('62.5'), Decimal('50.0'), Decimal('75.0')]
    
    student = Student(name='沈小魚')
    student.error_analysis = error_dict
    student.analyze_error()

    calculated_percentages = [err.percentage for err in student.error_analysis.values()]
    assert calculated_percentages == expected_percentages, "Error analysis percentages do not match expected values"

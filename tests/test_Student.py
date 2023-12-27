import os
import pytest
from decimal import Decimal
from GradeReportAndAnalysis.Student import Student
from GradeReportAndAnalysis.ErrorAnalysisVO import ErrorAnalysisVO

@pytest.fixture
def test_case_1():
    student = Student('沈小魚')
    student.error_analysis = {
        '形音義': ErrorAnalysisVO(correct=5, total=8),
        '詞語使用': ErrorAnalysisVO(correct=4, total=8),
        '成語運用': ErrorAnalysisVO(correct=6, total=8),
        '修辭技巧': ErrorAnalysisVO(correct=4, total=8),
        '國學常識': ErrorAnalysisVO(correct=3, total=8),
        '閱讀素養': ErrorAnalysisVO(correct=6, total=10),
    }

    ans = {
        'name': '沈小魚',
        'percentages': [Decimal('62.5'), Decimal('50.0'), Decimal('75.0'), Decimal('50.0'), Decimal('37.5'), Decimal('60.0')],
        'labels': student.error_analysis.keys(),
    }
    return student, ans

def test_initialize(test_case_1):
    student, ans = test_case_1
    assert student.name == ans['name'], 'Student() initialization error'

def test_analyze_error(test_case_1):
    student, ans = test_case_1
    student.analyze_error()
    calculated_percentages = [err.percentage for err in student.error_analysis.values()]
    assert calculated_percentages == ans['percentages'], "Error analysis percentages do not match expected values"

def test_draw_figure(test_case_1):
    student, ans = test_case_1
    student.analyze_error()
    student.draw_figure()

    assert student.figure.name == ans['name'], f'Figure name error, should be {ans["name"]}'
    assert student.figure.values == ans['percentages'], "Figure values not correct"
    assert student.figure.labels == ans['labels'], "Figure labels not correct"
    assert student.figure.path == os.path.join(os.getcwd(), 'output_files', 'static', f'{ans["name"]}.png'), "Figure read path not correct"
 
@pytest.mark.parametrize("name, expected_masked_name", [
    ('沈健康的魚', '沈ＯＯＯ魚'),
    ('沈健康魚', '沈ＯＯ魚'),
    ('沈小魚', '沈Ｏ魚'),
    ('沈魚', '沈Ｏ'),
    ('魚', '魚'),
])
def test_mask_name(name, expected_masked_name):
    student = Student(name)
    assert student.masked_name == expected_masked_name, f"Mask name error, should be {expected_masked_name}"

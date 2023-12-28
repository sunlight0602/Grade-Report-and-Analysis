import os
import pytest

from GradeReportAndAnalysis.Info import Info

@pytest.fixture
def test_case_1():
    input_path = os.path.join(os.getcwd(), 'input_files', '1214_第２次全民中檢模擬考.xlsx')
    info = Info(file_name=input_path)
    ans = {
        'title': '第２次全民中檢模擬考',
        'level': '中等',
        'date': '2023/12/14',
        'question_numbers': [i for i in range(1, 51)],
        'descriptions': ['下列文句中「」的字，何者讀音正確？ A「蝙」蝠──「ㄅㄧㄢˇ」 B 神采「熠熠」──「ㄓㄜˊ」 C「興」奮──「ㄒㄧㄥˋ」 D 一語成「讖」──「ㄔㄣˋ」'] + [''] * 49,
        'categories': ['形音義'] * 8 + ['詞語使用'] * 8 + ['成語運用'] * 8 + ['修辭技巧'] * 8 + ['國學常識'] * 8 + ['閱讀素養'] * 10,
        'answers': ['D','B','C','C','A','D','B','D','D','A','D','B','C','B','B','A','D','C','B','C','C','A','D','C','D','B','B','B','D','A','B','C','A','C','C','B','D','D','A','B','C','B','D','A','C','B','A','C','A','D'],
        'names': ['沈小魚', '陳映羽', '陳冠廷', '歐冠女', '陳火昱婷', '屁孩一', 'ASDFGASF'],
        'std1_answers': ['D','B','C','C','A','D','B','D','D','A','D','B','C','B','B','A','D','C','B','C','C','A','D','C','D','B','B','B','D','A','B','C','A','C','C','B','D','D','A','B','C','B','D','A','C','B','A','C','A','D'],
        'std1_conditions' : ['顏色太深'],
    }
    return info, ans

@pytest.fixture
def test_case_2():
    input_path = os.path.join(os.getcwd(), 'input_files', '1117_第１次全民中檢仿真模擬考.xlsx')
    info = Info(file_name=input_path)
    ans = {
        'title': '第１次全民中檢仿真模擬考',
        'level': '初等',
        'date': '2023/07/13',
    }
    return info, ans

def test_initialize(test_case_1, test_case_2):
    for test_case in [test_case_1, test_case_2]:
        info, ans = test_case
        assert info.title == ans['title'], f'Info() initialization error, title should be {ans["title"]}'
        assert info.level == ans['level'], f'Info() initialization error, level should be {ans["level"]}'
        assert info.date == ans['date'], f'Info() initialization error, date should be {ans["date"]}'

def test_read_excel(test_case_1):
    info, ans = test_case_1
    for idx, question in enumerate(info.questions):
        assert question.quest_num == ans['question_numbers'][idx], f'Read excel error, question number should be {ans["question_numbers"][idx]}'
        assert question.description == ans['descriptions'][idx], f'Read excel error, description should be {ans["descriptions"][idx]}'
        assert question.category == ans['categories'][idx], f'Read excel error, category should be {ans["categories"][idx]}'
        assert question.answer == ans['answers'][idx], f'Read excel error, answer should be {ans["answers"][idx]}'
    
    for idx, student in enumerate(info.students):
        assert student.name == ans['names'][idx], f'Read excel error, student name should be {ans["names"][idx]}'

    for i, answer in enumerate(info.students[0].answers):
        assert answer.answer == ans['std1_answers'][i], f'Read excel error, student answer should be {ans["std1_answers"][i]}'
    for i, cond in enumerate(info.students[0].conditions):
        assert cond == ans['std1_conditions'][i], f'Read excel error, student condition should be {ans["std1_conditions"][i]}'

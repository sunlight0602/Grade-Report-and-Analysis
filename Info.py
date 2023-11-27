import decimal
import os

import pandas as pd

from QuestionVO import QuestionVO
from Rank import Rank
from Student import Student, StudentAnswerVO

class Info:
    input_path = os.path.join(".", "input_files")
    output_path = os.path.join(".", "output_files")

    def __init__(self, file_name) -> None:
        self.questions: list[QuestionVO] = []
        self.students: list[Student] = []
        self.title: str
        self.level: str
        self.date = ''

        self.__read_excel(file_name)
        self.rank: Rank
        
    def __read_excel(self, file_name):
        pages = pd.read_excel(os.path.join(Info.input_path, file_name), sheet_name=None)
        self.__read_pg1(pages['題目與答案'])
        self.__read_pg23(pages['學生作答'], pages['學生畫卡'])
    
    def __read_pg1(self, pg1):
        for qnum, desc, cate, ans in zip(list(pg1['題號']), list(pg1['題目']), list(pg1['單元名稱']), list(pg1['解答'])):
            desc = '' if pd.isnull(desc) else desc
            self.questions.append(QuestionVO(qnum, desc, cate, ans))
        self.title = pg1['標題'][0]
        self.level = pg1['級別'][0]
        self.date = pg1['測驗日期'][0]
    
    def __read_pg23(self, pg2, pg3):
        _, *names = pg2.columns
        for name in names:
            student = Student(name)
            student.answers = [StudentAnswerVO(qnum, ans) for qnum, ans in zip(pg2['學生／題號'], pg2[name])]
            student.conditions = [s for s in list(pg3[name]) if not pd.isnull(s)]
            self.students.append(student)

    def calculate_score(self):
        n = len(self.questions)
        for student in self.students:
            # TODO: Test: number of problems is the same as number of answers
            # TODO: Feature: sort problems and answers by idx
            correct = 0

            for idx, (s_ans, q_ans) in enumerate(zip(student.answers, self.questions)):
                if s_ans.quest_num == q_ans.quest_num:
                    category = student.error_analysis[q_ans.category]
                    if s_ans.answer == q_ans.answer:
                        correct += 1
                        category.correct += 1
                        if student.answers[idx].quest_num == q_ans.quest_num:
                            student.answers[idx].correction = '.'
                        else:
                            pass # rais error
                    else:
                        if student.answers[idx].quest_num == q_ans.quest_num:
                            student.answers[idx].correction = q_ans.answer
                        else:
                            pass # raise error
                    category.total += 1
                else:
                    # TODO: Raise error
                    pass

            student.score = round(decimal.Decimal(str(correct / n)) * 100)

            student.analyze_error()
    
        self.rank = Rank(self.students)

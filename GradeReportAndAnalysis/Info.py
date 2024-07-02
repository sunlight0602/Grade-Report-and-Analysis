"""Info class"""

import os

import pandas as pd

from .QuestionVO import QuestionVO
from .Rank import Rank
from .Student import Student, StudentAnswerVO


class Info:
    """excel as the exam info"""

    input_path = os.path.join(os.getcwd(), "input_files")
    output_path = os.path.join(os.getcwd(), "output_files")

    def __init__(self, file_name) -> None:
        self.questions: list[QuestionVO] = []
        self.students: list[Student] = []
        self.title: str
        self.level: str
        self.date: str

        self._read_excel(file_name)
        self.rank: Rank = None

    def _read_excel(self, file_name):
        pages = pd.read_excel(
            os.path.join(Info.input_path, file_name),
            sheet_name=None,
            keep_default_na=False,
        )
        self.__read_pg1(pages["題目與答案"])
        self.__read_pg23(pages["學生作答"], pages["學生畫卡"])

    def __read_pg1(self, pg1):
        for qnum, desc, cate, ans in zip(
            list(pg1["題號"]),
            list(pg1["題目"]),
            list(pg1["單元名稱"]),
            list(pg1["解答"]),
        ):
            self.questions.append(QuestionVO(qnum, desc, cate, ans))
        self.title = pg1["標題"][0]
        self.level = pg1["級別"][0]
        self.date = pg1["測驗日期"][0].strftime("%Y/%m/%d")

    def __read_pg23(self, pg2, pg3):
        _, *names = pg2.columns
        for name in names:
            student = Student(name)
            student.answers = [
                StudentAnswerVO(qnum, ans)
                for qnum, ans in zip(pg2["學生／題號"], pg2[name])
            ]
            student.conditions = [cond for cond in list(pg3[name]) if cond]
            student.calculate_score(self.questions)
            self.students.append(student)

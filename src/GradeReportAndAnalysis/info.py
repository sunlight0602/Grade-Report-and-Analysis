"""Info class"""

import os

import pandas as pd

from .question import Question
from .rank import Rank
from .student import Student, StudentAnswer


class Info:
    """excel as the exam info"""

    input_path = os.path.join(os.getcwd(), "input_files")
    output_path = os.path.join(os.getcwd(), "output_files")

    def __init__(self, file_name, excel_file, from_exe=True) -> None:
        self.questions: list[Question] = []
        self.students: list[Student] = []
        self.title: str
        self.level: str
        self.date: str

        if from_exe:
            self._read_excel(file_name)
        else:
            self._read_excel_web(excel_file)
        self.rank: Rank = None

    def _read_excel(self, file_name):
        pages = pd.read_excel(
            os.path.join(Info.input_path, file_name),
            sheet_name=None,
            keep_default_na=False,
        )
        self.__read_pg1(pages["題目與答案"])
        self.__read_pg234(pages["學生作答"], pages["畫卡狀況"], pages["作答速度"])

    def _read_excel_web(self, excel_file):
        """read excel from backend api"""
        pages = pd.read_excel(
            io=excel_file,
            sheet_name=None,
            keep_default_na=False,
        )
        self.__read_pg1(pages["題目與答案"])
        self.__read_pg234(pages["學生作答"], pages["畫卡狀況"], pages["作答速度"])

    def __read_pg1(self, pg1):
        for qnum, desc, cate, ans in zip(
            list(pg1["題號"]),
            list(pg1["題目"]),
            list(pg1["單元名稱"]),
            list(pg1["解答"]),
        ):
            self.questions.append(Question(qnum, desc, cate, ans))
        self.title = pg1["標題"][0]
        self.level = pg1["級別"][0]
        self.date = pg1["測驗日期"][0].strftime("%Y/%m/%d")

    def __read_pg234(self, pg2, pg3, pg4):
        _, *names = pg2.columns
        for name in names:
            student = Student(name)
            student.answers = [
                StudentAnswer(qnum, ans)
                for qnum, ans in zip(pg2["學生／題號"], pg2[name])
            ]
            student.conditions = [cond for cond in list(pg3[name]) if cond]
            student.speeds = [cond for cond in list(pg4[name]) if cond]
            student.calculate_score(self.questions)
            self.students.append(student)

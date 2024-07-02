import collections
import decimal
import os

from .error_analysis import ErrorAnalysis
from .figure import Figure
from .student_answer import StudentAnswer


class Student:
    output_path = os.path.join(".", "output_files")

    def __init__(self, name) -> None:
        self.name: str = name
        self.masked_name: str = self._mask_name(self.name)
        self.answers: list[StudentAnswer] = []
        self.conditions: list = []
        self.speeds: list = []

        self.score: decimal.Decimal = None

        self.error_analysis = collections.defaultdict(ErrorAnalysis)
        self.figure: Figure

    def _mask_name(self, name):
        if len(name) <= 2:
            return name[0] + "Ｏ" * (len(name) - 1)
        return f"{name[0]}{'Ｏ' * (len(name) - 2)}{name[-1]}"

    def __analyze_error(self):
        for error in self.error_analysis.values():
            error.calculate_percentage()

    def get_figure(self):
        values = [err.percentage for err in self.error_analysis.values()]
        figure = Figure(
            name=self.name, values=values, labels=self.error_analysis.keys()
        )
        self.figure = figure

    def calculate_score(self, questions):
        n = len(questions)
        correct = 0

        for s_ans, question in zip(self.answers, questions):
            self.error_analysis[question.category].total += 1
            if s_ans.answer == question.answer:
                correct += 1
                self.error_analysis[question.category].correct += 1
                s_ans.correction = "."
            else:
                s_ans.correction = s_ans.answer

        self.score = round(decimal.Decimal(str(correct / n)) * 100)
        self.__analyze_error()

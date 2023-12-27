import decimal
import os

import collections

from .ErrorAnalysisVO import ErrorAnalysisVO
from .StudentAnswerVO import StudentAnswerVO
from .Figure import Figure


class Student:
    output_path = os.path.join(".", "output_files")

    def __init__(self, name) -> None:
        self.name: str = name
        self.masked_name: str = self.__mask_name(self.name)
        self.answers: list[StudentAnswerVO] = []
        self.conditions = []
    
        self.score: decimal.Decimal = None

        self.error_analysis = collections.defaultdict(ErrorAnalysisVO)
        self.figure: Figure
        self.report = None

    def __mask_name(self, name):
        if len(name) <= 2:
            return name[0] + 'Ｏ' * (len(name) - 1)
        return f"{name[0]}{'Ｏ' * (len(name) - 2)}{name[-1]}"       

    def __analyze_error(self):
        for error in self.error_analysis.values():
            error.calculate_percentage()

    def draw_figure(self):
        values = [err.percentage for err in self.error_analysis.values()]
        figure = Figure(name=self.name, values=values, labels=self.error_analysis.keys())
        self.figure = figure

    def calculate_score(self, questions):
        n = len(questions)
        correct = 0

        for s_ans, question in zip(self.answers, questions):
            if s_ans.quest_num == question.quest_num:
                self.error_analysis[question.category].total += 1
                if s_ans.answer == question.answer:
                    correct += 1
                    self.error_analysis[question.category].correct += 1
                    s_ans.correction = '.'
                else:
                    s_ans.correction = s_ans.answer
        
        self.score = round(decimal.Decimal(str(correct / n)) * 100)
        self.__analyze_error()

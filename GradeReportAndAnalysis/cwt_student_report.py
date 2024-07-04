import os
from typing import List

from .cwt_report import CWTReport
from .info import Info
from .question import Question
from .rank import Rank
from .student import Student


class CWTStudentReport(CWTReport):  # composition from Info, Student, and Rank
    def __init__(self, student: Student, info: Info, rank: Rank) -> None:
        self.student: Student = student

        self.questions: List[Question] = info.questions
        self.title: str = info.title
        self.level: str = info.level
        self.date: str = info.date

        self.rank: Rank = rank
        self.report = None

    def generate_student_report(self):
        template = self.open_template("cwt_student_report_template.html")
        self.rank.hide_rank()
        self.rank.random_rank()
        self.student.get_figure()

        ranking = []
        for std, rank in zip(
            self.rank.sorted_rank["students"], self.rank.sorted_rank["rank"]
        ):
            ranking.append([std.masked_name, std.score, rank])

        self.report = template.render(
            title=self.title,
            date=self.date,
            level=self.level,
            name=self.student.name,
            score=self.student.score,
            conditions=self.student.conditions,
            speeds=self.student.speeds,
            q_answers=[question.answer for question in self.questions],
            s_answers=[answer.correction for answer in self.student.answers],
            fig_path=self.student.figure.path,
            error_analysis=self.student.error_analysis,
            pr88=self.rank.pr88,
            pr75=self.rank.pr75,
            pr50=self.rank.pr50,
            pr25=self.rank.pr25,
            ranking=ranking,
        )

        print(os.path.join(self.output_path, f"{self.student.name}.html"))
        wrt_path = os.path.join(self.output_path, f"{self.student.name}.html")
        with open(wrt_path, encoding="utf-8", mode="w") as f:
            f.write(self.report)

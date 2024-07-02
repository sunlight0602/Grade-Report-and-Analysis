import decimal
import os

from .cwt_report import CWTReport
from .figure import Figure
from .info import Info
from .rank import Rank


class CWTTeacherReport(CWTReport):  # composition from Info, Student, and Rank
    name = "老師"

    def __init__(self, student, info, rank) -> None:
        self.error_analysis = student.error_analysis

        self.info: Info = info
        self.title: str = info.title
        self.level: str = info.level
        self.date: str = info.date

        self.rank: Rank = rank
        self.report = None

    def _get_accuracy_for_each_question(self):
        students = self.info.students
        n, m = len(students), len(self.info.questions)
        correct = [0] * m
        incorrect = [0] * m

        for student in students:
            for idx, ans in enumerate(student.answers):
                if ans.correction == ".":
                    correct[idx] += 1
                else:
                    incorrect[idx] += 1

        correct_accuracy = []
        incorrect_accuracy = []
        for num in correct:
            acc = round(decimal.Decimal(str(num / n)) * 100)
            correct_accuracy.append(acc)
            incorrect_accuracy.append(100 - acc)
        return correct, incorrect, correct_accuracy, incorrect_accuracy

    def __get_teacher_figure(self):
        n = len(self.info.students)
        corrects = [0] * len(self.error_analysis)
        quest_total = [0] * len(self.error_analysis)
        for student in self.info.students:
            for idx, (_, err) in enumerate(student.error_analysis.items()):
                corrects[idx] += err.correct
                quest_total[idx] = err.total * n

        avg_crt = [round(decimal.Decimal(str(crt / n)), 2) for crt in corrects]

        values = []
        for corr, q_total in zip(corrects, quest_total):
            values.append(round(decimal.Decimal(str(corr / q_total)) * 100))

        figure = Figure(
            name=self.name, values=values, labels=self.error_analysis.keys()
        )
        return figure.path, avg_crt

    def generate_teacher_report(self):
        template = self.open_template("cwt_teacher_report_template.html")
        self.rank.calculate_rank()
        correct_num, incorrect_num, correct_accuracy, incorrect_accuracy = self._get_accuracy_for_each_question()
        teacher_fig_path, avg_each_std = self.__get_teacher_figure()

        ranking = []
        for std, rank in zip(
            self.rank.sorted_rank["students"], self.rank.sorted_rank["rank"]
        ):
            ranking.append([std.name, std.score, rank])

        self.report = template.render(
            title=self.title,
            date=self.date,
            level=self.level,
            q_answers=[question.answer for question in self.info.questions],
            q_categories=[question.category[0] for question in self.info.questions],
            q_accuracy=incorrect_accuracy,
            q_incorrect_num=incorrect_num,
            fig_path=teacher_fig_path,
            error_analysis=self.error_analysis,
            avg_each_std=avg_each_std,
            zip=zip,
            pr88=self.rank.pr88,
            pr75=self.rank.pr75,
            pr50=self.rank.pr50,
            pr25=self.rank.pr25,
            ranking=ranking,
        )

        wrt_path = os.path.join(self.output_path, f"{self.name}.html")
        with open(wrt_path, "w") as f:
            f.write(self.report)

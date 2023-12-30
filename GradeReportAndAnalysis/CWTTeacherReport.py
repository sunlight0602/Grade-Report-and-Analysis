import decimal
import os

from .CWTReport import CWTReport
from .Figure import Figure
from .Info import Info
from .Rank import Rank


class CWTTeacherReport(CWTReport): # composition from Info, Student, and Rank
    name = '老師'

    def __init__(self, student, info, rank) -> None:
        self.error_analysis = student.error_analysis

        self.info: Info = info
        self.title: str = info.title
        self.level: str = info.level
        self.date: str = info.date

        self.rank: Rank = rank
        self.report = None

    def __get_accuracy_for_each_question(self):
        students = self.info.students
        n, m = len(students), len(self.info.questions)
        correct = [0] * m

        for student in students:
            for idx, ans in enumerate(student.answers):
                if ans.correction == '.':
                    correct[idx] += 1
        
        return correct, [round(decimal.Decimal(str(num / n)) * 100) for num in correct]
    
    def __get_teacher_figure(self):
        n = len(self.info.students)
        corrects, quest_total = [0] * len(self.error_analysis), [0] * len(self.error_analysis)
        for student in self.info.students:
            for idx, (_, err) in enumerate(student.error_analysis.items()):
                corrects[idx] += err.correct
                quest_total[idx] = err.total * n
        average_corr_each_student = [round(decimal.Decimal(str(corr/n)), 2) for corr in corrects]
        
        values = []
        for corr, q_total in zip(corrects, quest_total):
            values.append(round(decimal.Decimal(str(corr / q_total)) * 100))         

        figure = Figure(name=self.name, values=values, labels=self.error_analysis.keys())
        return figure.path, average_corr_each_student

    def generate_teacher_report(self):
        template = self.open_template('teacher_report_template.html')
        self.rank.calculate_rank()
        correct_num, acc = self.__get_accuracy_for_each_question()
        teacher_fig_path, avg_each_std = self.__get_teacher_figure()

        ranking = []
        for std, rank in zip(self.rank.sorted_rank['students'], self.rank.sorted_rank['rank']):
            ranking.append([std.name, std.score, rank])

        self.report = template.render(
            title = self.title,
            date = self.date,
            level = self.level,

            q_answers = [question.answer for question in self.info.questions],
            q_categories = [question.category[0] for question in self.info.questions],
            q_accuracy = acc,
            q_correct_num = correct_num,

            fig_path = teacher_fig_path,
            error_analysis = self.error_analysis,
            avg_each_std = avg_each_std,
            zip = zip,

            pr88 = self.rank.pr88,
            pr75 = self.rank.pr75,
            pr50 = self.rank.pr50,
            pr25 = self.rank.pr25,
            ranking = ranking,
        )

        with open(os.path.join(self.output_path, f'{self.name}.html'), 'w') as f:
            f.write(self.report)

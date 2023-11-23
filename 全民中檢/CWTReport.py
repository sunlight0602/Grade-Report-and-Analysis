import os
from Info import Info
from Student import Student
from jinja2 import Template

class CWTReport: # composition from Both Info and Student
    # output_path = os.path.join(".", "output_files")

    def __init__(self, student, info) -> None:
        self.student: Student = student
        self.info:Info = info
        self.report = None
    
    def generate_report(self):
        with open('student_report_template.html', 'r') as file:
            template = Template(file.read())
        
        self.info.rank.calculate_rank(masked=True, random=True)

        self.report = template.render(
            title = self.info.title,
            date = self.info.date.strftime("%Y/%m/%d"),
            level = self.info.level,

            name = self.student.name,
            score = self.student.score,
            conditions = self.student.conditions,

            q_answers = [question.answer for question in self.info.questions],
            s_answers = [answer.correction for answer in self.student.answers],

            fig_path = self.student.figure_path,
            error_analysis = self.student.error_analysis,

            pr88 = self.info.rank.pr88,
            pr75 = self.info.rank.pr75,
            pr50 = self.info.rank.pr50,
            pr25 = self.info.rank.pr25,
            ranking = self.info.rank.sorted_rank
        )

        with open(f'{self.student.name}.html', 'w') as f:
            f.write(self.report)
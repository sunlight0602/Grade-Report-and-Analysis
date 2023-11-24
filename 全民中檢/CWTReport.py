import os
from Info import Info
from Student import Student
from jinja2 import Template
import decimal
import numpy as np
import matplotlib.pyplot as plt

class CWTReport: # composition from Both Info and Student
    output_path = os.path.join(".", "output_files")

    def __init__(self, student, info) -> None:
        self.student: Student = student
        self.info:Info = info
        self.report = None
    
    def generate_student_reports(self):
        with open('student_report_template.html', 'r') as file:
            template = Template(file.read())
        self.info.rank.calculate_rank(masked=True, random=True)
        
        self.student.draw_figure()
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

        with open(os.path.join(self.output_path, self.student.name + '.html'), 'w') as f:
            f.write(self.report)

    def get_accuracy_for_each_question(self):
        students = self.info.students
        n, m = len(students), len(self.info.questions)
        correct = [0] * m

        for student in students:
            for idx, ans in enumerate(student.answers):
                if ans.correction == '.':
                    correct[idx] += 1
        
        return correct, [round(decimal.Decimal(str(num / n)) * 100) for num in correct]
    
    def get_teacher_figure(self):
        n = len(self.info.students)
        corrects, quest_total = [0] * len(self.student.error_analysis), [0] * len(self.student.error_analysis)
        for student in self.info.students:
            for idx, (_, err) in enumerate(student.error_analysis.items()):
                corrects[idx] += err.correct
                quest_total[idx] = err.total * n
        average_corr_each_student = [round(decimal.Decimal(str(corr/n)), 2) for corr in corrects]
        
        values = []
        for corr, q_total in zip(corrects, quest_total):
            values.append(round(decimal.Decimal(str(corr / q_total)) * 100))         

        angles = np.linspace(0, 2*np.pi, len(values), endpoint=False) # 設置每個數據點的顯示位置，在雷達圖上用角度表示

        # 拼接數據首尾，使圖形中線條封閉
        values = np.concatenate((values,[values[0]]))
        angles = np.concatenate((angles,[angles[0]]))

        # 繪圖
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, values, 'o-', linewidth=2) # 繪製折線圖
        ax.fill(angles, values, alpha=0.25) # 填充顏色

        # 設置圖標上的角度劃分刻度，爲每個數據點處添加標籤
        ax.set_thetagrids(angles=(0,60,120,180,240,300), labels=self.student.error_analysis.keys(), fontsize=14)

        ax.set_ylim(0, 100) # 設置雷達圖的範圍
        ax.grid(True) # 添加網格線

        plt.savefig(os.path.join(self.output_path, 'static', '老師.png'))
        return os.path.join('.', 'static', '老師.png'), average_corr_each_student



    def generate_teacher_report(self):
        with open('teacher_report_template.html', 'r') as file:
            template = Template(file.read())
        
        self.info.rank.calculate_rank(masked=False, random=False)
        correct_num, acc = self.get_accuracy_for_each_question()
        teacher_fig_path, avg_each_std = self.get_teacher_figure()


        self.report = template.render(
            title = self.info.title,
            date = self.info.date.strftime("%Y/%m/%d"),
            level = self.info.level,

            name = self.student.name,
            score = self.student.score,
            conditions = self.student.conditions,

            q_answers = [question.answer for question in self.info.questions],
            q_categories = [question.category[0] for question in self.info.questions],
            q_accuracy = acc,
            q_correct_num = correct_num,

            fig_path = teacher_fig_path,
            error_analysis = self.student.error_analysis,
            avg_each_std = avg_each_std,
            zip = zip,

            pr88 = self.info.rank.pr88,
            pr75 = self.info.rank.pr75,
            pr50 = self.info.rank.pr50,
            pr25 = self.info.rank.pr25,
            ranking = self.info.rank.sorted_rank
        )

        with open(os.path.join(self.output_path, '老師.html'), 'w') as f:
            f.write(self.report)
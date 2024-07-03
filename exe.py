from os import listdir
from os.path import isfile, join

from GradeReportAndAnalysis.cwt_student_report import CWTStudentReport
from GradeReportAndAnalysis.cwt_teacher_report import CWTTeacherReport
from GradeReportAndAnalysis.info import Info
from GradeReportAndAnalysis.rank import Rank

onlyfiles = [
    f for f in listdir(join(".", "input_files")) if isfile(join(".", "input_files", f))
]
excels = []
for file in onlyfiles:
    if file.endswith(".xlsx"):
        excels.append(file)

info = Info(file_name=excels[0])
rank = Rank(info.students)
rank.calculate_rank()

for student in info.students:
    cwt_student_report = CWTStudentReport(student, info, rank)
    cwt_student_report.generate_student_report()

cwt_teacher_report = CWTTeacherReport(student, info, rank)
cwt_teacher_report.generate_teacher_report()

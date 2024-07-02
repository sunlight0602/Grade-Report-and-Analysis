from GradeReportAndAnalysis.cwt_student_report import CWTStudentReport
from GradeReportAndAnalysis.cwt_teacher_report import CWTTeacherReport
from GradeReportAndAnalysis.info import Info
from GradeReportAndAnalysis.rank import Rank

info = Info(file_name="1214_第２次全民中檢模擬考.xlsx")
rank = Rank(info.students)
rank.calculate_rank()

for student in info.students:
    cwt_student_report = CWTStudentReport(student, info, rank)
    cwt_student_report.generate_student_report()

cwt_teacher_report = CWTTeacherReport(student, info, rank)
cwt_teacher_report.generate_teacher_report()

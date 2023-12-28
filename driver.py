from GradeReportAndAnalysis.Info import Info
from GradeReportAndAnalysis.CWTReport import CWTReport
from GradeReportAndAnalysis.Rank import Rank

info = Info(file_name="1214_第２次全民中檢模擬考.xlsx")
rank = Rank(info.students)
rank.calculate_rank()

for student in info.students:
    cwt_report = CWTReport(student, info, rank)
    cwt_report.generate_student_report()

cwt_report.generate_teacher_report()

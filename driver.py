from GradeReportAndAnalysis.Info import Info
from GradeReportAndAnalysis.CWTReport import CWTReport

info = Info(file_name="1214_第２次全民中檢模擬考.xlsx")
info.calculate_score()

for student in info.students:
    cwt_report = CWTReport(student, info)
    cwt_report.generate_student_report()

cwt_report.generate_teacher_report()

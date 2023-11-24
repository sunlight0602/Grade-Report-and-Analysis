from Info import Info
from CWTReport import CWTReport

info = Info(file_name="1117_第１次全民中檢仿真模擬考.xlsx")
info.calculate_score()
info.students[0].draw_figure()
cwt_report = CWTReport(info.students[0], info)
cwt_report.generate_student_reports()

cwt_report.generate_teacher_report()

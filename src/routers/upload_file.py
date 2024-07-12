"""handle file upload"""

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from src.GradeReportAndAnalysis.cwt_student_report import CWTStudentReport
from src.GradeReportAndAnalysis.cwt_teacher_report import CWTTeacherReport
from src.GradeReportAndAnalysis.info import Info
from src.GradeReportAndAnalysis.rank import Rank

router = APIRouter()


@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """process excel file and pass to database"""
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .xlsx files are allowed."
        )

    content = await file.read()
    info = Info(file_name="", excel_file=content, from_exe=False)
    names = [student.name for student in info.students]

    return JSONResponse(
        content={"message": "File processed successfully", "data": names}
    )


def process_file(info: Info):
    """process info"""

    rank = Rank(info.students)
    rank.calculate_rank()

    for student in info.students:
        cwt_student_report = CWTStudentReport(student, info, rank)
        cwt_student_report.generate_student_report()

    cwt_teacher_report = CWTTeacherReport(student, info, rank)
    cwt_teacher_report.generate_teacher_report()

"""handle file upload"""

import io

import openpyxl
import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from src.GradeReportAndAnalysis.info import Info
# from ..GradeReportAndAnalysis.info import Info

# from src.GradeReportAndAnalysis.info import Info

router = APIRouter()


# @app.post("/uploadfile/")
@router.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    """process excel file and pass to database"""
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only .xlsx files are allowed."
        )

    # Read the file content
    content = await file.read()
    workbook = openpyxl.load_workbook(io.BytesIO(content))
    sheet = workbook.active

    # Another read file content
    # pages = pd.read_excel(
    #     io=content,
    #     sheet_name=None,
    #     keep_default_na=False,
    # )
    info = Info(file_name="", excel_file=content, from_exe=False)

    # Process the data (example: print all rows)
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
        print(row)  # Example action: print each row

    return JSONResponse(
        content={"message": "File processed successfully", "data": data}
    )

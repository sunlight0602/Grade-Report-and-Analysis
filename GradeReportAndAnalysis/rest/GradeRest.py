from fastapi import UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import openpyxl
import io

from GradeReportAndAnalysis.Server import app


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .xlsx files are allowed.")

    # Read the file content
    content = await file.read()
    workbook = openpyxl.load_workbook(io.BytesIO(content))
    sheet = workbook.active

    # Process the data (example: print all rows)
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
        print(row)  # Example action: print each row

    return JSONResponse(content={"message": "File processed successfully", "data": data})

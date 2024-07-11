"""handle file upload"""

import io

import openpyxl
from fastapi import File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from src.main import app


@app.post("/uploadfile/")
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

    # Process the data (example: print all rows)
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
        print(row)  # Example action: print each row

    return JSONResponse(
        content={"message": "File processed successfully", "data": data}
    )

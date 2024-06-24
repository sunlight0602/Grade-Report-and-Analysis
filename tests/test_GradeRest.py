import pytest
from fastapi.testclient import TestClient
from io import BytesIO
import openpyxl
from GradeReportAndAnalysis.Server import app  # Ensure this import matches your application structure

client = TestClient(app)


@pytest.fixture
def sample_xlsx_file():
    # Create a sample Excel file in memory
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet["A1"] = "Hello"
    sheet["B1"] = "World"
    file_stream = BytesIO()
    workbook.save(file_stream)
    file_stream.seek(0)
    return file_stream


def test_upload_file(sample_xlsx_file):
    response = client.post(
        "/uploadfile/",
        files={"file": (
            "test.xlsx", sample_xlsx_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["message"] == "File processed successfully"
    assert json_response["data"] == [["Hello", "World"]]


def test_upload_invalid_file():
    response = client.post(
        "/uploadfile/",
        files={"file": ("test.txt", BytesIO(b"Invalid content"), "text/plain")}
    )
    assert response.status_code == 400
    json_response = response.json()
    assert json_response["detail"] == "Invalid file type. Only .xlsx files are allowed."

"""entry point of backend API"""

from fastapi import FastAPI

from src.routers import upload_file

app = FastAPI()
app.include_router(upload_file.router)


@app.get("/")
def test():
    """test get method"""
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

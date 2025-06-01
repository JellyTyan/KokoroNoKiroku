import uvicorn
from fastapi import FastAPI

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=5003, log_level="info")

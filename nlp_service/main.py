from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from schema import DataModel
from parcer import parse_text


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://api:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse/", response_model=DataModel)
def read_root(
    text: str
) -> DataModel:
    return parse_text(text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
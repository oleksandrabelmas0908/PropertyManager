from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Annotated

from db.engine import get_session, Session
from schemas import InputModel, PropertySchema
from crud import get_and_set_matching_properties


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://api:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/match/", response_model=list[PropertySchema])
def read_root(
    input: InputModel,
    session: Annotated[Session, Depends(get_session)],
):
    property_list = get_and_set_matching_properties(session, input.user_id)

    return property_list


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
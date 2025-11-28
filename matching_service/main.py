from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Annotated

from db.engine import get_session, Session
from schemas import InputModel, PropertySchema
from crud import get_and_set_matching_properties

from broker import get_messages, produce


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://api:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/match/")
def read_root(
    session: Annotated[Session, Depends(get_session)]
):
    messages = get_messages(
        topic="match_topic",
        group_id="matching_service_group"
    )
    property_lists = []
    for message in messages:
        user_id = message.get("user_id")
        if user_id:
            property_list = get_and_set_matching_properties(session, int(user_id))

            produce(
                message={
                    "user_id": int(user_id),
                    "matched_properties": property_list
                },
                topic="proceeded_match_topic"
            )

            property_lists.append(property_list)

    return {"status": "success"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
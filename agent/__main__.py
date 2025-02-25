from os import name
from typing import Literal, Mapping
from fastapi import FastAPI, Request

from agent.helpers import get_user_from_db, search_from_query

app = FastAPI()

# @app.post("/agent/search")
# async def search(request: Request) -> dict[str, str]:
#     request_body = await request.json()
#     result = search_from_query(request_body['search_query'])
#     return {
#         "result": result
#     }

# @app.get("/agent/get-note")
# async def get_note(request: Request) -> dict[str, str]:
#     note = get_note_from_db()
#     print("got note:", note)
#     return {
#         "note": note
#     }

@app.get("/")
def read_root() -> dict[str, str]:
    return {}

# @app.post("/agent/save-user")
# async def take_note(request: Request) -> dict[str, str]:
#     request_body = await request.json()
#     # if save_note(request_body['note']):
#     #     return {"status": "success"}
#     # else:
#     #     return {"status": "error"}
#     print(request_body)
#     return {}

@app.post("/agent/commit")
async def search(request: Request) -> dict[str, str]:
    request_body = await request.json()
    print(request_body)
    # result = search_from_query(request_body['search_query'])
    return {}

@app.post("/agent/init")
async def init(request: Request): # dict[Literal["dynamic_variables", "conversation_config_override"], dict[str, str | dict[str, dict[str, str | dict[str, str]]]]]:
    request_body = await request.json()
    caller_id = request_body['caller_id']
    print("caller_id:", caller_id)
    user = get_user_from_db(caller_id)
    print("got user:", user)
    if not user:
        return {}

    output = {
        "dynamic_variables": {
            "name": user['name'],
            "phone_number": user['phone_number'],
            "_id": user['_id']
        },
        "conversation_config_override": {
            "agent": {
                "prompt": {
                    "prompt": "You are a recruiter named RecruitBot and are helping customers to find new employees or contractors to help them."
                },
                "first_message": "Hi, Dylan, how can I help you today?"
            }
        }
    }
    
    print("got here:", user)

    return output
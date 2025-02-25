from os import name
from typing import Literal, Mapping
from fastapi import FastAPI, Request

from agent.helpers import Commitment, get_last_commitment, get_user_from_db, save_commitment

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {}

@app.post("/agent/commit")
async def search(request: Request) -> dict[str, str]:
    request_body = await request.json()
    save_commitment(request_body)
    return {
        "status": "success"
    }

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
        },
        "conversation_config_override": {
            "agent": {
                "prompt": {
                    "prompt": "You are a recruiter named RecruitBot and are helping customers to find new employees or contractors to help them."
                },
                "first_message": "Hi, {name}, how can I help you today?"
            }
        }
    }

    last_commitment: Commitment | None = get_last_commitment(caller_id)
    if last_commitment:
        output["conversation_config_override"]["agent"]["first_message"] = f"Hi, {name}, how can I help you today?  How did things go with {last_commitment['firstName']}?"
    
    print("got here:", user)

    return output
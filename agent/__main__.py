from fastapi import FastAPI, Request

from agent.helpers import get_note_from_db, save_note, search_from_query

app = FastAPI()

@app.get("/")
def read_root() -> dict[str, str]:
    return {}

@app.post("/agent/take-note")
async def take_note(request: Request) -> dict[str, str]:
    request_body = await request.json()
    if save_note(request_body['note']):
        return {"status": "success"}
    else:
        return {"status": "error"}

@app.post("/agent/search")
async def search(request: Request) -> dict[str, str]:
    request_body = await request.json()
    result = search_from_query(request_body['search_query'])
    return {
        "result": result
    }

@app.post("/agent/commit")
async def search(request: Request) -> dict[str, str]:
    request_body = await request.json()
    print(request_body)
    # result = search_from_query(request_body['search_query'])
    return {}

@app.get("/agent/get-note")
async def get_note(request: Request) -> dict[str, str]:
    note = get_note_from_db()
    print("got note:", note)
    return {
        "note": note
    }

@app.post("/agent/init")
async def init(request: Request) -> dict[str, str]:
    request_body = await request.json()
    print(request_body)
    return {"status": "success"}

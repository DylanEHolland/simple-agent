from pymongo.results import InsertOneResult


from pymongo.synchronous.mongo_client import MongoClient


from typing import Any, TypedDict


import os
from dotenv import load_dotenv
from pymongo import DESCENDING, MongoClient
import requests
from elevenlabs import ElevenLabs

_ = load_dotenv()

MONGO_URI: str | None = os.getenv("MONGODB_URI")    
client = MongoClient(MONGO_URI)
db = client['recruit_bot']
# notes_collection = db['notes']
users_collection = db['users']
eleven_labs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

# def save_note(note: str) -> bool:
#     result = notes_collection.insert_one({"note": note})
#     if result.inserted_id:
#         return True
#     else:
#         return False

class User(TypedDict):
    _id: str
    phone_number: str
    name: str

def save_user(user: User) -> bool:
    result: InsertOneResult = users_collection.insert_one(user)
    if result.inserted_id:
        return True
    else:
        return False

def get_user_from_db(phone_number: str) -> User | None:
    last_doc = users_collection.find_one({"phone_number": phone_number}, sort=[("_id", DESCENDING)])
    if last_doc:
        return last_doc
    else:
        return None

#   const body = {
#     model: metaData?.model || "llama-3.1-sonar-large-128k-online", // Specify the model
#     messages: [
#       { role: "system", content: "You are an AI assistant." },
#       { role: "user", content: prompt },
#     ],
#     max_tokens: 1024,
#     // temperature: 0.7
#   };

def query_perplexity(query: str):
# Searches perplexity
    url = "https://api.perplexity.ai/chat/completions"

    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv("PERPLEXITY_API_KEY")}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "sonar",
        "messages": [
            { "role": "system", "content": "You are an AI assistant." },
            { "role": "user", "content": query },
        ],
        "max_tokens": 1024,
    }

    response = requests.post(url, headers=headers, json=data)
    citations = response.json()['citations']
    output = response.json()['choices'][0]['message']['content']
    return output

def search_from_query(note: str) -> str:
# Searches perplexity
    result = query_perplexity(note)

    if result:
        return result
    else:
        return "couldn't find any relevant note"

def get_agent(name: str | None = None):
# Get an agent object by name, current the search is broken on the elevenlabs side
    if name:
        return eleven_labs.conversational_ai.get_agents(search=name)
    else:
        return eleven_labs.conversational_ai.get_agents()
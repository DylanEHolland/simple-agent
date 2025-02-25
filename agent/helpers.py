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
commitments_collection = db['commitments']
eleven_labs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

class User(TypedDict):
    _id: str
    phone_number: str
    name: str

class Commitment(TypedDict):
    lastName: str
    firstName: str
    phoneNumber: str
    email: str
    phone_number: str

def save_user(user: User) -> bool:
    result: InsertOneResult = users_collection.insert_one(user)
    if result.inserted_id:
        return True
    else:
        return False

def save_commitment(commitment: Commitment) -> bool:
    result: InsertOneResult = commitments_collection.insert_one(commitment)
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

def get_agent(name: str | None = None):
# Get an agent object by name, current the search is broken on the elevenlabs side
    if name:
        return eleven_labs.conversational_ai.get_agents(search=name)
    else:
        return eleven_labs.conversational_ai.get_agents()
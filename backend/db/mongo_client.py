from pymongo import MongoClient
from backend.core.config import settings

mongo_client = MongoClient(settings.MONGO_URL)
db = mongo_client[settings.MONGO_DB]

def get_mongo_db():
    return db

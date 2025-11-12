from pymongo import MongoClient
from app.settings import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
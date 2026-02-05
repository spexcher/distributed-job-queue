from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]
worker_collection = db["workers"]
job_collection = db["jobs"]

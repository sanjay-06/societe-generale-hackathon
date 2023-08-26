from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url=os.getenv("MONGO_URL")

conn = MongoClient(mongo_url)

db= conn.get_database('cloudwiry')

collection = db.usercredentials

permission = db.permissions
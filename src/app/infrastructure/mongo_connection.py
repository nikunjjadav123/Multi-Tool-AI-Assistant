import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_database():
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")

    client = MongoClient(uri)
    return client[db_name]

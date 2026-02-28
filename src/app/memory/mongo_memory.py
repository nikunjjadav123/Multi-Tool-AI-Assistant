from langgraph.checkpoint.mongodb import MongoDBSaver
from app.infrastructure.mongo_connection import get_database


def get_mongo_checkpointer():
    db = get_database()
    collection = db["conversation_memory"]
    return MongoDBSaver(collection)

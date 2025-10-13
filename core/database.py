from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            uri = os.getenv("MONGODB_URI")
            db_name = os.getenv("MONGODB_DB_NAME")

            if not uri or not db_name:
                raise ValueError("As variáveis MONGODB_URI e MONGODB_DB_NAME precisam estar definidas no .env")

            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(uri)
            cls._instance.db = cls._instance.client[db_name]
        return cls._instance

    def get_collection(self, name: str):
        return self.db[name]

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("MONGODB_URI")

client = MongoClient(url, server_api=ServerApi("1"))

try:
    client.mercado_livre.command("ping")
    print("Ping db test successful")
except Exception as e:
    print(e)

db = client.mercado_livre

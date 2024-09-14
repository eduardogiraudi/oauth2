from flask_pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv('.env')
client = MongoClient(f'mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@{os.getenv("MONGO_HOST")}:{os.getenv("MONGO_PORT")}/')
db = client['auth']
clients_collection= db['clients']
users_collection = db['users']
with open('client.json', 'r') as file:
    clients = json.load(file)
if not clients_collection.find_one({}):
    clients_collection.insert_one(clients)
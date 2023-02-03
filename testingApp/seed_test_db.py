from apiApp.dev_data import patterns, users
from pymongo import MongoClient

import os
import urllib.parse 
from dotenv import load_dotenv
load_dotenv()

mongo_uri = str(os.getenv('MONGO_URI'))
client = MongoClient(mongo_uri)

db = client["multiply_till_you_die_db"]


def seed_test_db():
    patterns_collection = db['patterns_test']
    patterns_collection.drop()
    patterns_collection.insert_many(patterns)
    
    users_collection = db['users_test']
    users_collection.drop()
    users_collection.insert_many(users)

from dev_data import patterns, users
from pymongo import MongoClient

import os
import urllib.parse 
from dotenv import load_dotenv
load_dotenv()

username_env = str(os.getenv('MONGO_USERNAME'))
password_env = str(os.getenv('MONGO_PASSWORD'))

username = urllib.parse.quote_plus(username_env)
password = urllib.parse.quote_plus(password_env)
client = MongoClient('mongodb+srv://%s:%s@rootcluster.i0un9uw.mongodb.net/' % (username, password))
db = client["multiply_till_you_die_db"]

def seed_db():
    patterns_collection = db['patterns']
    patterns_collection.drop()
    patterns_collection.insert_many(patterns)
    
    users_collection = db['users']
    users_collection.drop()
    users_collection.insert_many(users)

seed_db()

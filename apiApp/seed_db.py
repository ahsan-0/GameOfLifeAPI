from dev_data import patterns, users
from pymongo import MongoClient


def seed_db():
    client = MongoClient(
        "mongodb+srv://GNA7R:eerDKGruC7PUqjyx@rootcluster.i0un9uw.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client['multiply_till_you_die_db']
    patterns_collection = db['patterns']
    patterns_collection.drop()
    patterns_collection.insert_many(patterns)
    
    users_collection = db['users']
    users_collection.drop()
    users_collection.insert_many(users)

seed_db()

from apiApp.dev_data import patterns, users
from pymongo import MongoClient


def seed_test_db():
    client = MongoClient(
        "mongodb+srv://GNA7R:eerDKGruC7PUqjyx@rootcluster.i0un9uw.mongodb.net/?retryWrites=true&w=majority"
    )
    db = client['multiply_till_you_die_db']
    patterns_collection = db['patterns_test']
    patterns_collection.drop()
    patterns_collection.insert_many(patterns)
    
    users_collection = db['users_test']
    users_collection.drop()
    users_collection.insert_many(users)

seed_test_db()

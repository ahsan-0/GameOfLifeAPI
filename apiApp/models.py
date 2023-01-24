import json
from bson import ObjectId
from typing import Any
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status

# Create your models here.
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def find_patterns(request, pattern_collection):
    pattern_data = MongoJSONEncoder().encode(list(pattern_collection.find({})))
    return pattern_data


def find_single_pattern(request, id, pattern_collection):
    try:
        list(pattern_collection.find_one({"_id": ObjectId(id)}))
    except:
        return Response(
            {"msg": "Request contains invalid id."}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        pattern = MongoJSONEncoder().encode(
            list(pattern_collection.find({"_id": ObjectId(id)}))
        )
        return pattern


def find_users(request, users_collection):
    users_data = MongoJSONEncoder().encode(list(users_collection.find({})))
    return users_data


def find_single_user(request, username, users_collection):
    try:
        list(users_collection.find_one({"username": username}))
    except:
        return Response(
            {"msg": "Request contains invalid username."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        user = MongoJSONEncoder().encode(
            list(users_collection.find({"username": username}))
        )
        print(user)
        return user


def find_patterns_by_username(request, username, patterns_collection):
    try:
        list(patterns_collection.find_one({"username": username}))
    except:
        return Response(
            {"msg": "Request contains invalid username."},
            status=status.HTTP_404_NOT_FOUND,
        )
    user_patterns = MongoJSONEncoder().encode(
        list(patterns_collection.find({"username": username}))
    )
    return user_patterns

def insert_pattern(request, patterns_collection):
    request_body = request.data
    allowed_keys = ("pattern_body", "pattern_name", "username")
    username = request_body["username"]

    try:
        list(patterns_collection.find_one({"username": username }))
    except:
        return Response(
            {"msg": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    for key in request_body:
        if key not in allowed_keys:
            return Response({"msg": "Request body contains invalid key."},
            status=status.HTTP_400_BAD_REQUEST)
    
    if not all(k in request_body for k in allowed_keys):
        return Response({"msg": "Request body is missing a required key."}, 
        status=status.HTTP_400_BAD_REQUEST)

    for pattern in patterns_collection.find({}):
        if all((pattern.get(key) == value for key, value in request_body.items())) == True:
            return Response({"msg": "Pattern already exists in database."},
            status=status.HTTP_400_BAD_REQUEST)
    
    request_body["created_at"] = datetime.now()
    patterns_collection.insert_one(request_body)
    new_pattern = MongoJSONEncoder().encode(list(patterns_collection.find({
        "pattern_name": request_body["pattern_name"]
    })))

    return Response({ "pattern": json.loads(new_pattern)[0]}, status=status.HTTP_201_CREATED)


def insert_user(request, users_collection):
    request_body = request.data
    allowed_keys = ("account_owner", "username", "email", "avatar_url")

    for key in request_body:
        if key not in allowed_keys:
            return Response({"msg": "Request body contains invalid key."},
            status=status.HTTP_400_BAD_REQUEST)
    
    if not all(k in request_body for k in allowed_keys):
        return Response({"msg": "Request body is missing a required key."}, 
        status=status.HTTP_400_BAD_REQUEST)

    for user in users_collection.find({}):
        if all((user.get(key) == value for key, value in request_body.items())) == True:
            return Response({"msg": "User already exists in database."},
            status=status.HTTP_400_BAD_REQUEST)
    
    users_collection.insert_one(request_body)
    new_user = MongoJSONEncoder().encode(list(users_collection.find({
        "username": request_body["username"]
    })))

    return Response({ "user": json.loads(new_user)[0]}, status=status.HTTP_201_CREATED)
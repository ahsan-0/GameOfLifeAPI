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
        pattern_collection.find_one({"_id": ObjectId(id)})
        if len(list(pattern_collection.find({"_id": ObjectId(id)}))) == 0:
            raise Exception
    except:
        return Response(
            {"msg": "Request contains invalid id."}, status=status.HTTP_404_NOT_FOUND
        )

    pattern = MongoJSONEncoder().encode(
        list(pattern_collection.find({"_id": ObjectId(id)}))
    )
    return Response(json.loads(pattern)[0], status=status.HTTP_200_OK)


def find_users(request, users_collection):
    users_data = MongoJSONEncoder().encode(list(users_collection.find({})))
    return users_data


def find_single_user(id, users_collection):
    try:
        users_collection.find_one({"_id": ObjectId(id)})
        if len(list(users_collection.find({"_id": ObjectId(id)}))) == 0:
            raise Exception
    except:
        return Response(
            {"msg": "Request contains invalid id."}, status=status.HTTP_404_NOT_FOUND
        )
    user = MongoJSONEncoder().encode(list(users_collection.find({"_id": ObjectId(id)})))
    return Response(json.loads(user)[0], status=status.HTTP_200_OK)


def find_patterns_by_username(username, patterns_collection, users_collection):
    if users_collection.find_one({"username": username}) is None:
        return Response(
            {"msg": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    if patterns_collection.find_one({"username": username}) is None:
        return Response(
            {"msg": "There are no patterns for that user."},
            status=status.HTTP_404_NOT_FOUND,
        )

    user_patterns = MongoJSONEncoder().encode(
        list(patterns_collection.find({"username": username}))
    )
    return Response({"patterns": json.loads(user_patterns)}, status=status.HTTP_200_OK)


def insert_pattern(request, patterns_collection, users_collection):
    request_body = request.data
    allowed_keys = ("pattern_body", "pattern_name", "username")
    username = request_body["username"]

    if users_collection.find_one({"username": username}) is None:
        return Response(
            {"msg": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
        )

    for key in request_body:
        if key not in allowed_keys:
            return Response(
                {"msg": "Request body contains invalid key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    if not all(k in request_body for k in allowed_keys):
        return Response(
            {"msg": "Request body is missing a required key."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for pattern in patterns_collection.find({}):
        if (
            all((pattern.get(key) == value for key, value in request_body.items()))
            == True
        ):
            return Response(
                {"msg": "Pattern already exists in database."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    request_body["created_at"] = datetime.now()
    patterns_collection.insert_one(request_body)
    new_pattern = MongoJSONEncoder().encode(
        list(
            patterns_collection.find(
                {"pattern_name": request_body["pattern_name"], "username": username}
            )
        )
    )
    return Response(
        {"pattern": json.loads(new_pattern)[0]}, status=status.HTTP_201_CREATED
    )


def insert_user(request, users_collection):
    request_body = request.data
    allowed_keys = ("account_owner", "username", "email", "avatar_url")
    for key in request_body:
        if key not in allowed_keys:
            return Response(
                {"msg": "Request body contains invalid key."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    if not all(k in request_body for k in allowed_keys):
        return Response(
            {"msg": "Request body is missing a required key."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for user in users_collection.find({}):
        if all((user.get(key) == value for key, value in request_body.items())) == True:
            return Response(
                {"msg": "User already exists in database."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif user["username"] == request_body["username"]:
            return Response(
                {"msg": "That username is already taken."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    users_collection.insert_one(request_body)
    new_user = MongoJSONEncoder().encode(
        list(users_collection.find({"username": request_body["username"]}))
    )

    return Response({"user": json.loads(new_user)[0]}, status=status.HTTP_201_CREATED)


def update_pattern(request, id, patterns_collection):
    try:
        patterns_collection.find_one({"_id": ObjectId(id)})
        if len(list(patterns_collection.find({"_id": ObjectId(id)}))) == 0:
            raise Exception
    except:
        return Response(
            {"msg": "Request contains invalid id."}, status=status.HTTP_404_NOT_FOUND
        )
    request_body = request.data
    if bool(request_body) == False:
        return Response(
            {"msg": "Request body cannot be empty"}, status=status.HTTP_400_BAD_REQUEST
        )
    elif bool(request_body.get("pattern_name")) == False:
        return Response(
            {"msg": "Request is missing required property"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif len(request_body) > 1:
        return Response({"msg": "Request contains invalid property."},status=status.HTTP_400_BAD_REQUEST)
    patterns_collection.update_one({"_id": ObjectId(id)}, {"$set": request_body})
    updated_pattern = MongoJSONEncoder().encode(
        list(patterns_collection.find({"_id": ObjectId(id)}))
    )
    return Response(
        {"updated_pattern": json.loads(updated_pattern)[0]},
        status=status.HTTP_202_ACCEPTED,
    )


def update_user(request, id, users_collection, patterns_collection):
    request_body = {
        key: value for key, value in request.data.items() if value is not None
    }
    allowed_keys = ("account_owner", "username", "email", "avatar_url")
    try:
        users_collection.find_one({"_id": ObjectId(id)})
        if len(list(users_collection.find({"_id": ObjectId(id)}))) == 0:
            raise Exception
    except:
        return Response(
            {"msg": "Request contains invalid id."},
            status=status.HTTP_404_NOT_FOUND,
        )

    username = request_body.get("username", "x")
    if " " in username:
        return Response(
            {"msg": "Username cannot contain spaces."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for key in request_body:
        if key not in allowed_keys:
            return Response(
                {"msg": "Request body contains invalid key."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    if bool(request_body) == False:
        return Response(
            {"msg": "Request cannot be an empty object"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    old_usernames = []
    curr_usernames = []
    for patterns in patterns_collection.find({}):
        old_usernames.append(patterns["username"])
    for users in users_collection.find({}):
        curr_usernames.append(users["username"])

    updated_username = [k for k in old_usernames if k not in curr_usernames]

    users_collection.update_one({"_id": ObjectId(id)}, {"$set": request_body})

    if len(updated_username) != 0:
        patterns_collection.update_many(
            {"username": updated_username[0]}, {"$set": request_body}
        )

    updated_user = MongoJSONEncoder().encode(
        list(users_collection.find({"_id": ObjectId(id)}))
    )

    return Response(
        {"updated_user": json.loads(updated_user)[0]}, status=status.HTTP_202_ACCEPTED
    )


def delete_items(id, collection):
    try:
        collection.find_one({"_id": ObjectId(id)})
    except:
        return Response(
            {"msg": "Request contains invalid id."},
            status=status.HTTP_404_NOT_FOUND,
        )
    if collection.find_one({"_id": ObjectId(id)}) is None:
        return Response(
            {"msg": "Request contains invalid id."},
            status=status.HTTP_404_NOT_FOUND,
        )
    collection.delete_one({"_id": ObjectId(id)})
    return Response(status=status.HTTP_204_NO_CONTENT)

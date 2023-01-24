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
        return Response({"msg": "Request contains invalid id."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        pattern = MongoJSONEncoder().encode(list(pattern_collection.find({"_id": ObjectId(id)})))
        return Response(json.loads(pattern)[0])

def find_users(request, users_collection):
    users_data = MongoJSONEncoder().encode(list(users_collection.find({})))
    return users_data
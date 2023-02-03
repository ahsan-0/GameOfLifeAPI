from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo import MongoClient
from apiApp.models import (
    find_patterns,
    find_single_pattern,
    find_users,
    find_single_user,
    find_patterns_by_username,
    insert_pattern,
    insert_user,
    update_pattern,
    update_user,
    delete_items
)
import json
from apiApp.endpoints import endpoints

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
patterns_collection = db["patterns"]
users_collection = db["users"]


# Create your views here.
@api_view(["GET", "POST"])
def get_patterns(request):
    if request.method == "GET":
        return Response(
            {"patterns": json.loads(find_patterns(request, patterns_collection))},
            status=status.HTTP_200_OK,
        )
    elif request.method == "POST":
        return insert_pattern(request, patterns_collection, users_collection)


@api_view(["GET", "PUT", "DELETE"])
def single_pattern(request, id):
    if request.method == "GET":
        return find_single_pattern(request, id, patterns_collection)
    elif request.method == "PUT":
        return update_pattern(request, id, patterns_collection)
    elif request.method == "DELETE":
        return delete_items(id,patterns_collection)


@api_view(["GET", "POST"])
def get_users(request):
    if request.method == "GET":
        return Response(
            {"users": json.loads(find_users(request, users_collection))},
            status=status.HTTP_200_OK,
        )
    elif request.method == "POST":
        return insert_user(request, users_collection)

@api_view(["GET", "PUT", "DELETE"])
def get_single_user(request, id):
    if request.method == "GET":
        return find_single_user(id, users_collection)
    elif request.method == "PUT":
        return update_user(request, id, users_collection, patterns_collection)
    elif request.method == "DELETE":
        return delete_items(id,users_collection)


@api_view(["GET"])
def get_patterns_by_username(request, username):
    return find_patterns_by_username(username, patterns_collection, users_collection)

@api_view(["GET"])
def api_endpoints(request): return Response(endpoints)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def handler404(request, exception):
    return Response({"msg": "HTTP 404: not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def handler500(arg):
    return Response({"msg": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
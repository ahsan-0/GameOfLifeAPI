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
    insert_pattern
)
import json

# Create your views here.
client = MongoClient(
    "mongodb+srv://GNA7R:eerDKGruC7PUqjyx@rootcluster.i0un9uw.mongodb.net/?retryWrites=true&w=majority"
)
db = client["multiply_till_you_die_db"]
patterns_collection = db["patterns"]
users_collection = db["users"]


@api_view(["GET", "POST"])
def get_patterns(request):
  if request.method == 'GET':
    return Response(
        {"patterns": json.loads(find_patterns(request, patterns_collection))},
        status=status.HTTP_200_OK,
    )
  elif request.method == 'POST':
    return insert_pattern(request, patterns_collection)


@api_view(["GET"])
def get_single_pattern(request, id):
    return Response(
        json.loads(find_single_pattern(request, id, patterns_collection))[0]
    )


@api_view(["GET"])
def get_users(request):
    return Response(
        {"users": json.loads(find_users(request, users_collection))},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def get_single_user(request, username):
    return Response(
        json.loads(find_single_user(request, username, users_collection))[0]
    )


@api_view(["GET"])
def get_patterns_by_username(request, username):
    return Response(
        {
            "patterns": json.loads(
                find_patterns_by_username(request, username, patterns_collection)
            )
        },
        status=status.HTTP_200_OK,
    )

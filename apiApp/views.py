from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo import MongoClient
from apiApp.models import find_patterns, find_single_pattern, find_users
import json

# Create your views here.
client = MongoClient(
        "mongodb+srv://GNA7R:eerDKGruC7PUqjyx@rootcluster.i0un9uw.mongodb.net/?retryWrites=true&w=majority")
db = client['multiply_till_you_die_db']
patterns_collection = db['patterns']
users_collection = db['users']


@api_view(["GET"])
def get_patterns(request):
  return Response({'patterns':json.loads(find_patterns(request,patterns_collection))},status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_pattern(request, id):
  return find_single_pattern(request, id, patterns_collection)

@api_view(['GET'])
def get_users(request):
  return Response({'users':json.loads(find_users(request, users_collection))},status=status.HTTP_200_OK)

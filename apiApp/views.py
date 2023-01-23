from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from pymongo import MongoClient
from apiApp.models import find_patterns
import json
# Create your views here.
client = MongoClient(
        "mongodb+srv://GNA7R:eerDKGruC7PUqjyx@rootcluster.i0un9uw.mongodb.net/?retryWrites=true&w=majority")
db = client['multiply_till_you_die_db']
patterns_collection = db['patterns']

@api_view(['GET'])
def get_patterns(request):
  if request.method == 'GET':
    return Response({'patterns':json.loads(find_patterns(request,patterns_collection))},status=status.HTTP_200_OK)
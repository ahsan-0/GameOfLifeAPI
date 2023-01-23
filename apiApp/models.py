import json
from bson import ObjectId
from typing import Any
from datetime import datetime
# Create your models here.
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

def find_patterns(request,pattern_collection):
  # pattern_data = []
  for pattern in list(pattern_collection.find({})):
    print(pattern['created_at'].tostring())
#pattern_data = MongoJSONEncoder().encode(list(pattern_collection.find({})))
  # return pattern_data
  # print(pattern_data)
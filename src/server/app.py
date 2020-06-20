import os
import pymongo
from flask import Flask
from pprint import pprint

ADMIN_NAME = "SGP"
PASSWORD = "UxmwrTNrtbmrHzGp"

app = Flask(__name__)
uri = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(ADMIN_NAME, PASSWORD)

# connect to db and get cluster
cluster = pymongo.MongoClient(uri)

# get db from cluster 
db = cluster['StackedUp']

# get collection from db
collection = db['users']

# testing insert

# collection.insert_one({"_id": 0, "user-name":"omar", "user_items": [
#             {"name":"bread", "category": "carb",
#             "purchase_date": "9/6/2020", "expiration_date":"22/6/2020"}
#       ]
# })
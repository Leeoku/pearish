import os
import pymongo
from flask import Flask
from pprint import pprint
import api

app = Flask(__name__)
uri = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(api.ADMIN_NAME, api.PASSWORD)

# connect to db and get cluster
cluster = pymongo.MongoClient(uri)

# get db from cluster 
db = cluster['StackedUp']

# get collection from db
collection = db['users']

# testing insert

# collection.insert_one({"_id": 0, "user-name":"omar", "user_items": [
#             {"name":"milk", "category": "dairy",
#             "purchase_date": "10/6/2020", "expiration_date":"23/6/2020"}
#       ]
# })
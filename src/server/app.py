import os
import pymongo
from flask import Flask
from pprint import pprint

ADMIN_NAME = os.environ["ADMIN_NAME"]
PASSWORD = os.environ["PASSWORD"]

app = Flask(__name__)
uri = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(ADMIN_NAME, PASSWORD)
cluster = pymongo.MongoClient(uri)
db = cluster['StackedUp']
collection = db['users']
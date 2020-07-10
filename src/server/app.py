import os
import pymongo
import flask
from pprint import pprint
import api
import json, collections
import bson
#import bsonjs
#from bson.json_util import dumps as bdumps

app = flask.Flask(__name__)
url = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(api.ADMIN_NAME, api.PASSWORD)

# connect to db and get cluster
cluster = pymongo.MongoClient(url)

# get db from cluster 
db = cluster['StackedUp']

# get collection from db
collection = db['users']

# testing insert

# collection.insert_one({"_id": 0, "user_name":"omar", "user_items": [
#             {"name":"milk", "category": "dairy",
#             "purchase_date": "10/6/2020", "expiration_date":"23/6/2020"}
#       ]
# })

test = collection.find_one({"_id":0})
print(test)
d = bson.encode(test)
print(d)
d_text = bson.decode(d)
print(d_text)
# d = bdumps(test)
# #raw_bson = bsonjs.loads(test)
# print(test)
# print('Test is of type ' + str(type(test)))
# print('Json.dumps(test) is of type ' + str(type(json.dumps(test))))
# print(chr(d))
# print(type(d))



@app.route("/")
def my_index():
    #return flask.render_template("index.html", token=flask.json.loads(flask.json.dumps(test)))
    return flask.render_template("index.html", token= d_text)
app.run(debug=True)
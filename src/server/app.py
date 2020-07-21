import os
import sys
import pymongo
import flask 
from flask import render_template, request
from pprint import pprint
import api
import json
import collections
import bson
#import bsonjs
from bson import json_util
from flask_restful import Api, Resource
from flask.json import JSONEncoder, jsonify
from parse import *

app = flask.Flask(__name__)
restful_api = Api(app)
url = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(
    api.ADMIN_NAME, api.PASSWORD)

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

test = collection.find_one({"_id": 0})

@app.route("/user/upload", methods = ['POST'])
def upload_file():
    file = request.files['file']
    print(file)
    return "done"

@app.route("/")
def my_index():
    return flask.render_template("index.html", token=test)

# Response to get all user items, mapped to /user/


class UserCollection(Resource):
    def get(self):
        #user = collection.find_one({"user_name": user_name})
        container = []
        for user in collection.find():
            container.append(user)
        return json.loads(json_util.dumps(container))

# Response to add an entry, mapped to /user/create/<user_name>


class UserCollectionCreate(Resource):
    # NEED TO ADD PAYLOAD FROM PARSE.PY AND IDENTIFY WHICH USER IT IS, THIS POST IS A PLACEHOLDER
    def post(self, user_name):
        payload = {
            "user_name": user_name,
            "user_items": [{
                "cateogry": "",
                "count": "",
                "expiration_date": "",
                "name": "",
                "purchase_date": ""
            }]
        }
        collection.insert(payload)
        return f"{user_name} added"

# Response to get, update and delete one user


class UserCollectionName(Resource):
    def get(self, user_name):
        user = collection.find_one({"user_name": user_name})
        # return {"User": user}
        return json.loads(json_util.dumps(user))

    def delete(self, user_name):
        collection.delete_one({"user_name": user_name})
        return f"{user_name} deleted"

    def post(self, user_name):
        collection.update_one({"user_name": user_name})
        return f"{user_name} updated"

# Response to get and delete items
# Sample Object

# ['{"name": "carrot", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 1}',
# '{"name": "oranges", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 3}']


class UserCollectionItems(Resource):
    def get(self, user_name):
        user = collection.find_one({"user_name": user_name})
        items = user["user_items"]
        return{"Items": items}

    def post(self, user_name):
        # results = [{"name": "carrot", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 1}, 
        # {"name": "oranges", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 3}]
        (single,plural,matcher) = pattern_match()
        results = get_results(single,plural,matcher)
        for i in range(len(results)):
            #collection.update_many({"user_name": user_name}, {"$set":items[i]}, upsert = True)
            collection.update_many({"user_name": user_name}, {"$push": { "user_items" : results[i] }}, upsert = True)
        return f"Updated items for {user_name}"

restful_api.add_resource(UserCollection, '/user/')
restful_api.add_resource(UserCollectionCreate,
                         '/user/create/<string:user_name>')
restful_api.add_resource(UserCollectionName, '/user/<string:user_name>')
restful_api.add_resource(UserCollectionItems, '/user/<string:user_name>/items')

if __name__ == '__main__':
    # (single,plural,matcher) = pattern_match()
    # results = get_results(single,plural,matcher)
    # print(results)
    app.run(debug=True)

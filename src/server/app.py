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
from bson import json_util
from flask_restful import Api, Resource
from flask.json import JSONEncoder, jsonify
from parse import *
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
#from mongostuff import *

app = flask.Flask(__name__)
restful_api = Api(app)
# app.config['MONGO_URI'] = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(
#     api.ADMIN_NAME, api.PASSWORD)

url = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(
    api.ADMIN_NAME, api.PASSWORD)
app.config['MONGO_URI'] = url
app.config['SECRET_KEY'] = 'super secret key'


mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

# connect to db and get cluster
cluster = pymongo.MongoClient(url)
# cluster = pymongo.MongoClient('MONGO_URI')

# get db from cluster
db = cluster['StackedUp']

# get collection from db
collection = db['users']


@app.route("/users/upload", methods=['POST'])
def upload_file():
    file = request.files['file']
    print(file)
    return "done"

@app.route('/users/register', methods=["POST"])
def register():
    users = mongo.db.users
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
    user_items = []

    user_id = users.insert({
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created,
        'user_items': [],
        'user_name': str(email)
    })

    new_user = users.find_one({'_id': user_id})

    result = {'email': new_user['email'] + ' registered'}

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    users = mongo.db.users
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    response = users.find_one({'email': email})

    if response:
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity={
                'first_name': response['first_name'],
                'last_name': response['last_name'],
                'email': response['email']
            })
            result = jsonify({'token': access_token})
        else:
            result = jsonify({"error": "Invalid username and password"})
    else:
        result = jsonify({"result": "No results found"})
    return result


# Response to get all user items, mapped to /user/


class UserCollection(Resource):
    def get(self):
        container = []
        for user in collection.find():
            container.append(user)
        return json.loads(json_util.dumps(container))
  

# Response to add an entry, mapped to /user/create/<user_name>


# class UserCollectionCreate(Resource):
#     # NEED TO ADD PAYLOAD FROM PARSE.PY AND IDENTIFY WHICH USER IT IS, THIS POST IS A PLACEHOLDER
#     def post(self, user_name):
#         payload = {
#             "user_name": user_name,
#             "user_items": [{
#                 "cateogry": "",
#                 "count": "",
#                 "expiration_date": "",
#                 "name": "",
#                 "purchase_date": ""
#             }]
#         }
#         collection.insert(payload)
#         return f"{user_name} added"

# Response to get, update and delete one user
# defget (self, email)
# user = collection.find_one({email": email})
class UserCollectionName(Resource):
    def get(self, user_name):
        user = collection.find_one({"user_name": user_name})
        return json.loads(json_util.dumps(user))
        
    def delete(self, user_name):
        collection.delete_one({"user_name": user_name})
        return f"{user_name} deleted"

# Response to get and delete items
# Sample Object
# ['{"name": "carrot", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 1}',
# '{"name": "oranges", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 3}']



class UserCollectionItems(Resource):
    
    def db_update(id, data):
        collection.update_one(id, {"$set": data})

    def get(self, user_name):
        user = collection.find_one({"user_name": user_name})
        items = user["user_items"]
        return{"Items": items}

    def post(self, user_name):
        # results = [{"name": "carrot", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 1},
        # {"name": "beer", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 3}]
        user = collection.find_one({"user_name": user_name})
        (single, plural, matcher) = pattern_match()
        results = get_results(single, plural, matcher)


        for x in results:
            user['user_items'].append(x)

        db_update({"user_name": user_name}, user)

        return f"Updated items for {user_name}"
        # print(user)
        # collection.update_one({"user_name": user_name}, {"$set": {}})


        # (single, plural, matcher) = pattern_match()
        # results = get_results(single, plural, matcher)
        # for i in range(len(results)):
        #     #collection.update_many({"user_name": user_name}, {"$set":items[i]}, upsert = True)
        #     collection.update_many({"user_name": user_name}, {
        #                            "$push": {"user_items": results[i]}}, upsert=True)
        # return f"Updated items for {user_name}"



    def delete(self, user_name):
        item = {"name": "oranges", "category": "placeholder", "purchase_date": "07/21/20", "expiration_date": "08/04/20", "count": 3}
        item_name = item["name"]
        lookup = collection.find_one({"user_name": user_name})
        db_item = lookup.get('user_items')

        for index in range(0,len(db_item)):
            if db_item[index]["name"] == item_name:
                collection.update({"user_name":user_name}, {"$pull": {"user_items": db_item[index]}})
                return f"{item_name} deleted"
            else:
                continue
        return f"{item_name} not found"

        #         collection.update({"user_name":user_name}, {"$pull": {"user_items": db_item[index]["name"]}})
        #         return f"{item_name} deleted"
        #     return f"{item_name} not found"
        # for index, entry in enumerate(db_item):
        #     print(index, entry)
        #     # name = json.loads(entry).get("name")
        #     name = db_item[index]["name"]
        #     if name == item_name:
        #         collection.update({"user_name":user_name}, {"$pull": {"user_items": db_item[index]}})
        #         return f"{item_name} deleted"
        #     return f"No item found"
    


    def put(self, user_name):
        #sample incoming object
        item = {"name": "apple", "category": "applessuck", "purchase_date": "11/21/21", "expiration_date": "12/04/21", "count": 5}
        item_name = item["name"]
        item_category = item['category']
        item_purchase_date = item["purchase_date"]
        item_expiration_date = item["expiration_date"]
        item_count = item["count"]
        lookup = collection.find_one({"user_name": user_name})
        db_item = lookup.get('user_items')

        for i in range(0, len(db_item)):
            if lookup['user_items'][i]['name'] == item_name:
                lookup['user_items'][i]['category'] = item_category
                lookup['user_items'][i]["purchase_date"] = item_purchase_date
                lookup['user_items'][i]["expiration_date"] = item_expiration_date
                lookup['user_items'][i]['count'] = item_count
                print("True")              
                break
            else:
                continue
        collection.update_one({"user_name":user_name}, {"$set": lookup})
        return f"{item_name} has been updated"


restful_api.add_resource(UserCollection, '/user/')
# restful_api.add_resource(UserCollectionCreate,'/user/create/<string:user_name>')
restful_api.add_resource(UserCollectionName, '/user/<string:user_name>')
restful_api.add_resource(UserCollectionItems, '/user/<string:user_name>/items')

if __name__ == '__main__':
    # (single,plural,matcher) = pattern_match()
    # results = get_results(single,plural,matcher)
    # print(results)
    app.run(debug=True)

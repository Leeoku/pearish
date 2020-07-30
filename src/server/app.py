import os
import sys
import pymongo
import flask
from flask import flash, request, redirect, url_for,request
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
#from mongostuff import *, future use of helper functions
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
restful_api = Api(app)
# app.config['MONGO_URI'] = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(
#     api.ADMIN_NAME, api.PASSWORD)

UPLOAD_FOLDER = './img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
url = "mongodb+srv://{}:{}@stackedup-nr3iv.mongodb.net/StackedUp?retryWrites=true&w=majority".format(
    api.ADMIN_NAME, api.PASSWORD)
app.config['MONGO_URI'] = url
app.config['SECRET_KEY'] = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/users/upload", methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename =  "receipt." + file.filename.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "done"


# @app.route("/files", methods=['POST'])
# def files():
#     return "FILES HERE"

#Register Function
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
#Default payload for each collection 
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

#Login Function
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


# Response to get all user items, mapped to /users/

class UserCollection(Resource):
    def get(self):
        container = []
        for user in collection.find():
            container.append(user)
        return json.loads(json_util.dumps(container))

# Response to get specific collection for a user, mapped to /users/<string:user_name>
class UserCollectionName(Resource):
    def get(self, user_name):
        user = collection.find_one({"user_name": user_name})
        return json.loads(json_util.dumps(user))
        
    def delete(self, user_name):
        collection.delete_one({"user_name": user_name})
        return f"{user_name} deleted"

# Response to get and delete items
# Sample Object
# [{"name": "carrot", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 1},
# {"name": "oranges", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 3}]

#Made function for collection.update_one
def db_update(id, data):
    collection.update_one(id, {"$set": data})

#Response for item requests, mapped to /users/<string:<user_name>/items
class UserCollectionItems(Resource):
    
    def get(self, user_name):
        user = collection.find_one({"user_name": user_name})
        items = user["user_items"]
        return{"Items": items}

    # Add items to a user_items for specific user_name
    def post(self, user_name):
        # results = [{"name": "carrot", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 1},
        # {"name": "beer", "category": "placholder", "purchase_date": "07/18/20", "expiration_date": "08/01/20", "count": 3}]
        user = collection.find_one({"user_name": user_name})
        (single, plural, matcher) = pattern_match()
        results = get_results(single, plural, matcher)
        print(results)
        # Add new parsed item into user_items array
        for x in results:
            user['user_items'].append(x)
        #Update the Collection
        db_update({"user_name": user_name}, user)
        return f"Updated items for {user_name}"

    #Delete single item in user_items
    def delete(self, user_name):
        item = {"name": "oranges", "category": "placeholder", "purchase_date": "07/21/20", "expiration_date": "08/04/20", "count": 3}
        item_name = item["name"]
        lookup = collection.find_one({"user_name": user_name})
        db_item = lookup.get('user_items')

    #Look for a specific foodname, then delete that specific item in user_items
        for index in range(0,len(db_item)):
            if db_item[index]["name"] == item_name:
                collection.update_one({"user_name":user_name}, {"$pull": {"user_items": db_item[index]}})
                return f"{item_name} deleted"
            else:
                continue
        return f"{item_name} not found"

    #Look for a specific foodname, then update the collection object
    def put(self, user_name):
        #sample incoming object
        item = {"name": "oranges", "category": "orangesbetterthanapples", "purchase_date": "11/21/21", "expiration_date": "12/04/21", "count": 5}
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


restful_api.add_resource(UserCollection, '/users/')
# restful_api.add_resource(UserCollectionCreate,'/user/create/<string:user_name>')
restful_api.add_resource(UserCollectionName, '/users/<string:user_name>')
restful_api.add_resource(UserCollectionItems, '/users/<string:user_name>/items')

if __name__ == '__main__':
    # (single,plural,matcher) = pattern_match()
    # results = get_results(single,plural,matcher)
    # print(results)
    app.run(debug=True)

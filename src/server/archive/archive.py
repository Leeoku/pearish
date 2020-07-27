
# @app.route("/")
# def my_index():
#     return flask.render_template("index.html", token=test)


# testing insert

# collection.insert_one({"_id": 0, "user_name":"omar", "user_items": [
#             {"name":"milk", "category": "dairy",
#             "purchase_date": "10/6/2020", "expiration_date":"23/6/2020"}
#       ]
# })

# test = collection.find_one({"_id": 0}) 
 
 
 #PUT UPDATE TEST COKDE
        # db_update({"user_name", user_name}, db_item)
            # print(lookup['user_items'])
        #     # for k, v in lookup['user_items'][i].items():
        #     #     print(k, v)
        #     if lookup['user_items'][i]["name"] == item_name:
        #         lookup['user_items'][i]["category"] == item_category
        #         lookup['user_items'][i]["purchase_date"] == item_purchase_date
        #         lookup['user_items'][i]["expiration_date"] == item_expiration_date
        #         return f"{item_name} values have been updated"
            # else:
            #     return f"Could not find {item_name} "

            #SNAP ATTEMPT
            # if lookup['user_items'][i]['category'] == "placeholder":
            #     # print(lookup['user_items'][i]['category'])
            #     lookup['user_items'][i]['category'] = "Diary"
            # if lookup['user_items'][i]['name'] == "carrot":
            #     # print(lookup['user_items'][i]['name'])
            #     lookup['user_items'][i]['name'] = "YEET"
        # print(lookup)
        #db_update({"user_name", user_name}, lookup)

        
#KENS INITIAL ATTEMPT FOR PUT API
        # #Try just updating item_category first
        # for index, entry in enumerate(db_item):
        #     name = json.loads(entry).get("name") #I THINK WE
        #     if name == item_name:
        #         # print(db_item[index])
        #         # print(name)
        #         # print(item_category)
        #         collection.update_one({"user_name.user_items":item_name}, 
        #         {"$set": {"user_items.$.category": item_category}})             
        #         # collection.update_one({"user_name.user_items": item_name},
        #         # {"$set": {"category": item_category}})
        #         return True
        # #         #collection.update({"user_name":user_name}, {"$set": {"user_items": db_item[index]}},{"set":{"category": db_category}}, upsert = True)
        # #         collection.update_one({"user_name":user_name}, {"set":{"category": item_category}})
        # #         return f"Updated"
        # return db_item
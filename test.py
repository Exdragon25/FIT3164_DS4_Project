from pymongo import MongoClient
from pprint import pprint


client = MongoClient()
db = client.fit3164
dish_coll = db.Dish_collection

result = dish_coll.find({"cuisine":{"$in":['American','Chinese']}}, {"course":{"$in":['Salad']}})
for doc in result:
    print(doc)
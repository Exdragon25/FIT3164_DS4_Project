from pymongo import MongoClient
from pprint import pprint


client = MongoClient()
db = client.fit3164
dish_coll = db.Dish_collection

user_Input = "chicken"
cuisine_input = ["Chinese"]
course_input = []
taste_input = ["sweet", "salty"]

if user_Input == "":
    user_Input = "."

if len(cuisine_input) == 0 and len(course_input) == 0:
    result = dish_coll.find({'name': {"$regex": user_Input, "$options": "$i"}})
elif len(cuisine_input) == 0 and len(course_input) != 0:
    result = dish_coll.find({'name': {"$regex": user_Input, "$options": "$i"},
                             "course": {'$in': course_input}})
elif len(cuisine_input) != 0 and len(course_input) == 0:
    result = dish_coll.find({'name': {"$regex": user_Input, "$options": "$i"},
                             "cuisine": {"$in": cuisine_input}})
else:
    result = dish_coll.find({'name': {"$regex": user_Input, "$options": "$i"}, "cuisine": {"$in": cuisine_input},
                             "course": {'$in': course_input}})
output_coll = []

if result is not None:
    if result == "Please do some selection":
        pass
    else:
        for doc in result:
            add = True
            for i in taste_input:
                if doc['taste'] is not None:
                    if doc['taste'].get(i) is None:
                        add = False
                        break
                    if doc['taste'].get(i) < 0.8:
                        add = False
                        break
            if add:
                output_coll.append(doc['name'])
pprint(output_coll)

result = dish_coll.find({"cuisine": {"$or": ['American', 'Chinese']}},
                        {"course": {"$or": ['Salad']}})
for doc in result:
    print(doc)

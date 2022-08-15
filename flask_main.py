from pprint import pprint

from flask import Flask, jsonify, url_for, render_template, request
import config
import json, time, datetime
# import pysolr
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(config)  # 导入config


@app.route("/about/result")
def about_result():
    context = {"username": "ahajhdhisfsi"}

    return render_template("search_result.html")


@app.route("/", methods=['get', 'post'])
def search():
    if request.method == 'POST':
        output = {"Search": request.form.get('Search'),
                  'Cuisine': request.form.getlist('Cuisine'),
                  'Taste': request.form.getlist('Taste'),
                  'Course': request.form.getlist('Course')}
        render_result(output)
        return "successful"
    return render_template('homepage.html')


@app.route("/signin", methods=['post'])
def login():
    return render_template('signin.html')

def login_register(call_mode: str, user_detail_dict: dict):
    """
    This function will provide login/ registration database module by calling from webpage
    :param call_mode: string for indecate what you want to do with user
                "login" : for user login
                "register" : for user registration
                "view_history" for view history to do ML and recommendation
                "update_history" for update history when user viewing some dishes
    :param user_detail_dict: dictionary of user input, mostly are username and password
    :return: a list for showing 5 situations:
                1. "Success" For registration
                2. "This username has already been registered" For registration failed
                3. "The username or password may be wrong, please try again" For login failed
                4. "Login successfully" For login
                5. A list of dish_name that user has searched. For recommendation
                6. "Update history successfully" For add history
    """
    result = None
    client = MongoClient()
    db = client.fit3164
    usr_coll = db.user_collection
    pass


def render_result(input_dict):
    """
    :param input_dict: a dictionary with user input data for searching
    :return: a render_template function with a new web pages
    处理多种可能输入
    """
    result = None
    client = MongoClient()
    db = client.fit3164
    dish_coll = db.Dish_collection

    print(input_dict)

    userinput = input_dict["Search"]  # String
    cuisine_input = input_dict["Cuisine"]  # List = 1
    taste_input = input_dict["Taste"]  # list <= 2
    course_input = input_dict["Course"]  # list <= 3

    taste_coll = []
    for tas in taste_input:
        temp = "taste." + str(tas)
        taste_coll.append(temp)
    print(taste_coll)

    print("有什么情况")
    print(len(taste_coll), len(cuisine_input), len(course_input))
    situation_marker = str(len(taste_coll)) + str(len(cuisine_input)) + str(len(course_input))

    result = dish_coll.find({'name': {"$regex": userinput, "$options": "$i"}})

    # Here start handle situation.
    # 0 0 0
    if situation_marker == "000":
        print("000")
        if len(userinput) == 0:
            result = "Please do some selection"
        else:
            result = dish_coll.find({'name': {"$regex": userinput, "$options": "$i"}})
    # 0 0 1
    elif situation_marker == "001":
        print('001')
        if len(userinput) == 0:
            result = dish_coll.find(
                {"course": course_input}
            )
        else:
            result = dish_coll.find(
                {'name': {"$regex": userinput, "$options": "$i"},
                 "course": course_input}
            )
    # 0 0 2
    elif situation_marker == "002":
        print('002')
        if len(userinput) == 0:
            result = dish_coll.find(
                {"$and": [{"course": course_input[0]},
                          {"course": course_input[1]}]})
        else:
            result = dish_coll.find(
                {'name': {"$regex": userinput, "$options": "$i"},
                 "$and": [{"course": course_input[0]},
                          {"course": course_input[1]}]}
            )
    # 0 0 3
    elif situation_marker == "003":
        print('003')
        if len(userinput) == 0:
            result = dish_coll.find(
                {"$and": [{"course": course_input[0]},
                          {"course": course_input[1]},
                          {"course": course_input[2]}]}
            )
        else:
            result = dish_coll.find(
                {'name': {"$regex": userinput, "$options": "$i"},
                 "$and": [{"course": course_input[0]},
                          {"course": course_input[1]},
                          {"course": course_input[2]}]}
            )
    # -------------------------------------
    # 0 1 0
    elif situation_marker == "010":
        print('010')
        if len(userinput) == 0:
            result = dish_coll.find({"cuisine": cuisine_input[0]})
        else:
            result = dish_coll.find({'name': {"$regex": userinput, "$options": "$i"}, "cuisine": cuisine_input[0]})
    # 0 1 1
    elif situation_marker == "011":
        print('011')
        if len(userinput) == 0:
            result = dish_coll.find(
                {"cuisine": cuisine_input[0], "course": course_input}
            )
        else:
            result = dish_coll.find(
                {'name': {"$regex": userinput, "$options": "$i"},
                 "cuisine": cuisine_input[0],
                 "course": course_input}
            )
    # 0 1 2
    elif situation_marker == "012":
        print('012')
        if len(userinput) == 0:
            result = dish_coll.find(
                {"cuisine": cuisine_input[0],
                 "$and": [{"course": course_input[0]},
                          {"course": course_input[1]}]})
        else:
            result = dish_coll.find(
                {'name': {"$regex": userinput, "$options": "$i"},
                 "cuisine": cuisine_input[0],
                 "$and": [{"course": course_input[0]},
                          {"course": course_input[1]}]}
            )
    # 0 1 3
    elif situation_marker == "013":
        print('013')
        if len(userinput) == 0:
            result = dish_coll.find(
                {"cuisine": cuisine_input[0],
                 "$and": [{"course": course_input[0]},
                          {"course": course_input[1]},
                          {"course": course_input[2]}]}
            )
        else:
            result = dish_coll.find(
                {'name': {"$regex": userinput, "$options": "$i"},
                 "cuisine": cuisine_input[0],
                 "$and": [{"course": course_input[0]},
                          {"course": course_input[1]},
                          {"course": course_input[2]}]}
            )
    # 000 - 013 above
    # 100 - 113 below
    # 1 0 0
    elif situation_marker == "100":
        print('100')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
            })
    # 1 0 1
    elif situation_marker == "101":
        print('101')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
                "course": course_input[0]  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
                "course": course_input[0]
            })
    # 1 0 2
    elif situation_marker == "102":
        print('102')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]
            })
    # 1 0 3
    elif situation_marker == "103":
        print('103')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]
            })
    # -------------------------------------
    # 1 1 0
    elif situation_marker == "110":
        print('110')
        if len(userinput) == 0:
            result = dish_coll.find({
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8},
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8},
            })
    # 1 1 1
    elif situation_marker == "111":
        print('111')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
                "cuisine": cuisine_input[0],
                "course": course_input[0]  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
                "cuisine": cuisine_input[0],
                "course": course_input[0]
            })
    # 1 1 2
    elif situation_marker == "112":
        print('112')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
                "cuisine": cuisine_input[0],
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
                "cuisine": cuisine_input[0],
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]
            })
    # 1 1 3
    elif situation_marker == "113":
        print('113')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8},
                "cuisine": cuisine_input[0],
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8},
                "cuisine": cuisine_input[0],
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]
            })

    # 200 - 213 below:

    elif situation_marker == "200":
        print('200')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
            })
    # 2 0 1
    elif situation_marker == "201":
        print('201')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "course": course_input[0]
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "course": course_input[0]
            })
    # 2 0 2
    elif situation_marker == "202":
        print('202')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]
            })
    # 2 0 3
    elif situation_marker == "203":
        print('203')
        if len(userinput) == 0:
            result = dish_coll.find({
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]
            })
    # -------------------------------------
    # 2 1 0
    elif situation_marker == "210":
        print('210')
        if len(userinput) == 0:
            result = dish_coll.find({
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
            })
    # 2 1 1
    elif situation_marker == "211":
        print('211')
        if len(userinput) == 0:
            result = dish_coll.find({
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "course": course_input[0]
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "course": course_input[0]
            })
    # 2 1 2
    elif situation_marker == "212":
        print('212')
        if len(userinput) == 0:
            result = dish_coll.find({
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]}]
            })
    # 2 1 3
    elif situation_marker == "213":
        print('213')
        if len(userinput) == 0:
            result = dish_coll.find({
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]
            })
        else:
            result = dish_coll.find({
                'name': {"$regex": userinput, "$options": "$i"},
                "cuisine": cuisine_input[0],
                taste_coll[0]: {"$gte": 0.8}, taste_coll[1]: {"$gte": 0.8},  # conjunction
                "$and": [{"course": course_input[0]},
                         {"course": course_input[1]},
                         {"course": course_input[2]}]
            })

    print(result)

    output_coll = []
    if result is not None:
        if result == "Please do some selection":
            return result
        else:
            for doc in result:
                output_coll.append(doc['name'])
    pprint(output_coll)
    return output_coll  # {'name': 'Three-Pea Salad'}


def update_database():
    # result = collname.update_one({"package": "MonITTour"},
    #                              { "$set": { "name": "Monash IT Faculty Tour"}})
    pass


if __name__ == '__main__':
    app.run(debug=True)

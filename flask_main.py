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
    if request.method == 'post':
        output = {"Search": request.form.get('Search'),
                  'Cuisine': request.form.getlist('Cuisine'),
                  'Taste': request.form.getlist('Taste'),
                  'Course': request.form.getlist('Course')}
        render_result(output)
        return "successful"
    return render_template('homepage.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        # return "successful"

        for i in user:      # idea
            if i['uname'] == uname and i['pwd'] == pwd:
                return "Login Successfully"         # 再写一个跳转到原网页的function
            elif i['uname'] == uname and i['pwd'] != pwd:
                return render_template("login.html", msg="Wrong password, please try again.")
            else:
                return render_template("login.html", msg="User not found. Please register first.")

    return render_template("login.html")


def login_register(call_mode: str, user_detail_dict: dict):
    """
    This function will provide login/ registration database module by calling from webpage
    :param call_mode: string for indicate what you want to do with user
                "login" : for user login
                "register" : for user registration
                "view_history" for view history to do ML and recommendation
                "update_history" for update history when user viewing some dishes
    :param user_detail_dict: dictionary of user input, mostly are username and password
    :return: a list for showing 5 situations:
                1. "success" For registration
                2. "This username has already been registered" For registration failed
                3. "The username or password may be wrong, please try again" For login failed
                4. "login successfully" For login
                5. A list of dish_name that user has searched. For recommendation
                6. "Update history successfully" For add history
    """
    result = None
    client = MongoClient()
    db = client.fit3164
    usr_coll = db.user_collection

    username = user_detail_dict["username"]  # string
    password = user_detail_dict["password"]  # string
    user_history = user_detail_dict["user_history"]  # list with only 1 record

    if call_mode == "login":
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) == 1:  # if someone have same username, check the password:
            user_db = co[0]  # pick the user info from cursor
            if user_db["password"] == password:
                return "login successfully"
            else:  # if password is wrong.
                return "The username or password may be wrong, please try again"
        else:  # if no this user
            return "The username or password may be wrong, please try again"

    elif call_mode == "register":
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) != 0:  # if someone have same username
            return "This username has already been registered"
        else:  # if this username is valid.
            temp = {"username": username, "password": password, "user_history": []}
            return usr_coll.insert_one(temp)

    elif call_mode == "view_history":
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) == 1:  # if someone have same username:
            user_db = co[0]  # pick the user info from cursor
            return user_db["user_history"]  # return the history array.

        else:  # if no this user
            return "The username or password may be wrong, please try again"

    elif call_mode == "update_history":
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) == 1:  # if someone have same username:
            user_db = co[0]  # pick the user info from cursor
            history_list: list = user_db["user_history"] # take history from db
            if len(history_list) <= 15: # if less than 15 history
                history_list.append(user_history[0])
                result = user_db.update_one(
                    {"username": username},
                    {
                        "$set": {"user_history": history_list}
                    }
                )
                update_count = result.matched_count # this should be 1
                return "update success: " + str(update_count)

            else:  # if over 15 history, remove the oldest one:
                history_list.pop(0)
                # and insert new one:
                history_list.append(user_history[0])
                result = user_db.update_one(
                    {"username": username},
                    {
                        "$set": {"user_history": history_list}
                    }
                )
                update_count = result.matched_count # this should be 1
                return "update success: " + str(update_count)

        else:  # if no this user
            return "The username or password may be wrong, please try again"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        # return "successful"

        for i in user:      # idea
            if i['uname'] == uname:
                return render_template("register.html", msg="username already exists, please re-entry.")
            else:
                return render_template("login.html", msg="Account created successfully.")    # 再写一个成功跳转原网页的function

    return render_template("register.html")



def render_result(input_dict):
    """
    Function for handling the search input and do query on db
    :param input_dict: a dictionary with user input data for searching
    :return: a render_template function with a new web pages
    处理多种可能输入 NER
    """
    client = MongoClient()
    db = client.fit3164
    dish_coll = db.Dish_collection

    print(input_dict)

    user_input = input_dict["Search"]  # String
    cuisine_input = input_dict["Cuisine"]  # List = 1
    taste_input = input_dict["Taste"]  # list <= 2
    course_input = input_dict["Course"]  # list <= 3

    if user_input == "":
        user_input = "."

    if len(cuisine_input) == 0 and len(course_input) == 0:  # if no cuisine and course selection.
        result = dish_coll.find({'name': {"$regex": user_input, "$options": "$i"}})
    elif len(cuisine_input) == 0 and len(course_input) != 0:  # if only have course selection.
        result = dish_coll.find({'name': {"$regex": user_input, "$options": "$i"},
                                 "course": {'$in': course_input}})
    elif len(cuisine_input) != 0 and len(course_input) == 0:  # if only have cuisine selection.
        result = dish_coll.find({'name': {"$regex": user_input, "$options": "$i"},
                                 "cuisine": {"$in": cuisine_input}})
    else:  # if both of them have been selected.
        result = dish_coll.find({'name': {"$regex": user_input, "$options": "$i"}, "cuisine": {"$in": cuisine_input},
                                 "course": {'$in': course_input}})
    output_coll = []
    if result is not None:
        if result == "Please do some selection":
            return output_coll
        else:  # Do a filter if the user has selected some taste options.
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
    return output_coll


def update_database():
    # result = collname.update_one({"package": "MonITTour"},
    #                              { "$set": { "name": "Monash IT Faculty Tour"}})
    pass


if __name__ == '__main__':
    app.run(debug=True)

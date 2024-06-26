import ast
import datetime
import json
import random
import re
import secrets
import string
import time
import urllib.parse

import nltk
import numpy as np
import pandas as pd
import pymongo
import unidecode
from flask import (Flask, jsonify, make_response, redirect, render_template,
                   request, session, url_for)
from nltk import WordNetLemmatizer
from pymongo import MongoClient

import config
import most_similar_dish as ml

app = Flask(__name__)
app.config.from_object(config)  # 导入config
app.config['SECRET_KEY'] = 'EJFHhiufwh893hf'


@app.route('/get_cookie')
def get_cookie():
    c = request.cookies.get("session_id")
    return c


@app.route("/", methods=['GET', 'POST'])
def passingfunc():
    """
    passing user selection on homepage.
    :return: redirect to webpage
    """
    current_user = get_current_user()
    user_his = get_current_user_his()
    dly_recom_recipe = []
    if user_his is None or len(user_his) == 0:
        client = MongoClient()
        db = client.fit3164
        dish_coll = db.Dish_collection
        cursor = dish_coll.aggregate([{"$sample": {"size": 4}}])
        for doc in cursor:
            dly_recom_recipe.append(doc['name'])
    else:
        print(user_his)
        ml_recom = ml.find_similar_recipes(ml.aggregate_vectors(user_his), user_his)
        print(ml_recom)
        dly_recom_recipe = random.sample(ml_recom, 4)

    if request.method == 'POST':
        output = {'search': request.form.get('search'),
                  'cuisine': request.form.getlist('cuisine'),
                  'taste': request.form.getlist('taste'),
                  'course': request.form.getlist('course')}
        return redirect("http://127.0.0.1:5000/1/search?" + urllib.parse.urlencode(output, doseq=True))
    return render_template('homepage.html', current_user=current_user, dly_recom_recipe=dly_recom_recipe)


@app.route('/<int:page_number>/search', methods=['GET', 'POST'])
def search(page_number):
    """
    rendering search result webpages, including filter and multiple pages
    """
    current_user = get_current_user()
    if request.method == 'POST' and request.form['submit_button'] == 'next_page':
        next_page_number = page_number + 1
        full_path = request.full_path.split("/")
        return redirect("http://127.0.0.1:5000/" + str(next_page_number) + "/" + full_path[-1])
    elif request.method == 'POST' and request.form['submit_button'] == 'previous_page':
        next_page_number = page_number - 1
        full_path = request.full_path.split("/")
        return redirect("http://127.0.0.1:5000/" + str(next_page_number) + "/" + full_path[-1])
    elif request.method == 'POST' and (
            request.form['submit_button'] == 'apply' or request.form['submit_button'] == 'search'):
        output = {'search': request.form.get('search'),
                  'cuisine': request.form.getlist('cuisine'),
                  'taste': request.form.getlist('taste'),
                  'course': request.form.getlist('course')}
        return redirect("http://127.0.0.1:5000/1/search?" + urllib.parse.urlencode(output, doseq=True))
    # choose page number action
    elif request.method == 'POST' and request.form['submit_button'] is not None:
        next_page_number = int(request.form['submit_button'])
        full_path = request.full_path.split("/")
        return redirect("http://127.0.0.1:5000/" + str(next_page_number) + "/" + full_path[-1])

    search = request.args.get('search')
    cuisine = request.args.getlist('cuisine')
    taste = request.args.getlist('taste')
    course = request.args.getlist('course')
    search = search.replace("_", " ")
    for i in range(len(course)):
        course[i] = course[i].replace("_", " ")
    result = render_result(search, cuisine, taste, course)
    num_result = len(result)
    max_pages = len(result) // 40 + 1
    if len(result) > page_number * 40:
        result = result[(page_number - 1) * 40:page_number * 40 - 1]
        next_page = True
    else:
        result = result[(page_number - 1) * 40:]
        next_page = False

    previous_page = False
    if page_number > 1:
        previous_page = True

    pages = cal_nearest_10_page(page_number, max_pages)
    show_pages = True
    if len(pages) <= 1:
        show_pages = False

    mid_index = len(result) // 2
    result_right = result[:mid_index]
    result_left = result[mid_index:]
    print(result)
    return render_template("searchpage.html", result=result, result_right=result_right, result_left=result_left,
                           next_page=next_page, previous_page=previous_page, current_user=current_user,
                           pages=pages, current_page=page_number, num_result=num_result, show_pages=show_pages)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    For user to login, set cookies
    :return:
    """
    if request.method == 'POST':
        user_info = dict(username=request.form.get('uname'), password=request.form.get('pwd'))
        result = login_register("login", user_info)  # string
        if len(result) == 22:  # length of session id is 22
            resp = make_response(redirect('/'))
            resp.set_cookie('session_id', result, max_age=36000)
            return resp
        else:
            return result
    return render_template("login.html")


@app.route("/<string:recipe_name>/", methods=['GET', 'POST'])
def show_recipe(recipe_name):
    """
    show detail webpage of recipes
    """
    if recipe_name != "favicon.ico" and recipe_name != " ":
        current_user = get_current_user()
        client = MongoClient()
        db = client.fit3164
        usr_coll = db.user_collection
        dish_coll = db.Dish_collection

        if current_user:
            usr_coll.update_one(
                {'username': current_user},
                {'$addToSet': {'user_history': recipe_name}})
        cursor = dish_coll.find({'name': recipe_name})
        result = []
        for doc in cursor:
            result.append(doc)
        cuisine = result[0]['cuisine']
        course = result[0]['course']
        ingredients = result[0]['ingredient_array']
        instructions = result[0]['instructions']
        num_ner = len(ingredients)
        num_NER = str(num_ner) + " ingredients"

        if request.method == 'POST':
            output = {'search': request.form.get('search')}
            return redirect("http://127.0.0.1:5000/1/search?" + urllib.parse.urlencode(output, doseq=True))

        return render_template("resultpage.html",
                               recipe_name=recipe_name, cuisine=cuisine, course=course,
                               ingredients=ingredients, instructions=instructions, num_NER=num_NER,
                               current_user=current_user)


def get_current_user():
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        client = MongoClient()
        db = client.fit3164
        usr_coll = db.user_collection
        search_result = usr_coll.find({'session_id': session_id})
        cur_user = []
        for doc in search_result:
            cur_user.append(doc)
        return cur_user[0]["username"]
    else:
        return None


def get_current_user_his():
    """
    directly query the user's history by cookies
    """
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        client = MongoClient()
        db = client.fit3164
        usr_coll = db.user_collection
        search_result = usr_coll.find({'session_id': session_id})
        cur_user_his = []
        for doc in search_result:
            cur_user_his.append(doc)
        return cur_user_his[0]["user_history"]
    else:
        return None


def login_register(call_mode: str, user_detail_dict: dict):
    """
    This function will provide login/ registration database module by calling from webpage
    :param call_mode: string for indicate what you want to do with user
                "login" : for user login
                "register" : for user registration
                "view_history" for view history to do ML and recommendation [not use]
                "update_history" for update history when user viewing some dishes [not use]
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

    if call_mode == "login":
        search_result = usr_coll.find({"username": username})

        co = []
        js = """<script> alert("Incorrect username or password, please try again.")</script>"""
        for doc in search_result:
            co.append(doc)

        if len(co) == 1:  # if someone have same username, check the password:
            user_doc = co[0]  # pick the user info from cursor
            if user_doc["password"] == password:
                return user_doc["session_id"]
            else:  # if password is wrong.
                return render_template("login.html") + js
        else:  # if no this user
            return render_template("login.html") + js

    elif call_mode == "register":
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) != 0:  # if someone have same username
            js = """<script> alert("This username has already been registered.")</script>"""
            return render_template("register.html") + js
        else:  # if this username is valid.
            session_id = secrets.token_urlsafe(16)
            temp = {"session_id": session_id, "username": username, "password": password, "user_history": []}
            usr_coll.insert_one(temp)
            resp = make_response(redirect('/'))
            resp.set_cookie('session_id', session_id, max_age=36000)
            return resp

    elif call_mode == "view_history":
        user_history = user_detail_dict["user_history"]  # list with only 1 record
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) == 1:  # if someone have same username:
            user_doc = co[0]  # pick the user info from cursor
            return user_doc["user_history"]  # return the history array.

        else:  # if no this user
            return "The username or password may be wrong, please try again."

    elif call_mode == "update_history":
        user_history = user_detail_dict["user_history"]  # list with only 1 record
        search_result = usr_coll.find({"username": username})

        co = []
        for doc in search_result:
            co.append(doc)

        if len(co) == 1:  # if someone have same username:
            user_doc = co[0]  # pick the user info from cursor
            history_list: list = user_doc["user_history"]  # take history from db
            if len(history_list) <= 15:  # if less than 15 history
                history_list.append(user_history[0])
                result = user_doc.update_one(
                    {"username": username},
                    {
                        "$set": {"user_history": history_list}
                    }
                )
                update_count = result.matched_count  # this should be 1
                return "update success: " + str(update_count)

            else:  # if over 15 history, remove the oldest one:
                history_list.pop(0)
                # and insert new one:
                history_list.append(user_history[0])
                result = user_doc.update_one(
                    {"username": username},
                    {
                        "$set": {"user_history": history_list}
                    }
                )
                update_count = result.matched_count  # this should be 1
                return "update success: " + str(update_count)

        else:  # if no this user
            return "The username or password may be wrong, please try again."


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_info = dict(username=request.form.get('uname'), password=request.form.get('pwd'))
        # return "successful"
        result = login_register("register", user_info)
        return result

    return render_template("register.html")


def render_result(ingredient, cuisine, taste, course):
    """
    deal with user search input and return a list of recipe name
    :param ingredient:
    :param cuisine:
    :param taste:
    :param course:
    :return: list of recipe name
    """

    def ingredient_parser(ingreds):
        measures = [
            "teaspoon",
            "t",
            "tsp.",
            "tablespoon",
            "T",
            "tbl.",
            "tb",
            "tbsp.",
            "fluid ounce",
            "fl oz",
            "gill",
            "cup",
            "c",
            "pint",
            "p",
            "pt",
            "fl pt",
            "quart",
            "q",
            "qt",
            "fl qt",
            "gallon",
            "g",
            "gal",
            "ml",
            "milliliter",
            "millilitre",
            "cc",
            "mL",
            "l",
            "liter",
            "litre",
            "L",
            "dl",
            "deciliter",
            "decilitre",
            "dL",
            "bulb",
            "level",
            "heaped",
            "rounded",
            "whole",
            "pinch",
            "medium",
            "slice",
            "pound",
            "lb",
            "#",
            "ounce",
            "oz",
            "mg",
            "milligram",
            "milligramme",
            "g",
            "gram",
            "gramme",
            "kg",
            "kilogram",
            "kilogramme",
            "x",
            "of",
            "mm",
            "millimetre",
            "millimeter",
            "cm",
            "centimeter",
            "centimetre",
            "m",
            "meter",
            "metre",
            "inch",
            "in",
            "milli",
            "centi",
            "deci",
            "hecto",
            "kilo",
        ]

        if isinstance(ingreds, list):
            ingredients = ingreds
        else:
            ingredients = ast.literal_eval(ingreds)

        # remove all the punctuations
        translator = str.maketrans("", "", string.punctuation)
        # initialize WordNetlemmatizer, WordNetlemmatizer can find the base of a word, for example, apples -> apple
        lemmatizer = WordNetLemmatizer()
        ingred_list = []
        for i in ingredients:
            i.translate(translator)
            # split up hyphens and spaces
            items = re.split(" |-", i)
            # remove the words containing non-alphabet letters
            items = [word for word in items if word.isalpha()]
            # every word to lowercase
            items = [word.lower() for word in items]
            # remove accents
            items = [
                unidecode.unidecode(word) for word in items
            ]
            # Lemmatize words so we can compare words to measuring words
            items = [lemmatizer.lemmatize(word) for word in items]
            stop_words = set(nltk.corpus.stopwords.words('english'))
            items = [word for word in items if word not in stop_words]
            # Gets rid of measuring words/phrases, e.g. heaped teaspoon
            items = [word for word in items if word not in measures]

            if items:
                word = " ".join(items)
                if word not in ingred_list:
                    ingred_list.append(word)
        return ingred_list

    client = MongoClient()
    db = client.fit3164
    dish_coll = db.Dish_collection

    add_result = None
    result = None
    ingredient_search = False
    empty_input = False

    # if empty input, then search everything
    if ingredient == "":
        empty_input = True
        ingredient = "."
    # if contains , then search ingredient
    elif ingredient.__contains__(","):
        ingredient_search = True

    # if input has no comma, search if it matches the name
    if not ingredient_search:
        # no cuisine and course selected
        if len(cuisine) == 0 and len(course) == 0:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "i"}})
        # only course selected
        elif len(cuisine) == 0 and len(course) != 0:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "i"},
                                     "course": {'$in': course}})
        # only cuisine selected
        elif len(cuisine) != 0 and len(course) == 0:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "i"},
                                     "cuisine": {"$in": cuisine}})
        # cuisine and course are selected
        else:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "i"}, "cuisine": {"$in": cuisine},
                                     "course": {'$in': course}})

    # do not need additional search if empty input
    # If user input a words without comma, or user input a list of ingredient,
    # we do an additional search. Because a single word without comma may also be an ingredient, not a recipe name.
    if not empty_input:
        if ingredient_search:
            user_input_li = ingredient.split(",")
            # we use ingredient parser to clean up the input
            ingredient = ingredient_parser(user_input_li)
        else:
            # if input is a single word, we make it into a list, so we can do $in query
            ingredient = [ingredient]
            # similar code to above
        if len(cuisine) == 0 and len(course) == 0:
            add_result = dish_coll.find({'NER': {"$in": ingredient}})
        elif len(cuisine) == 0 and len(course) != 0:
            add_result = dish_coll.find({'NER': {"$in": ingredient},
                                         "course": {'$in': course}})
        elif len(cuisine) != 0 and len(course) == 0:
            add_result = dish_coll.find({'NER': {"$in": ingredient},
                                         "cuisine": {"$in": cuisine}})
        else:
            add_result = dish_coll.find({'NER': {"$in": ingredient}, "cuisine": {"$in": cuisine},
                                         "course": {'$in': course}})

    output_coll = []
    # we lastly filter the result with taste chosen
    if result is not None:
        for doc in result:
            add = True
            # do not add into list if taste is not what isn't wants or taste data == None
            for i in taste:
                if doc['taste'] is not None:
                    add = True
                    if doc['taste'].get(i) is None:
                        add = False
                        break
                    if doc['taste'].get(i) < 0.8:
                        add = False
                        break
                else:
                    add = False
            if add:
                output_coll.append(doc["name"])

    # similar to the code above
    if add_result is not None:
        for doc in add_result:
            add = True
            for i in taste:
                if doc['taste'] is not None:
                    add = True
                    if doc['taste'].get(i) is None:
                        add = False
                        break
                    if doc['taste'].get(i) < 0.8:
                        add = False
                        break
                else:
                    add = False
            # do not add in duplicate
            if add and doc['name'] not in output_coll:
                output_coll.append(doc["name"])
    return output_coll


@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('session_id', '', expires=0)
    return resp


def cal_nearest_10_page(page_number, max_pages):
    """ it calculates the nearest 10 page """
    page_list = []
    pivot = page_number
    if pivot - 5 < 0:
        for i in range(1, pivot + 1):
            page_list.append(i)
        if pivot + 5 + abs(pivot - 5) > max_pages or pivot + 5 > max_pages:
            for i in range(pivot, max_pages + 1):
                page_list.append(i)
        else:
            for i in range(pivot, pivot + 5 + abs(pivot - 5) + 1):
                page_list.append(i)
    else:
        if pivot + 5 > max_pages:
            if pivot - 5 - abs(max_pages - pivot - 5) < 0:
                for i in range(1, pivot + 1):
                    page_list.append(i)
            else:
                for i in range(pivot - 5 - abs(max_pages - pivot - 5) + 1, pivot + 1):
                    page_list.append(i)
            for i in range(pivot, max_pages + 1):
                page_list.append(i)
        else:
            for i in range(pivot - 5 + 1, pivot + 5 + 1):
                page_list.append(i)
    return sorted(list(set(page_list)))


if __name__ == '__main__':
    # app.run(debug=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)
    # server.serve_forever()
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, jsonify, url_for, render_template, request
import config
import json, time, datetime
# import pysolr
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(config)  # 导入config

MC = MongoClient("127.0.0.1", 27017)
DB = MC.fit3164

usr_coll = DB.user_data
app = Flask(__name__)
app.config.from_object(config)


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

        return "success"
    return render_template('homepage.html')


def process_json(data):
    return data


def render_result(input_dict):
    """
    :param input_dict: a dictionary with user input data for searching
    :return: a render_template function with a new web pages
    """
    dish_coll = DB.dish_analysis
    print(input_dict)
    pass


if __name__ == '__main__':
    app.run(debug=True)

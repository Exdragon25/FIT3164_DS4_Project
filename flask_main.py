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

dish_coll = DB.dish_analysis
usr_coll = DB.user_data


@app.route("/about/result")
def about_result():
    context = {"username": "DS_4"}

    return render_template("search_result.html", **context)


# get user input
@app.route("/", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        output = {"search": request.args.get("Search"),
                  "cuisine": request.args.getlist("Cuisine"),
                  "taste": request.args.getlist("Taste"),
                  "course": request.args.getlist("Course")
                  }
        print(output)  # should jump to next search result pages.
        # return render_result(output)
    return render_template('homepage.html')


def render_result(input_dict):
    """
    :param input_dict: a dictionary with user input data for searching
    :return: a render_template function with a new web pages
    """


if __name__ == '__main__':
    app.run(debug=True)

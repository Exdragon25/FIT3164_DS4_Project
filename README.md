# FIT3164_DS4_Project

This is FIT3164 DS4 team Project

>Dish recommendation system

Provide the different dishes based on user's input, 
and with an ML provide the daily recommendation based on user's searching history.

For now, we have:

[Done]Dataset and Database

[Doing]Search Functions

[Not Start yet]Filter Functions

[Prototype] ML recommendation system

[Doing] Webpages and Flask

This project is mainly on python with Flask framework.
And make by 5 people:

+ Tzu-Han Cheng [ML]
+ Zhuoting Chen [Webpage/css]
+ Lijia Qi [Webpage/Flask]
+ Xiaolong Shen [Database/Search Function]
+ Xin Zhou [ML/Webpage]

# import datasets
mongoimport  -d fit3164 -c Dish_collection --type=json --jsonArray dish_collection.json

pip3 install pymongo
pip3 install numpy
pip3 install nltk
pip3 install scipy
pip3 install pandas
pip3 install flask
pip3 install unidecode
pip3 install spacy
pip3 install gevent 

http://docs.jinkan.org/docs/flask/quickstart.html#web
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

# Kill process
lsof -i:8000
kill -9 PID

# run by:
set FLASK_APP=app.py | flask run --host=0.0.0.0 --port=8000

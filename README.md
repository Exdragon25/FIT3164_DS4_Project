# FIT3164_DS4_Project

This is FIT3164 DS4 team Project

>Dish recommendation system

Provide the different dishes based on user's input, 
and with an ML provide the daily recommendation based on user's searching history.

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

# run by:
set FLASK_APP=app.py | flask run --host=0.0.0.0 --port=8000

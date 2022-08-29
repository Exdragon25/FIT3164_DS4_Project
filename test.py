import nltk
import string
import ast
import re
import unidecode
from nltk import WordNetLemmatizer
from pymongo import MongoClient

def render_result(ingredient, cuisine, taste, course):
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

    print(ingredient_parser(["bananas", "water"]))
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

    # if input has no comma
    if not ingredient_search:
        # no cuisine and course selected
        if len(cuisine) == 0 and len(course) == 0:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "$i"}})
        # only course selected
        elif len(cuisine) == 0 and len(course) != 0:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "$i"},
                                     "course": {'$in': course}})
        # only cuisine selected
        elif len(cuisine) != 0 and len(course) == 0:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "$i"},
                                     "cuisine": {"$in": cuisine}})
        # cuisine and course are selected
        else:
            result = dish_coll.find({'name': {"$regex": ingredient, "$options": "$i"}, "cuisine": {"$in": cuisine},
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
            # if input is a single word, we make it into a list so we can do $in query
            ingredient = [ingredient]
            # similar code to above
        if len(cuisine) == 0 and len(course) == 0:
            add_result = dish_coll.find({'NER': {"in": ingredient}})
        elif len(cuisine) == 0 and len(course) != 0:
            add_result = dish_coll.find({'NER': {"in": ingredient},
                                         "course": {'in': course}})
        elif len(cuisine) != 0 and len(course) == 0:
            add_result = dish_coll.find({'NER': {"in": ingredient},
                                         "cuisine": {"in": cuisine}})
        else:
            add_result = dish_coll.find({'NER': {"in": ingredient}, "cuisine": {"in": cuisine},
                                         "course": {'in': course}})

    output_coll = []
    # we lastly filter the result with taste chosen
    if result is not None:
        for doc in result:
            add = True
            # do not add into list if taste is not what isn't wants or taste data == None
            for i in taste:
                if doc['taste'] is not None:
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
    return len(output_coll)

print(render_result("", ["American"], [], ["Salads"]))

client = MongoClient()
db = client.fit3164
dish_coll = db.Dish_collection

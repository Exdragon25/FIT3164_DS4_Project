import csv

import pandas as pd
import json
import numpy as np

import nltk
import string
import ast
import re
import unidecode
import spacy


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
    words_to_remove = [
        "very",
        "fresh",
        "chilly",
        "minced",
        "chopped",
        "oil",
        "a",
        "red",
        "bunch",
        "and",
        "clove",
        "or",
        "leaf",
        "chilli",
        "large",
        "extra",
        "sprig",
        "ground",
        "handful",
        "free",
        "small",
        "pepper",
        "virgin",
        "range",
        "from",
        "dried",
        "sustainable",
        "black",
        "peeled",
        "higher",
        "welfare",
        "seed",
        "for",
        "finely",
        "freshly",
        "sea",
        "quality",
        "white",
        "ripe",
        "few",
        "piece",
        "source",
        "to",
        "organic",
        "flat",
        "smoked",
        "sliced",
        "green",
        "picked",
        "the",
        "stick",
        "plain",
        "plus",
        "mixed",
        "bay",
        "basil",
        "your",
        "cumin",
        "optional",
        "serve",
        "unsalted",
        "baby",
        "paprika",
        "fat",
        "ask",
        "natural",
        "skin",
        "roughly",
        "into",
        "such",
        "cut",
        "good",
        "brown",
        "grated",
        "trimmed",
        "oregano",
        "powder",
        "yellow",
        "dusting",
        "knob",
        "frozen",
        "on",
        "deseeded",
        "low",
        "runny",
        "balsamic",
        "cooked",
        "streaky",
        "nutmeg",
        "sage",
        "rasher",
        "zest",
        "pin",
        "groundnut",
        "breadcrumb",
        "turmeric",
        "halved",
        "grating",
        "stalk",
        "light",
        "tinned",
        "dry",
        "soft",
        "rocket",
        "bone",
        "colour",
        "washed",
        "skinless",
        "leftover",
        "splash",
        "removed",
        "dijon",
        "thick",
        "big",
        "hot",
        "drained",
        "sized",
        "chestnut",
        "watercress",
        "fishmonger",
        "english",
        "dill",
        "caper",
        "raw",
        "worcestershire",
        "flake",
        "cider",
        "cayenne",
        "tbsp",
        "leg",
        "pine",
        "wild",
        "if",
        "fine",
        "herb",
        "almond",
        "shoulder",
        "cube",
        "dressing",
        "with",
        "chunk",
        "spice",
        "thumb",
        "garam",
        "new",
        "little",
        "punnet",
        "peppercorn",
        "shelled",
        "saffron",
        "other",
        "chopped",
        "salt",
        "olive",
        "taste",
        "can",
        "sauce",
        "water",
        "diced",
        "package",
        "italian",
        "shredded",
        "divided",
        "parsley",
        "all",
        "purpose",
        "crushed",
        "juice",
        "more",
        "coriander",
        "bell",
        "needed",
        "thinly",
        "boneless",
        "half",
        "thyme",
        "cubed",
        "cinnamon",
        "cilantro",
        "jar",
        "seasoning",
        "rosemary",
        "extract",
        "sweet",
        "baking",
        "beaten",
        "heavy",
        "seeded",
        "tin",
        "uncooked",
        "crumb",
        "style",
        "thin",
        "coarsely",
        "spring",
        "cornstarch",
        "strip",
        "cardamom",
        "rinsed",
        "root",
        "quartered",
        "head",
        "softened",
        "container",
        "crumbled",
        "frying",
        "lean",
        "cooking",
        "roasted",
        "warm",
        "whipping",
        "thawed",
        "pitted",
        "sun",
        "kosher",
        "bite",
        "toasted",
        "split",
        "melted",
        "degree",
        "lengthwise",
        "romano",
        "packed",
        "pod",
        "anchovy",
        "rom",
        "prepared",
        "juiced",
        "fluid",
        "floret",
        "room",
        "active",
        "seasoned",
        "mix",
        "deveined",
        "lightly",
        "anise",
        "thai",
        "size",
        "unsweetened",
        "torn",
        "wedge",
        "sour",
        "basmati",
        "marinara",
        "dark",
        "temperature",
        "garnish",
        "bouillon",
        "loaf",
        "shell",
        "reggiano",
        "canola",
        "parmigiano",
        "round",
        "canned",
        "ghee",
        "crust",
        "long",
        "broken",
        "ketchup",
        "bulk",
        "cleaned",
        "condensed",
        "sherry",
        "provolone",
        "cold",
        "cottage",
        "spray",
        "tamarind",
        "pecorino",
        "shortening",
        "part",
        "bottle",
        "sodium",
        "grain",
        "french",
        "roast",
        "stem",
        "link",
        "firm",
        "mild",
        "dash",
        "boiling",
        "oil",
        "chopped",
        "vegetable oil",
        "chopped oil",
        "garlic",
        "skin off",
        "bone out",
        "sugar",
        "powdered",
        "onion"
    ]

    if isinstance(ingreds, list):
        ingredients = ingreds
    else:
        ingredients = ast.literal_eval(ingreds)
    # We first get rid of all the punctuation. We make use of str.maketrans. It takes three input
    # arguments 'x', 'y', 'z'. 'x' and 'y' must be equal-length strings and characters in 'x'
    # are replaced by characters in 'y'. 'z' is a string (string.punctuation here) where each character
    #  in the string is mapped to None.

    translator = str.maketrans("", "", string.punctuation)
    lemmatizer = WordNetLemmatizer()
    ingred_list = []
    for i in ingredients:
        i.translate(translator)
        # We split up with hyphens as well as spaces
        items = re.split(" |-", i)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
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
        # Get rid of common easy words
        items = [word for word in items if word not in words_to_remove]

        if items:
            word = " ".join(items)
            if word not in ingred_list:
                ingred_list.append(word)

                """only do this in the fist time"""
                # if len(items) == 1 and word not in not_noun:
                #     doc = nlp(word)
                #     for token in doc:
                #         if token.pos_ == "NOUN" or token.pos_ == "PROPN":
                #             ingred_list.append(" ".join(items))
                #             print(not_noun)
                #         else:
                #             not_noun.add(str(word))
                #
                # else:
                #     ingred_list.append(word)
    return ingred_list


# test = ['cheddar cheese', 'mayonnaise', 'salt', 'ground red pepper', 'pecans', 'whole-berry', 'fresh cranberries', 'crackers', 'cranberry-cheese box']
# print(ingredient_parser(test))

not_noun = set()

# nltk.download()
from nltk.stem import WordNetLemmatizer

nlp = spacy.load("en_core_web_lg")
with open("dish_collection.json") as f:
    data = json.loads(f.read())
df = pd.DataFrame(data)
df = df[["name", "NER"]]
df = df[df['NER'].map(lambda d: len(d)) > 0]

for i in df.index:
    df["NER"][i] = ingredient_parser(df["NER"][i])
df = df[df['NER'].map(lambda d: len(d)) > 0]

"""only do this in the fist time"""
# with open('not_nouns.csv', 'w') as f:
#     writer = csv.writer(f)
#     for word in not_noun:
#         writer.writerow([word])

with open('not_nouns_cleaned.csv') as f:
    reader = csv.reader(f)
    words_to_remove = list(reader)
words_to_remove = words_to_remove[0]
print(words_to_remove)

for i in df.index:
    for ingred in df["NER"][i]:
        if ingred in words_to_remove:
            df["NER"][i].remove(ingred)

df = df[df['NER'].map(lambda d: len(d)) > 0]

import findspark

findspark.init()
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("test pyspark").getOrCreate()
sc = spark.sparkContext

df = spark.createDataFrame(df)
df.show(3)

from pyspark.ml.feature import Word2Vec

word2Vec = Word2Vec(
    vectorSize=100,
    minCount=0,
    inputCol="NER",
    outputCol="word2vec")

model = word2Vec.fit(df)
df_word2vec = model.transform(df)
df_word2vec.show(3)

df_word2vec.toPandas().to_csv('dish_word2vec.csv', index=False)

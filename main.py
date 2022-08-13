import csv
import pandas as pd
import json
import nltk
import string
import ast
import re
import unidecode
import spacy
# nltk.download()
from nltk.stem import WordNetLemmatizer


# clean the NER field and find words that are possibly not nouns
def data_cleaning_step1():
    global df

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
            # Get rid of common easy words
            items = [word for word in items if word not in words_to_remove]

            if items:
                if len(items) == 1:
                    single_word.add(items[0])
                word = " ".join(items)
                if word not in ingred_list:
                    ingred_list.append(word)
        return ingred_list

    # use spacy to find words that are possibly not a noun
    def find_not_nouns():
        not_nouns = set()
        for i in single_word:
            doc = nlp(i)
            for token in doc:
                if not (token.pos_ == "NOUN" or token.pos_ == "PROPN"):
                    not_nouns.add(i)
        return not_nouns

    nlp = spacy.load("en_core_web_lg")
    single_word = set()
    df = df[["name", "NER"]]
    # remove recipes contain empty NER
    df = df[df['NER'].map(lambda d: len(d)) > 0]
    # cleanup the NER
    df["NER"] = df["NER"].map(lambda x: ingredient_parser(x))
    df = df[df['NER'].map(lambda d: len(d)) > 0]
    not_nouns = find_not_nouns()

    # write the not_nouns found by machine learning model spacy into csv file
    # ,and we will verify the result by human and remove some words that are actually nouns
    with open('not_nouns.csv', 'w') as f:
        f.truncate()
        writer = csv.writer(f)
        for word in not_nouns:
            writer.writerow([word])


# not_nouns csv is cleaned and checked by human, and exported as not_nouns_cleaned.csv
# second step of data cleaning is to filter out the words in NER which are not nouns using the
# not_nouns_cleaned.csv
def data_cleaning_step2():
    global df
    with open('not_nouns_cleaned.csv') as f:
        reader = csv.reader(f)
        words_to_remove = list(reader)
    words_to_remove = words_to_remove[0]


    for i in df.index:
        for ingred in df["NER"][i]:
            if ingred in words_to_remove:
                df["NER"][i].remove(ingred)
    df = df[df['NER'].map(lambda d: len(d)) > 0]


def train_model():
    global df
    import findspark
    findspark.init()
    from pyspark.sql import SparkSession

    spark = SparkSession.builder.appName("recipe recommendation").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
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


if __name__ == '__main__':
    with open("dish_collection.json") as f:
        data = json.loads(f.read())
        df = pd.DataFrame(data)
    data_cleaning_step1()
    data_cleaning_step2()
    train_model()

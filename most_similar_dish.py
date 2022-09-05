import pandas as pd
import numpy as np
import json

df = pd.read_csv("dish_word2vec.csv")
userHistory = {
    "user_id": 1,
    "recipe_viewed": ["BLT Chicken Salad", "Shrimp Curry", "Vegetarian Moussaka", "Chicken Quinoa Salad",
                      "Spring Chicken Soup", "Chicken Enchiladas Suizas", "Baked Chicken Nachos", "Potato Gratin",
                      "Family Favorite Chicken Lo Mein", "Creamy Chicken Piccata"]
}
# change str to np array
df["word2vec"] = df["word2vec"].map(lambda x: np.array(json.loads(x)))


# convert recipe_name to vector
def convert_vector(target_name):
    target_embedding = df.loc[df["name"] == target_name, "word2vec"].iloc[0]
    return target_embedding


# find average vector of list of user searching history
def aggregate_vectors(history):
    history_vec = []
    for i in history:
        history_vec.append(convert_vector(i))

    return np.mean(history_vec, axis=0, dtype=np.ndarray)


# find similar recipes by a vector
def find_similar_recipes(target_embedding, n=30):
    global df
    from scipy.spatial import distance
    df["sim_value"] = df["word2vec"].map(lambda x: 1 - distance.cosine(target_embedding, x))
    df = df.sort_values(by="sim_value", ascending=False)
    return df['name'].head(n).tolist()


import pandas as pd
df = pd.read_csv("dish_word2vec.csv")

import numpy as np
import json


df["word2vec"] = df["word2vec"].map(lambda x : np.array(json.loads(x)))
target_name = "Chocolate Cake"
target_embedding = df.loc[df["name"]==target_name, "word2vec"].iloc[0]

from scipy.spatial import distance
df["sim_value"] = df["word2vec"].map(lambda x : 1 - distance.cosine(target_embedding, x))
df = df.sort_values(by="sim_value", ascending=False)
print(df[["name", "NER"]].head(10))

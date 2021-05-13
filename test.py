
import fasttext
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import combinations
from scipy.spatial.distance import cosine

from preprocess import *


def similarity(a, b, model):
        a_emb = model.get_sentence_vector(a)
        b_emb = model.get_sentence_vector(b)
        cosine_distance = 1 - cosine(a_emb, b_emb)
        return cosine_distance


def average_similarity(text_list, model):
        text_pairs = combinations(text_list, 2)
        sims = [similarity(x, y, model) for x, y in tqdm(text_pairs)]
        average = np.sum(sims) / len(sims)
        return sims, average


def flatten_list(t):
    return [item for sublist in t for item in sublist]


# Bring data
df = pd.read_csv('data/collegeboard_majors_all.csv')
df = df.dropna(subset=['introduction'])
df['introduction'] = df['introduction'].apply(lambda x: preprocess(x))


# FastText
pretrained_path = 'model/wiki.en.bin'
model = fasttext.load_model(pretrained_path)


# Compare cosine similarities of categories
category_level = 'category1'
category_df = df.groupby(category_level)['introduction'].apply(lambda x: list(x)).reset_index()

avg_list = []
for i, row in category_df.iterrows():
        text_list = category_df.loc[i]['introduction']
        _, avg = average_similarity(text_list, model)
        avg_list.append(avg)
print(np.mean(avg_list))
category_df['fasttext_similarity'] = avg_list


# Get cosine similarities of all categories
text_list = flatten_list( list(category_df['introduction']) )
_, avg_all = average_similarity(text_list, model)


print('Within categories:')
print(np.mean(avg_list))
print('\nAverage:')
print(avg_all)

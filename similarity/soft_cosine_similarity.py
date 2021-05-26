
import numpy as np
import pandas as pd
from tqdm import tqdm
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity

from embeddings import Word2VecEmbedding, fastTextEmbedding
from preprocess import *


def combinations_similarity(vectors_list):
        vectors_pairs = combinations(vectors_list, 2)
        sims = [cosine_similarity(x, y) for x, y in tqdm(vectors_pairs)]
        average = np.sum(sims) / len(sims)
        return sims, average


def flatten_list(t):
    return [item for sublist in t for item in sublist]


# Bring data: CollegeBoard
df = pd.read_csv('data/collegeboard_majors_all.csv')
df = df.dropna(subset=['introduction'])
df['introduction'] = df['introduction'].apply(lambda x: preprocess(x))

category_level = 'category1'
category_df = df.groupby(category_level)['introduction'].apply(lambda x: list(x)).reset_index()

# Bring data: NCES
all_df = pd.read_csv('data/nces_majors_all.csv')
key_df = pd.read_csv('data/nces_majors_key.csv')
df = key_df.merge(all_df[['category', 'definition']], left_on='category3', right_on='category')
df['definition'] = df['definition'].apply(lambda x: preprocess(x))
df = df.drop(columns='category')
df = df[(df['category1'] != '21) RESERVED.') & (df['category1'] != '55) RESERVED.')]

category_level = 'category1'
category_df = df.groupby(category_level)['definition'].apply(lambda x: list(x)).reset_index()

# Call embedding
word2vec_path = '../../Desktop/model/GoogleGoogleNews-vectors-negative300.bin'
fasttext_path = '../../Desktop/model/wiki.en.bin'

embedding = fastTextEmbedding(fasttext_path)

avg_list = []
for i, row in category_df.iterrows():
        text_list = category_df.loc[i]['introduction']
        _, avg = combinations_similarity(text_list)
        avg_list.append(avg)

category_df['fasttext_similarity'] = avg_list


# Get cosine similarities of all categories
text_list = flatten_list( list(category_df['introduction']) )
_, avg_all = combinations_similarity(text_list, model)


print('Within categories:')
avg_list = [avg for avg in avg_list if not np.isnan(avg)]
print(np.mean(avg_list))
print('\nAverage:')
print(avg_all)





# Compare cosine similarities of categories
category_level = 'category1'
category_df = df.groupby(category_level)['definition'].apply(lambda x: list(x)).reset_index()

avg_list = []
for i, row in category_df.iterrows():
        text_list = category_df.loc[i]['definition']
        _, avg = combinations_similarity(text_list, model)
        avg_list.append(avg)

category_df['fasttext_similarity'] = avg_list


# Get cosine similarities of all categories
text_list = flatten_list( list(category_df['definition']) )
_, avg_all = combinations_similarity(text_list, model)


print('Within categories:')
avg_list = [avg for avg in avg_list if not np.isnan(avg)]
print(np.mean(avg_list))
print('\nAverage:')
print(avg_all)

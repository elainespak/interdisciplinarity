
import pandas as pd

from similarity.embedding import Word2VecEmbedding, fastTextEmbedding
from similarity.soft_cosine_similarity import *
from preprocess import *


### Define parameters
data = 'NCES' # 'CollegeBoard'
category_level = 'category1'
section = 'definition' # 'introduction'
embedding_type = 'fastText' # 'word2vec'


### Load data
if data == 'NCES':
    all_df = pd.read_csv('data/nces_majors_all.csv')
    key_df = pd.read_csv('data/nces_majors_key.csv')
    df = key_df.merge(all_df[['category', section]], left_on='category3', right_on='category')
    df[section] = df[section].apply(lambda x: preprocess(x))
    df = df.drop(columns='category')
    df = df[(df['category1'] != '21) RESERVED.') & (df['category1'] != '55) RESERVED.')]

    category_df = df.groupby(category_level)[section].apply(lambda x: list(x)).reset_index()

elif data == 'CollegeBoard':
    df = pd.read_csv('data/collegeboard_majors_all.csv')
    df = df.dropna(subset=[section])
    df[section] = df[section].apply(lambda x: preprocess(x))

    category_df = df.groupby(category_level)[section].apply(lambda x: list(x)).reset_index()


### Call embedding
from similarity.embedding import Word2VecEmbedding, fastTextEmbedding

if embedding_type == 'fastText':
    model_path = '../../Desktop/model/wiki.en.bin'
    embedding = fastTextEmbedding(model_path)

elif embedding_type == 'word2vec':
    model_path = '../../Desktop/model/GoogleGoogleNews-vectors-negative300.bin'
    embedding = Word2VecEmbedding(model_path)

model = embedding.load_model()

avg_list = []
for i, row in category_df.iterrows():
        text_list = category_df.loc[i][section]
        vecs_list = [model.get_sentence_vector(text) for text in text_list]
        _, avg = combinations_similarity(vecs_list)
        avg_list.append(avg)

category_df['fasttext_similarity'] = avg_list


# Get cosine similarities of all categories
text_list = flatten_list( list(category_df[section]) )
vecs_list = [model.get_sentence_vector(text) for text in text_list]
_, avg_all = combinations_similarity(vecs_list)


print('Within categories:')
avg_list = [avg for avg in avg_list if not np.isnan(avg)]
print(np.mean(avg_list))
print('\nAverage:')
print(avg_all)

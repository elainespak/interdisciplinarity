
import pandas as pd

from preprocess import *
from similarity.soft_cosine_similarity import *
from similarity.encoder import Word2VecEncoder, fastTextEncoder, SentenceBERTEncoder


### Define parameters
data = 'NCES' # 'CollegeBoard'
category_level = 'category1'
section = 'definition' # 'introduction'
encoder_type = 'sentencebert' #'word2vec' # 'fastText'


### Load data
if data == 'NCES':
    all_df = pd.read_csv('data/nces_majors_all_stem.csv')
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
if encoder_type == 'fasttext':
    model_path = '../../Desktop/model/wiki.en.bin'
    encoder = fastTextEncoder(model_path)

elif encoder_type == 'word2vec':
    model_path = '../../Desktop/model/GoogleNews-vectors-negative300.bin'
    encoder = Word2VecEncoder(model_path)

elif encoder_type == 'sentencebert':
    model_path = 'bert-base-nli-mean-tokens'#'../../Desktop/model/bert-base-nli-mean-tokens'
    encoder = SentenceBERTEncoder(model_path)

# Get soft cosine similarities among all categories
text_list = flatten_list( list(category_df[section]) )
vecs_list = []
for text in tqdm(text_list):
    vecs_list.append( encoder.get_sentence_vector(text) )
_, avg_all = combinations_similarity(vecs_list)

# Get within-category soft cosine similarities
avg_list = []
for i, row in category_df.iterrows():
        text_list = category_df.loc[i][section]
        vecs_list = [encoder.get_sentence_vector(text) for text in text_list]
        _, avg = combinations_similarity(vecs_list)
        avg_list.append(avg)
category_df['similarity'] = avg_list

print(f'{data} - {category_level} - {encoder_type}\n')
print('Within categories:')
avg_list = [avg for avg in avg_list if not np.isnan(avg)]
print(np.mean(avg_list))
print('\nAverage:')
print(avg_all)


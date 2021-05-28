import re

import nltk
from nltk.stem import WordNetLemmatizer
stemmer = WordNetLemmatizer()
en_stop = set(nltk.corpus.stopwords.words('english'))

HTML_PATTERN = ['\n', '\xa0']


def clean_html(s):
    for p in HTML_PATTERN:
        s = s.replace(p, ' ')
    return s


def preprocess(document):
        # Remove all html tags
        document = clean_html(str(document))

        # Remove all the special characters
        document = re.sub(r'\W', ' ', document)

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Converting to Lowercase
        document = document.lower()

        # Lemmatization
        tokens = document.split()
        tokens = [stemmer.lemmatize(word) for word in tokens]
        tokens = [word for word in tokens if word not in en_stop]
        tokens = [word for word in tokens if len(word) > 3]

        preprocessed_text = ' '.join(tokens)

        return preprocessed_text

### TODO: Delete later
### Add STEM category to NCES Majors
import re
import pandas as pd


def replace(x):
    try:
        if not pd.isnull(x):
            x = re.sub('\s+', ' ', x)
    except:
        print(f'{x} caused problems')
    return x

all_df = pd.read_csv('data/nces_majors_all.csv')
all_df['category'] = all_df['category'].apply(lambda x: replace(x))
all_df.to_csv('data/nces_majors_all.csv')


stem = pd.read_csv('data/nces_majors_stem.csv')

def reformat(c):
    c = c[3:]
    if 'Moved from' in c:
        c = re.match('.*?(?= Moved from )', c).group(0)
    if '. New' in c:
        c = re.match('.*?(?=. New)', c).group(0) + '.'
    if not c.endswith('.'):
        c += '.'
    new_c = c[:7] + ')' + c[7:]
    return new_c

stem['category'] = stem['category'].apply(lambda x: reformat(x))
stem['stem'] = 'y'

all_stem_df = all_df.merge(stem, on='category', how='left')
test = all_df.merge(stem, on='category', how='right')
test = test[pd.isnull(test['definition'])]

# Check
len(stem) == len(all_stem_df[all_stem_df['stem']=='y']) + len(test)

all_stem_df['stem'] = all_stem_df['stem'].apply(lambda x: 'n' if pd.isnull(x) else 'y')
all_stem_df.to_csv('data/nces_majors_all_stem.csv')

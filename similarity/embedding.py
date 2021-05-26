
import fasttext
import numpy as np
from gensim.models import KeyedVectors


class Word2VecEmbedding():

    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        model = KeyedVectors.load_word2vec_format(model_path)
        print(f" Pretrained Word2Vec model loaded")
        return model

    def get_word_vector(self, word):
        if word in self.model:
            return self.model[word]
        else:
            np.zeros(self.model.vector_size)

    def get_sentence_vector(self, preprocessed_sentence):
        words = preprocessed_sentence.split()
        word_vectors = [self.get_word_vector(w) for w in words]
        sentence_vector = np.mean(word_vectors, axis=0)
        return sentence_vector


class fastTextEmbedding():

    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        model = fasttext.load_model(model_path)
        print(f" Pretrained fastText model loaded")
        return model

    def get_sentence_vector(self, preprocessed_sentence):
        return self.model.get_sentence_vector(preprocessed_sentence)

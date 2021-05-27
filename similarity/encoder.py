
import fasttext
import numpy as np
from gensim.models import KeyedVectors
from sentence_transformers import SentenceTransformer


class fastTextEncoder():

    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        print(" Pretrained fastText model loading ... ")
        model = fasttext.load_model(model_path)
        return model

    def get_sentence_vector(self, preprocessed_sentence):
        sentence_vector = self.model.get_sentence_vector(preprocessed_sentence)
        return sentence_vector


class Word2VecEncoder():

    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        print(" Pretrained Word2Vec model loading ... ")
        model = KeyedVectors.load_word2vec_format(model_path, binary=True)
        return model

    def get_word_vector(self, word):
        if word in self.model:
            return self.model[word]
        else:
            return np.zeros(self.model.vector_size)

    def get_sentence_vector(self, preprocessed_sentence):
        words = preprocessed_sentence.split()
        word_vectors = [self.get_word_vector(w) for w in words]
        sentence_vector = np.mean(word_vectors, axis=0)
        return sentence_vector


class SentenceBERTEncoder():

    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        print(" Pretrained SentenceBERT model loading ... ")
        model = SentenceTransformer(model_path)
        return model

    def get_sentence_vector(self, preprocessed_sentence):
        sentence_vector = self.model.encode(list(preprocessed_sentence))[0]
        return sentence_vector

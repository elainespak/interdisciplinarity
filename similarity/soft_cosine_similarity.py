
import numpy as np
from tqdm import tqdm
from itertools import combinations
from scipy.spatial.distance import cosine


def cosine_similarity(embedding_a, embedding_b):
        return 1 - cosine(embedding_a, embedding_b)


def combinations_similarity(vectors_list):
        vectors_pairs = combinations(vectors_list, 2)
        sims = [cosine_similarity(x, y) for x, y in tqdm(vectors_pairs)]
        average = np.sum(sims) / len(sims)
        return sims, average


def flatten_list(t):
    return [item for sublist in t for item in sublist]

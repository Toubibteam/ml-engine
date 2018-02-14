import unicodedata
import pandas as pd
import pymongo
from nltk.stem import PorterStemmer as Stemmer

from config import UNK, PUNC

class CodeDataset:
    """Loads codes and their description with some preprocessing"""

    def __init__(self, db, vocab=None):
        self._vocab = vocab
        self._data = db
        self._stemmer = Stemmer()


    def __iter__(self):
        for element in self._data.find() :
            descriptions = [self.preprocess(d) for d in element['Descriptions']]
            if descriptions is not None:
                yield element['Code'], descriptions


    def get_description(self, code_id):
        return self._data.find_one({'code' : code_id})


    def preprocess(self, description):
        """Preprocess description into a list of words or ids"""
        result = simple_tok(description)
        if result is None:
            return None

        if self._vocab is not None:
            result = [self._vocab.tok_to_id(tok) for tok in result]
        return result


def simple_tok(sentence):
    """
    Args:
        sentence: (string) with accents etc.

    Returns:
        words_raw: (list of words) with no accents and no punctuation

    """
    if sentence is None:
        return None

    s = "".join(c.replace('"','') for c in sentence if c not in PUNC) # remove punc
    words_raw = s.strip().split(" ")  # split by space
    words_raw = map(clean, words_raw) # remove accents
    return words_raw


def clean(word):
    """Removes accents"""
    if type(word) is not unicode: word = unicode(word, 'utf-8')
    word = unicodedata.normalize('NFKD', word)
    word = word.encode('ASCII', 'ignore')
    return word

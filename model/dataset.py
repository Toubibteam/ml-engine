import unicodedata
import pandas as pd
from nltk.stem import PorterStemmer as Stemmer

from config import UNK, PUNC
from vocab import build_vocab


class CodeDataset:
    """Loads codes and their description with some preprocessing"""

    def __init__(self, path, vocab=None):
        self._path = path
        self._vocab = vocab
        self._data = load_csv_file(self._path)
        # self._stemmer = Stemmer()


    def __iter__(self):
        for code_id, description  in self._data.items():
            des = self.preprocess(description['description'])
            yield code_id, des, description['type'] 

    def get_description(self, code_id):
        return self._data[code_id]


    def preprocess(self, description):
        """Preprocess description into a list of words or ids"""
        result = simple_tok(description)
        result = [tok for tok in result]
        if self._vocab is not None:
            result = [self._vocab.tok_to_id(tok) for tok in result]
        return result



def load_csv_file(path):
    """
    Args:
        path: (string) path to csv file with code and description

    Returns:
        d: (dict) d[code_id] = description

    """
    df = pd.read_csv(path, sep=";",names=['Code','Type','Description']) if path is not None else None
    data = {}
    if df is not None:
        for _, row in df.iterrows():
            print row
            code_id = row["Code"]
            description = row["Description"]
            data[code_id] = {'description' : description, 'type':row['Type']}
    return data


def simple_tok(sentence):
    """
    Args:
        sentence: (string) with accents etc.

    Returns:
        words_raw: (list of words) with no accents and no punctuation

    """
    s = "".join(c for c in sentence if c not in PUNC) # remove punc
    words_raw = s.strip().split(" ")  # split by space
    words_raw = map(clean, words_raw) # remove accents
    return words_raw


def clean(word):
    """Removes accents"""
    if type(word) is not unicode: word = unicode(word, 'utf-8')
    word = unicodedata.normalize('NFKD', word)
    word = word.encode('ASCII', 'ignore')
    return word
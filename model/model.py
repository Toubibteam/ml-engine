from os import path
import tensorflow as tf
import numpy as np
import json

from dataset import CodeDataset, simple_tok, clean
from vocab import Vocab

class Model:
    """Class to compute representation of query and descriptions"""

    def __init__(self, type_code):
        # self._vocab = Vocab("./data/vocab.txt")
        folder = path.abspath(path.split(__file__)[0])
        with open(folder + '/data/vocab.txt','r') as df :
            self._vocab = df.read().split('\n')
        with open(folder + '/data/ccam.json','r') as df :
            self._ccam = json.load(df)
        with open(folder + '/data/cim.json','r') as df :
            self._cim = json.load(df)

        self._all_vocab = Vocab(folder + "/data/vocab_all.txt")
        self._code_dataset = CodeDataset(folder + "/data/all_code.csv", self._all_vocab)
        self._descriptions = self._build_descriptions(type_code)
        print "model loaded"


    def _build_descriptions(self, type_code):
        """Load representation once and for all"""
        _descriptions = {}
        for code_id, description, code in self._code_dataset:
            if code == type_code :
                rep = self.description_representation(description)
                _descriptions[code_id] = rep
        return _descriptions


    @classmethod
    def similarity(self, query, description):
        q = set(query)
        d = set(description)
        return len(q.intersection(d))


    @classmethod
    def description_representation(self, description):
        return description


    def query_representation(self, query):
        return self._code_dataset.preprocess(query)


    def change_query(self, query, type_code) :
        if type_code == 'CCAM' :
            syn = self._ccam
        else :
            syn = self._cim
        query = simple_tok(query)
        new_query = ''
        for word in query :
            if word in self._vocab :
                new_query += word + ' '
            else :
                if word in syn.keys() :
                    new_query += syn[word][0] + ' '
                else :
                    new_query += ''
        return new_query


    def predict(self, query, type_code):
        query = self.change_query(query,type_code)
        query = self.query_representation(query)
        results = {}
        for code_id, description in self._descriptions.items():
            metric = self.similarity(query, description)
            if metric > 0:
                description = self._code_dataset.get_description(code_id)
                results[code_id] = {"metric": metric,
                                    "description": description}
        return results

if __name__ == "__main__":
    import json

    model = Model("CCAM")
    results = model.predict("muscles",'CCAM')
    print results

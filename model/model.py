from os import path
import tensorflow as tf
import numpy as np
import json

from dataset import CodeDataset, simple_tok, clean
from vocab import Vocab

class Model:
    """Class to compute representation of query and descriptions"""

    def __init__(self):
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
        self._descriptions = self._build_descriptions()
        print "model loaded"


    def _build_descriptions(self):
        """Load representation once and for all"""
        _descriptions = {}
        for code_id, description, type_, tarif in self._code_dataset:
            rep = self.description_representation(description)
            _descriptions[code_id] = {'description' : rep, 'tarif' : tarif, 'type' : type_}
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
        if type_code == "CCAM" :
            syn = self._ccam
        if type_code == "CIM" :
            syn = self._cim
        query = simple_tok(query)
        new_query = ''
        for word in query :
            if word in self._vocab :
                new_query += word + ' '
            else :
                if word in syn.keys() :
                    temp = syn[word]
                    synonymes = [t['syn'] for t in temp]
                    weights = [t['weight'] for t in temp]
                    weights, synonymes = zip(*sorted(zip(weights, synonymes)))
                    new_query = synonymes[0] + ' '
                else :
                    new_query += ''
        return new_query


    def predict(self, query,type_code):
        query = self.change_query(query,type_code)
        query = self.query_representation(query)
        results = {}
        for code_id, descriptions in self._descriptions.items():
            if descriptions['type'] == type_code :
                metric = self.similarity(query, descriptions['description'])
                if metric > 0:
                    description = self._code_dataset.get_description(code_id)
                    results[code_id] = {"metric": metric,
                                        "description": descriptions['description'],
                                        "tarif": descriptions['tarif'],
                                        "type" : descriptions['type']}
        return results

if __name__ == "__main__":
    import json

    model = Model()
    results = model.predict("muscles","CCAM")
    print results

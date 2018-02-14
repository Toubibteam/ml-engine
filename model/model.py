from os import path
import tensorflow as tf
import numpy as np
import json
import pymongo

from dataset import CodeDataset, simple_tok, clean
from vocab import Vocab

class Model:
    """Class to compute representation of query and descriptions"""

    def __init__(self,db):
        folder = path.abspath(path.split(__file__)[0])
        with open(folder + '/data/vocab.txt','r') as df :
            self._vocab = df.read().split('\n')
        with open(folder + '/data/ccam.json','r') as df :
            self._ccam = json.load(df)
        with open(folder + '/data/cim.json','r') as df :
            self._cim = json.load(df)

        self._all_vocab = Vocab(folder + "/data/vocab_all.txt")
        self._code_dataset = CodeDataset(db, self._all_vocab)
        self._descriptions = self._build_descriptions()
        print "model loaded"


    def _build_descriptions(self):
        """Load representation once and for all"""
        _descriptions = {}
        for code, descriptions in self._code_dataset :
            _descriptions[code] = descriptions
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

    def change_query(self,query,type_code) :
        query = simple_tok(query)
        new_query = ''
        syn = self._ccam if type_code == 'CCAM' else self._cim
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

    def predict(self, query, type_code):
        query = self.change_query(query,type_code)
        query = self.query_representation(query)
        results = {}
        for code_id, descriptions in self._descriptions.items():
            if len(descriptions) > 2 :
                occurence = 0
                for description in descriptions :
                    metric = self.similarity(query, description)
                    if metric > 0:
                        occurence += 1
                if occurence > 1 :
                    code_des = self._code_dataset.get_description(code_id)
                    results[code_id] = {"metric": metric,
                                        "description": code_des["descriptions"][0],
                                        "type" : type_code}
            else :
                metric = self.similarity(query, descriptions[0])
                if metric > 0 :
                    code_des = self._code_dataset.get_description(code_id)
                    results[code_id] = {"metric": metric,
                                        "description": code_des["descriptions"][0],
                                        "type" : type_code}

        return results


if __name__ == "__main__":
    import json

    client = pymongo.MongoClient("mongodb://localhost/codes")
    db = client.codes
    ccam = db.ccam

    model_ccam = Model(ccam)
    results = model_ccam.predict("muscles","CCAM")
    print results

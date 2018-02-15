from os import path
import tensorflow as tf
import numpy as np
import json
import pymongo

from dataset import CodeDataset, simple_tok, clean
from vocab import Vocab

class Model:
    """Class to compute representation of query and descriptions"""

    """ Class attributes """
    # (int) number of instances created
    _instances = 0
    # (array) contains all the vocabulary to enrich queries
    _vocab = []
    # (object) handle the token / id convertion
    _all_vocab = None
    # (dict) contains all the ccam synonyms
    _ccam_syn = {}
    # (dict) contains all the cim synonyms
    _cim_syn = {}

    def __init__(self,db):
        self.__class__.load_vocabs()
        self.__class__.load_synonyms(db)

        self._code_dataset = CodeDataset(db, self.__class__._all_vocab)
        self._descriptions = self._build_descriptions()
        self.__class__._instances += 1
        print "model loaded"


    def _build_descriptions(self):
        """Load representation once and for all"""
        _descriptions = {}
        for code, descriptions in self._code_dataset :
            _descriptions[code] = descriptions
        return _descriptions


    @classmethod
    def load_vocabs(cls):
        """ Load vocabularies from files

        Args:
            cls: (object) the class itself

        Returns:
            none

        """
        if cls._instances == 0:
            folder = path.abspath(path.split(__file__)[0])
            with open(folder + '/data/vocab.txt','r') as df :
                cls._vocab = df.read().split('\n')

            cls._all_vocab = Vocab(folder + "/data/vocab_all.txt")


    @classmethod
    def load_synonyms(cls, db):
        """ Load ccam and cim synonyms from database

        Args:
            cls: (object) the class itself
            db: (object) connection to the database

        Returns:
            none

        """
        if cls._instances == 0:
            for code in db.ccam_synonyms.find():
                cls._ccam_syn[code["word"]] = code["syn"]
            for code in db.cim_synonyms.find():
                cls._cim_syn[code["word"]] = code["syn"]


    @classmethod
    def similarity(cls, query, description):
        q = set(query)
        d = set(description)
        return len(q.intersection(d))

    @classmethod
    def description_representation(cls, description):
        return description

    def query_representation(self, query):
        return self._code_dataset.preprocess(query)

    def change_query(self,query,type_code) :
        query = simple_tok(query)
        new_query = ''
        syn = self.__class__._ccam_syn if type_code == 'CCAM' else self.__class__._cim_syn
        for word in query :
            if word in self.__class__._vocab :
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
                    code_des = self._code_dataset.get_description(code_id, type_code)
                    if code_des is not None:
                        results[code_id] = {
                            "metric": metric,
                            "description": code_des["descriptions"][0],
                            "type" : type_code
                        }
            else :
                metric = self.similarity(query, descriptions[0])
                if metric > 0 :
                    code_des = self._code_dataset.get_description(code_id, type_code)
                    if code_des is not None:
                        results[code_id] = {
                            "metric": metric,
                            "description": code_des["descriptions"][0],
                            "type" : type_code
                        }

        return results


if __name__ == "__main__":
    import json

    client = pymongo.MongoClient("mongodb://localhost/codes")
    db = client.codes
    ccam = db

    model_ccam = Model(ccam)
    model_ccam2 = Model(ccam)
    results = model_ccam.predict("muscles","CCAM")
    print results

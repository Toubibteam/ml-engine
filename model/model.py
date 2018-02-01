import tensorflow as tf
import numpy as np


from dataset import CodeDataset,simple_tok,clean
from vocab import Vocab


class Model:
    """Class to compute representation of query and descriptions"""

    def __init__(self, code_dataset,type_code):
        self._code_dataset = code_dataset
        self._descriptions = self._build_descriptions(type_code)


    def _build_descriptions(self,type_code):
        """Load representation once and for all"""
        _descriptions = {}
        for code_id, description, code in self._code_dataset:
            if code == type_code : 
                rep = self.description_representation(description)
                _descriptions[code_id] = rep
        return _descriptions


    def similarity(self, query, description):
        """Dummy now"""
        # TODO(Claire): do something more clever
        q = set(query)
        d = set(description)
        return len(q.intersection(d))


    def description_representation(self, description):
        """Dummy now"""
        # TODO(Claire): do something more clever
        return description


    def query_representation(self, query):
        """Dummy now"""
        # TODO(Claire): do something more clever
        return self._code_dataset.preprocess(query)

    def change_query(self,query,type_code) : 
        if type_code =='CCAM' :
            syn = ccam
        else :
            syn = cim
        query = simple_tok(query)
        new_query = ''
        for word in query : 
            if word in vocab :
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
        query = change_query(query,type_code)
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
    vocab = Vocab("data/vocab.txt")
    all_vocab = Vocab("data/vocab_all.txt")
    with open('data/ccam.json','r') as df :
        ccam = json.load(df)
    with open('data/cim.json','r') as df :
        cim = json.load(df)
    code_dataset = CodeDataset("data/all_code.csv", all_vocab)
    model = Model(code_dataset)
    results = model.predict("muscles",'CCAM')
    print results

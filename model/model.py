from os import path
import json
import pymongo

from dataset import CodeDataset
from tokenizer import Tokenizer
from vocab import Vocab

class Model:
    """Class to compute representation of query and descriptions"""

    """ Class attributes """
    # (int) number of instances created
    _instances = 0
    # (object) tokenizer
    _tkz = Tokenizer()
    # (array) contains all the vocabulary to enrich queries
    _vocab = []
    # (object) handle the token / id convertion
    _all_vocab = None
    # (object) handle the preprocessing of codes descriptions
    _code_dataset = None
    # (dict) contains all the ccam synonyms
    _ccam_syn = {}
    # (dict) contains all the cim synonyms
    _cim_syn = {}
    # (dict) contains all the ccam preprocessed keywords associated to each code. The keys are the code ids
    _ccam_descriptions = {}
    # (dict) contains all the cim preprocessed keywords associated to each code. The keys are the code ids
    _cim_descriptions = {}

    def __init__(self,db):
        self.__class__.load_vocabs()
        self.__class__.load_synonyms(db)

        self.__class__._code_dataset = CodeDataset(db, self.__class__._all_vocab)
        self.__class__.build_descriptions()
        self.__class__._instances += 1
        print "model loaded"


    @classmethod
    def build_descriptions(cls):
        """ Load representations once and for all

        Args:
            cls: (object) the class itself

        Returns:
            none

        """
        if cls._instances == 0:
            for code, descriptions in cls._code_dataset.build_descriptions("CCAM"):
                cls._ccam_descriptions[code] = descriptions
            for code, descriptions in cls._code_dataset.build_descriptions("CIM"):
                cls._cim_descriptions[code] = descriptions


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
                cls._vocab = df.read().strip().split('\n')

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
    def similarity(cls, query, keywords):
        """ Compute the similarity between two sets of words

        Args:
            cls: (object) the class itself
            query: (string) user's query
            keywords: (array) contains dict
                word: (string | number) keyword
                w: (number) weight of the keyword

        Returns:
            similarity: (int)

        """

        q = set(query)
        d = set(keywords.keys())

        similarity = 0
        for k in q.intersection(d):
            similarity += keywords[k]
        return similarity

    @classmethod
    def description_representation(cls, description):
        return description


    def preprocess_query(self, query, type_code):
        """ Preprocess a query for computation

        Args:
            self: (object) class instance
            query: (string) user's query
            type_code: (string) either "CCAM" or "CIM"

        Returns:
            ids: (list) ids of each word

        """
        tokens = self.__class__._tkz.tokenize(query)
        new_tokens = []
        list_synonyms = self.__class__._ccam_syn if type_code == 'CCAM' else self.__class__._cim_syn
        for token in tokens:
            if token in self.__class__._vocab:
                new_tokens.append(token)
            else:
                if token in list_synonyms:
                    syn, weights = [], []
                    for item in list_synonyms[token]:
                        syn.append(item["syn"])
                        weights.append(item["weight"])
                    weights, syn = zip(*sorted(zip(weights, syn)))
                    new_tokens.append(syn[0])

        ids = [ self.__class__._all_vocab.tok_to_id(token) for token in new_tokens ]
        return ids


    def predict(self, query, type_code):
        query = self.preprocess_query(query, type_code)
        results = {}
        codes_descriptions = self.__class__._ccam_descriptions if type_code == 'CCAM' else self.__class__._cim_descriptions
        for code_id, keywords in codes_descriptions.items():
            metric = self.similarity(query, keywords)
            if metric > 0 :
                code_des = self.__class__._code_dataset.get_description(code_id, type_code)["description"]
                results[code_id] = {
                    "metric": metric,
                    "description": code_des,
                    "type" : type_code
                }

        return results


if __name__ == "__main__":
    import json

    client = pymongo.MongoClient("mongodb://localhost/codes")
    db = client.codes
    ccam = db

    model_ccam = Model(ccam)
    results = model_ccam.predict("muscles","CCAM")
    print results

from os import path
import json
import pymongo

from model.model import Model
from model.similarcode import SimilarCodeModel
from model.vocab import Vocab
from model.dataset import CodeDataset

client = pymongo.MongoClient("mongodb://localhost/toubib")

def _sorted_best_50(dico) :
    codes = []
    res_iter = sorted(dico.items(), key=lambda t: t[1]["metric"],reverse=True)
    for code_id, details in res_iter:

        # TODO: add tarif once the attribute has been added in dataset or it breaks the API
        codes.append({
            "type": details["type"],
            "code": code_id,
            "description": details["description"]
        })

    if len(codes) > 50 :
        codes = codes[:50]
    return codes

### Search Codes
def get_code():
    model = Model()

    def model_code_api(input_data):
        results_ccam = model.predict(input_data,'CCAM')
        results_cim = model.predict(input_data,'CIM')

        codes = _sorted_best_50(results_cim) + _sorted_best_50(results_ccam)

        return codes

    return model_code_api

### Similar Codes
def get_similarcode():
    db = client.NOM_DB
    model = SimilarCodeModel(db)

    folder = path.abspath(path.split(__file__)[0])
    all_vocab = Vocab(folder + "/model/data/vocab_all.txt")
    code_dataset = CodeDataset(folder + "/model/data/all_code.csv", all_vocab)

    def model_similarcode_api(input_data):
        cim,ccam = model.same_code(input_data)

        similar_codes = []

        for code in cim :
            description = code_dataset[code]
            similar_codes.append({
                'type' : 'CIM',
                'code' : code,
                'description' : description
                })

        for code in ccam :
            description = code_dataset[code]
            similar_codes.append({
                'type' : 'CCAM',
                'code' : code,
                'description' : description
                })

        return similar_codes

    return model_similarcode_api

from model.model import Model
from model.similarcode import SimilarCodeModel
import json
import pymongo

client = pymongo.MongoClient(NOM_CLIENT)


def _to_json(code_id, metric, description,tarif):
    obj = {
        "code_id": code_id,
        "metric": metric,
        "description": description,
        "tarif" : tarif
    }
    return obj

def _sorted_best_50(dico) :
    codes = []
    res_iter = sorted(dico.items(), key=lambda t: t[1]["metric"],reverse=True)
    for code_id, details in res_iter:
        description = details["description"]
        metric = details["metric"]
        tarif = details["tarif"]
        codes.append(_to_json(code_id, metric, description,tarif))
    if len(codes) > 50 :
        codes = codes[:50]
    return codes

### Search Codes
def get_code():
    model_ccam = Model()

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
    all_vocab = Vocab(folder + "/data/vocab_all.txt")
    code_dataset = CodeDataset(folder + "/data/all_code.csv", self._all_vocab)

    def model_similarcode_api(input_data):
        cim,ccam = model.same_code(input_data)

        similar_codes = []

        for code in cim : 
            description = code_dataset[code]
            similar_codes.append({
                'type' : 'CIM'
                'code' : code, 
                'description' : description
                })

        for code in ccam : 
            description = code_dataset[code]
            similar_codes.append({
                'type' : 'CCAM'
                'code' : code, 
                'description' : description
                })

        return similar_codes

    return model_similarcode_api


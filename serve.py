from os import path
import json
import pymongo

from model.model import Model
from model.vocab import Vocab
from model.dataset import CodeDataset

from config import MONGODB_URI

client = pymongo.MongoClient(MONGODB_URI)

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
    db = client.codes
    model = Model(db)

    def model_code_api(input_data):
        results_ccam = model.predict(input_data,'CCAM')
        results_cim = model.predict(input_data,'CIM')

        codes = _sorted_best_50(results_cim) + _sorted_best_50(results_ccam)

        return codes

    return model_code_api

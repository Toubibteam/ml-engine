from model.model import Model
from model.vocab import Vocab
from model.dataset import CodeDataset
import json


def _to_json(code_id, metric, description):
    obj = {
        "code_id": code_id,
        "metric": metric,
        "description": description
    }
    return obj


def get_model_api():
    model = Model("CCAM")

    def model_api(input_data,type_code):
        results = model.predict(input_data,type_code)

        codes = []

        res_iter = sorted(results.items(), key=lambda t: t[1]["metric"],
                reverse=True)
        for code_id, details in res_iter:
            description = details["description"]
            metric = details["metric"]
            codes.append(_to_json(code_id, metric, description))

        return codes

    return model_api

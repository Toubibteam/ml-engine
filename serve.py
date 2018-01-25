from model.model import Model
from model.vocab import Vocab
from model.dataset import CodeDataset


def _to_html(code_id, metric, description):
    card_html = """<div class="card">
                      <div class="card-body">
                        <h4 class="card-title">{}</h4>
                        <h6 class="card-subtitle mb-2 text-muted">Score: {}</h6>
                        <p class="card-text">{}</p>
                      </div>
                   </div>""".format(code_id, metric,description)
    return card_html


def get_model_api():
    vocab = Vocab("data/vocab.txt")
    all_vocab = Vocab("data/vocab_all.txt")
    with open('data/ccam.json','r') as df :
        ccam = json.load(df)
    with open('data/cim.json','r') as df :
        cim = json.load(df)
    code_dataset = CodeDataset("data/all_code.csv", all_vocab)
    model = Model(code_dataset)

    def model_api(input_data,type_code):
        results = model.predict(input_data,type_code)

        html = ""

        res_iter = sorted(results.items(), key=lambda t: t[1]["metric"],
                reverse=True)
        for code_id, details in res_iter:
            description = details["description"]
            metric = details["metric"]
            element = _to_html(code_id, metric, description)
            html += element

        return html

    return model_api
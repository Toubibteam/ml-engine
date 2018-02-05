from dataset import CodeDataset

class SimilarCodeModel:
    """Class to compute representation of query and descriptions"""

    def __init__(self, similarcode_dataset):
        self._similarcode_dataset = similarcode_dataset

    def same_code(self,code):
        similar_code = self._similarcode_dataset[code]
        cim = similar_code['cim']
        if len(cim) > 10 :
            cim = cim[:10]
        ccam = similar_code['ccam']
        if len(ccam) > 10 :
            ccam = ccam[:10]
        return cim,ccam

if __name__ == "__main__":
    model = Model(code_dataset)
    results = model.same_code("AB001")
    print results

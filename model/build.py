import json
from dataset import CodeDataset
from vocab import build_vocab, write_vocab, Vocab
from nltk.stem import PorterStemmer
import pymongo

client = pymongo.MongoClient('NOM_CLIENT')
db = client.codes 

stemmer = PorterStemmer()
def add_voc(vocab):
	with open('data/cim.json','r') as df :
		cim = json.load(df)
	with open('data/ccam.json','r') as df :
		ccam = json.load(df)
	vocab = vocab + [stemmer.stem(c) for c in cim.keys()] + [stemmer.stem(c) for c in ccam.keys()]
	return vocab

if __name__ == "__main__":
	dataset_cim = CodeDataset(db.cim)
	dataset_ccam = CodeDataset(db.ccam)
    vocab_cim = build_vocab(dataset_cim)
    vocab_ccam = build_vocab(dataset_ccam)
    write_vocab(vocab_cim + vocab_ccam, "data/vocab.txt")

    all_vocab = add_voc(vocab)
    write_vocab(all_vocab, "data/vocab_all.txt")

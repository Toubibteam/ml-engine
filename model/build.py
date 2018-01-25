import json
from dataset import CodeDataset
from vocab import build_vocab, write_vocab, Vocab

def add_voc(vocab):
	with open('data/cim.json','r') as df : 
		cim = json.load(df)
	with open('data/ccam.json','r') as df : 
		ccam = json.load(df)
	vocab = vocab + cim.keys() + ccam.keys()
	return vocab

if __name__ == "__main__":
    dataset = CodeDataset("data/all_code.csv")
    vocab = build_vocab(dataset)
    write_vocab(vocab, "data/vocab.txt")
    all_vocab = add_voc(vocab)
    write_vocab(all_vocab, "data/vocab_all.txt")
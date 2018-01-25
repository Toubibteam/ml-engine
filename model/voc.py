import pandas as pd
import string

data = pd.read_csv("data/ccam_simple.csv",sep=';')

proc = data['Proc'].tolist()

print proc

def preprocess(description):
	vocab = []
	result = description.split(' ')
	result = [tok for tok in result if tok not in list(string.punctuation)]
	return result

voc = []
for p in proc :
	voc += preprocess(p)


voc_ = '\n'.join(list(set(voc)))

with open('voc.txt','w') as df :
	df.write(voc_)


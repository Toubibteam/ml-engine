# -*- coding: utf-8 -*-
import json
import gensim
import numpy as np

model = gensim.models.KeyedVectors.load('keyword_model.w2v')  

with open('ccam1.json','r') as df :
	ccam = json.load(df)
with open('cim1.json','r') as df :
    cim = json.load(df)

data = cim

for key in data.keys() : 
	temp  = data[key]
	for t in temp : 
		if t['syn'] in key :
			t['weight'] = 1
		else : 
			try :
				keys = key.split(' ')
				maxi = 0 
				for k in keys :
					sim =  model.similarity(t['syn'],k)
					if sim > maxi :
						maxi = sim
				t['weight'] = maxi
			except :
				pass	



with open('cim2.json','w') as df :
	json.dump(data,df)

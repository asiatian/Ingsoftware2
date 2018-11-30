import tweepy
import sys
import os
import json
import pandas as pd
import re
from datetime import datetime, timedelta
from textblob import TextBlob

zoits = ["futaleufu","putre","osorno","valparaiso"]

if not os.path.exists('output'):
	os.makedirs('output')
folderName = str(datetime.now().date()-timedelta(1)) 
for lugar in zoits:
	if(os.path.isfile('output/'+lugar+'_palabras.csv')):
		df = pd.read_csv(lugar+'_palabras.csv',index_col=0)
		bolsa = df.to_dict("split")
		bolsa = dict(zip(bolsa["index"],bolsa["data"]))
		print(df)
	else:
		bolsa = None
	direcion = folderName + '/' + lugar + '.json'
	with open(direcion) as f:
		content = f.readlines()
		pos_contador = 0
		neg_contador = 0
		neu_contador = 0
		popular = None
		flag = 0
		for x in content:
			x = json.loads(x)
			if(flag==0):
				popular=x
				flag += 1
			if 'created_at' in x:
				zen = TextBlob(x['text'])
				if 'RT' in zen:
					continue
				else:
					try:
						eng = zen.translate(to = 'en')
						if(eng.sentiment.polarity > 0):
							pos_contador += 1
						elif(eng.sentiment.polarity == 0):
							neu_contador += 1
						else:
							neg_contador += 1 
					except Exception as e:
						if(zen.sentiment.polarity > 0):
							pos_contador += 1
						elif(zen.sentiment.polarity == 0):
							neu_contador += 1
						else:
							neg_contador += 1 
				if(x['lang']=='es'):
					wordlist = re.sub(r'#\S+|http\S+|@\S+|\b[a-z]{2}\b|\b[a-z]{3}\b|\b[a-z]{1}\b|[^\w]|[?|$|.|!|…]|\b\d+(?:\.\d+)?\s+', ' ',  x['text'].lower(),flags=re.MULTILINE).split()
					#print(wordlist)
					for palabra in wordlist:
						if(bolsa == None):
							bolsa = {palabra : (1)}
						elif palabra in bolsa:
							bolsa[palabra] += 1
						else:
							bolsa[palabra] = (1)
				if(flag == 0 ):
					popular = x
					flag += 1
				elif(x['favorite_count'] > popular['favorite_count']):
					popular = x
		datos = [ {'Fecha': folderName, 'Positivos': pos_contador,'Neutrales': neu_contador,'Negativos': neg_contador,'Twitt del dia': popular['text'] } ]
		df = pd.DataFrame(datos)
		df = df[['Fecha','Positivos','Neutrales','Negativos','Twitt del dia']]
		if (os.path.isfile('output/'+lugar+'.csv')):
			with open('output/'+lugar+'.csv','a') as f:
				df.to_csv(f,header=False)
		else:
			df.to_csv('output/'+lugar+'.csv',sep=';',encoding='utf-8')
		df2 = pd.DataFrame.from_dict(bolsa,orient="index")
		#for k,v in bolsa.items():
		#	print(k,v)
			#print(palabra[0])
		#	df2.loc[k] = v 
		df2.to_csv('output/'+lugar+'_palabras.csv')
		#df.to_csv(lugar+'.csv',sep='\t',encoding='utf-8')
		print("En {} cantidad de positivos = {}, cantidad de neutros = {}, cantidad negativos = {}".format(lugar,pos_contador,neu_contador,neg_contador))

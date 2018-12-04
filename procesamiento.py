import sys
import os
import json
import pandas as pd
import re
from datetime import datetime, timedelta
from textblob import TextBlob

# # GLOBALES # #
zoits = ["futaleufu","putre","osorno","valparaiso"]
if not os.path.exists('output'):
	os.makedirs('output')
folderName = str(datetime.now().date()-timedelta(1))
# # # # # # # #
## FUNCIONES ##
def leer_bolsa(lugar):
	if(os.path.isfile('output/'+lugar+'_palabras.csv')):
		df = pd.read_csv(lugar+'_palabras.csv',index_col=0)
		bolsa = df.to_dict("split")
		bolsa = dict(zip(bolsa["index"],bolsa["data"]))
		return bolsa
	else:
		return None

def spanish_sentimiento(texto,positivos,neutrales,negativos):
	return positivos,neutrales,negativos

def english_sentimiento(texto,positivos,neutrales,negativos):
	zen = TextBlob(texto)
	if(zen.sentiment.polarity > 0):
		positivos += 1
	elif(zen.sentiment.polarity == 0):
		neutrales += 1
	else:
		negativos += 1
	return positivos,neutrales,negativos

def buscar_popular(popular,tweet):
	if(popular == None):
		popular = tweet
	elif(tweet['favorite_count'] > popular['favorite_count']):
		popular = tweet
	return popular

def crear_output (lugar,positivos,neutrales,negativos,popular):
	datos = [{
		'fecha': folderName, 
		'positivos': positivos,
		'neutrales': neutrales, 
		'negativos': negativos, 
		'mas favorito':popular['text']}]
	df = pd.DataFrame(datos)
	df = df[[
		'Fecha',
		'Positivos',
		'Neutrales',
		'Negativos',
		'Twitt del dia']]
	namefile='output/'+lugar+'.csv'
	if (os.path.isfile(namefile)):
		with open (namefile,'a') as f:
			df.to_csv(f,header=False)
	else:
		df.to_csv(namefile,sep='\t',encoding='utf-8')
	return

def crear_bolsa(lugar,bolsa):
	df = pd.DataFrame.from_dict(bolsa,orient='index')
	df.to_csv('output/'+lugar+'_palabras.csv')

def normalizar(texto):
	texto = texto.lower()
	listaPalabras = re.compile(r'\W+|\b[a-z]{1}\b|\b[a-z]{2}\b', re.UNICODE).split(texto)
	for x in listaPalabras:
		print x
	return

## ............. ##

for lugar in zoits:
	bolsa = leer_bolsa(lugar)
	direcion = folderName + '/' + lugar + '.json'
	with open(direcion) as f:
		content = f.readlines()
		pos_contador = 0
		neg_contador = 0
		neu_contador = 0
		popular = None
		for tweet in content:
			tweet = json.loads(tweet)
			if 'RT' in tweet['text']:
				continue
			else:
				if(tweet['lang']=='es'):
					normalizar(tweet['text'])
					pos_contador,neu_contador,neg_contador=spanish_sentimiento(tweet['text'],pos_contador,neu_contador,neg_contador)
				elif(tweet['lang']=='en'):
					pos_contador,neu_contador,neg_contador=english_sentimiento(tweet['text'],pos_contador,neu_contador,neg_contador)
				popular = buscar_popular(popular,tweet)
		#crear_output(lugar,pos_contador,neu_contador,neg_contador,popular)
		#crear_bolsa(lugar,bolsa)



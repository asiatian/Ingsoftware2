import sys, os , json ,re
import pandas as pd
import nltk, unicodedata, inflect
import indicoio
from datetime import datetime, timedelta
from textblob import TextBlob
from nltk.corpus import stopwords

indicoio.config.api_key = "35f35a51d29abd242a14ce2ff950e70d"

# # GLOBALES # #
zoits = ["futaleufu","putre","osorno","valparaiso"]
if not os.path.exists('output'):
	os.makedirs('output')
#folderName = str(datetime.now().date()-timedelta(1))
folderName = "2018-12-05"
# # # # # # # #
## FUNCIONES ##
def leer_bolsa(lugar):
	if(os.path.isfile('output/'+lugar+'_palabras.csv')):
		df = pd.read_csv('output/'+lugar+'_palabras.csv',index_col=0)
		bolsa = df.to_dict("split")
		bolsa = dict(zip(bolsa["index"],bolsa["data"][0]))
		return bolsa
	else:
		return None

def spanish_sentimiento(texto,positivos,neutrales,negativos):
	resultado = indicoio.sentiment(texto,lang='spanish')
	if (resultado >= 0.6 ):
		positivos += 1
	elif (resultado < 0.6 and 0.5 >= resultado):
		neutrales += 1
	else:
		negativos += 1
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
		'Twitt del dia':popular['text']}]
	df = pd.DataFrame(datos)
	df = df[[
		'fecha',
		'positivos',
		'neutrales',
		'negativos',
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
	return

def remover_non_ascii(listaPalabras):
	nueva_lista = []
	for palabra in listaPalabras:
		nueva_palabra = unicodedata.normalize('NFKD',palabra).encode('ascii','ignore').decode('utf-8','ignore')
		nueva_lista.append(nueva_palabra)
	return nueva_lista

def remover_puntuacion(listaPalabras):
	nueva_lista = []
	for palabra in listaPalabras:
		if(len(palabra)<13 and len(palabra)>3):
			nueva_palabra = re.sub(r'http\S+|[^\w\s]|[_]','',palabra)
			if nueva_palabra != '':
				nueva_lista.append(nueva_palabra)
	return nueva_lista

def replace_numbers(listaPalabras):
	p = inflect.engine()
	nueva_lista = []
	for palabra in listaPalabras:
		if palabra.isdigit():
			continue
		else:
			nueva_lista.append(palabra)
	return nueva_lista

def remove_stopwords(listaPalabras):
	nueva_lista = []
	for palabra in listaPalabras:
		if(len(palabra)<13 and len(palabra)>3):
			if palabra not in stopwords.words('spanish'):
				nueva_lista.append(palabra)
	return nueva_lista

def normalizar(texto,bolsa):
	texto = texto.lower()
	listaPalabras = nltk.word_tokenize(texto)
	listaPalabras = remover_non_ascii(listaPalabras)
	listaPalabras = remover_puntuacion(listaPalabras)
	listaPalabras = replace_numbers(listaPalabras)
	listaPalabras = remove_stopwords(listaPalabras)
	for palabra in listaPalabras:
		if bolsa == None:
			bolsa = {palabra : 1}
		elif palabra in bolsa:	
			bolsa[palabra] += 1
		else:
			bolsa[palabra] = 1
	return bolsa

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
					bolsa=normalizar(tweet['text'],bolsa)
					pos_contador,neu_contador,neg_contador=spanish_sentimiento(tweet['text'],pos_contador,neu_contador,neg_contador)
				elif(tweet['lang']=='en'):
					pos_contador,neu_contador,neg_contador=english_sentimiento(tweet['text'],pos_contador,neu_contador,neg_contador)
				popular = buscar_popular(popular,tweet)
		#print(bolsa)
		crear_output(lugar,pos_contador,neu_contador,neg_contador,popular)
		crear_bolsa(lugar,bolsa)


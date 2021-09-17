# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:17:34 2021

@author: eicruzl
"""
import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json',encoding='utf-8').read())

words = pickle.load(open('words.pkl', 'rb'))
tags = pickle.load(open('tags.pkl', 'rb'))

model = load_model('chatbotmodel.h5')

# create a data structure to hold user context
context = {}

def clean_up_sentence(sentence):
	sentence_words = nltk.word_tokenize(sentence)
	sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
	return sentence_words

def bag_of_words(sentence):
	sentence_words = clean_up_sentence(sentence)
	bag = [0] * len(words)
	for w in sentence_words:
		for i, word in enumerate(words):
			if word == w:
				bag[i] = 1
	return np.array(bag)

def predict_tag(sentence):
	bagOfWords = bag_of_words(sentence)
	res = model.predict(np.array([bagOfWords]))[0]
	ERROR_THRESHOLD = 0.25 # 25%
	results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

	results.sort(key=lambda x: x[1], reverse=True)
	return_list = []
	for r in results:
		return_list.append({'intent':  tags[r[0]], 'probability': r[1]})
	return return_list

def get_response(message):
    predictedTags = predict_tag(message)
    probability = predictedTags[0]['probability'];
    userID = 123
  
    if (probability > 0.7):
        response = ""
        tag = predictedTags[0]['intent']
        allIntents = intents['intents']
        for i in allIntents:
            if i['tag'] == tag:
			   #response = random.choice(i['responses'])
               #print(random.choice(i['responses']))
               # añadimos el contexto siempre y cuando lo tenga
               if 'context_set' in i:
                   context[userID] = i['context_set']

               # Verificamos si hay contexto para el usuario
               if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        # Respuesta
                        response = random.choice(i['responses'])
                        break
        return response
    else: # 
        return "Lo siento, pensé en lo que dijiste, pero aún no estoy seguro de cómo responder."
   
"""
start = True
while start:
	query = input('tu: ')
	if query in ["bye","see you later","goodbye","sayonara","hasta luego","chau","adios","ya vete"]:
		start = False
		continue
	try:
		res = get_response(query)
		print("BotSito:",res + '\n')
	except:
            print('-------')
"""

    
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:17:34 2021

@author: eicruzl
"""
import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
nltk.download('punkt')
nltk.download('wordnet')
# esto nos ayuda a reducir las mejores palabras "trabajando", "trabaje", "trabajo", a "trabajo"
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()

#cargamos el json con los intents
intents = json.loads(open('intents.json').read())

words = []
tags = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
	for pattern in intent['patterns']:
		word_list = nltk.word_tokenize(pattern.lower())
		words.extend(word_list)
		documents.append((word_list, intent['tag']))
		if intent['tag'] not in tags:
			tags.append(intent['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
print(words)
words = sorted(set(words))

tags = sorted(set(tags))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(tags, open('tags.pkl', 'wb'))

training = []
output = [0] * len(tags)

for document in documents:
	bag = []
	word_patterns = document[0]
	word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
	for word in words:
		bag.append(1) if word in word_patterns else bag.append(0)

	output_row = list(output)
	output_row[tags.index(document[1])] = 1
	training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])


#Aqui creamos las capasde la neurona
oculta1 = tf.keras.layers.Dense(units=128, input_shape=(len(train_x[0]),), activation='relu')
oculta1_drop = tf.keras.layers.Dropout(0.5)

oculta2 = tf.keras.layers.Dense(units=64,activation='relu')
oculta2_drop = tf.keras.layers.Dropout(0.5)

salida = tf.keras.layers.Dense(len(train_y[0]), activation='softmax')
modelo = tf.keras.Sequential([oculta1,oculta1_drop,oculta2,oculta2_drop, salida])

#sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
#gradiente descendente= sgd
modelo.compile(
    optimizer=tf.keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True),
    loss='categorical_crossentropy',
     metrics=['accuracy']
)

print("Comenzando entrenamiento...")
hist = modelo.fit(np.array(train_x), np.array(train_y), epochs=1000, verbose=True)
print("Modelo entrenado!")

scores = modelo.evaluate(train_x, train_y)
print("precision del modelo \n%s: %.2f%%" % (modelo.metrics_names[1], scores[1]*100))
###-----------------------

modelo.save('chatbotmodel.h5', hist)

print("Done")



































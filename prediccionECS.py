# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:17:34 2021

@author: eicruzl
"""
from tensorflow.keras.models import load_model

modelo = load_model('prediccionECS.h5')

print("Hagamos una predicción!")
resultado = modelo.predict([[8,21]])
print("El resultado es " + str(resultado) + " archivos a llegar!")

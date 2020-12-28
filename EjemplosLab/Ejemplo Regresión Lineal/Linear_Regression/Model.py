#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import numpy as np

ALPHA = 0.000001 #Taza de aprendizaje
MAX_ITERATIONS = 1000
MIN_VALUE = 0.5 #Valor más bajo que se busca encontrar en la función de costo

class Model:

    def __init__(self, data):
        # Se inicializan los coeficientes del modelo
        self.coefficients = np.random.random(4)
        self.bitacora = []
        # Se extraen los conjuntos de datos
        #Se extrae un 80% para el conjunto de entrenamiento
        #Se extrae un 20% para el conjunto de prueba
        slice_point = int(len(data)*0.8)
        self.training_set = data[:slice_point, :]
        self.test_set = data[slice_point:, :]

    def training(self):
        m = len(self.training_set) #Tamaño del valor de entrenamiento
        
        iterations = 0

        #Tomo el valor de las variables independientes (x1, x2, x3, ..., xn)
        x = self.training_set[:, :3]

        #Tomo el valor de la variable dependiente (y)
        y = self.training_set[:, 3]


        cost = self.cost_function(x, y, m) #Veo qué tan buenos son los coeficientes actuales del modelo
        end = self.finalization(cost, iterations) #Verifico si ya terminó el entrenamiento
        
        while not end:
            gradient = self.get_gradient(x, y, m)
            self.update_coefficients(gradient)
            cost = self.cost_function(x, y, m)
            iterations += 1
            end = self.finalization(cost, iterations)

    def update_coefficients(self, gradient):
        self.coefficients = self.coefficients - ALPHA * gradient

    def get_gradient(self, x, y, m):
        #Se crea un arreglo de tamaño 4 porque se tiene [B0, B1, B2, B3]
        gradient = np.array([0, 0, 0, 0])
        c = self.coefficients
        tam = len(self.coefficients)
        
        for i in range(tam):
            
            temp = c[0]+c[1:].dot(x.transpose())-y
            
            if i != 0:
                temp = temp*x[:, i-1]
                
            
            #gradient[i] = (1 / m)*sum(temp)
            t1 = float(1/float(m))
            t2 = sum(temp)
            t3 = t1 * t2
            gradient[i] = t3
        
        return gradient

    def finalization(self, cost, iterations):
        self.bitacora.append(cost)
        if cost < MIN_VALUE:
            return True
        elif iterations > MAX_ITERATIONS:
            return True
        else:
            return False

    #Indica qué tan buenos son los coeficientes del modelo
    def cost_function(self, x, y, m):
        c = self.coefficients #Tomo los coeficientes

        #x.transpose()#Se calcúla la transpuesta de X
        """
            x = [   
                     X1, X2, X3
                    [1,  2,  3],
                    [4,  5,  6],
                    [7,  8,  9]
                    [   ...   ]  <--- Aquí sigue si hay más registros para el modelo
                ]
            
            Si se calcula la transpuesta
            xT = [
                    [1, 4, 7], <--- X1
                    [2, 5, 8], <--- X2
                    [3, 6, 9]  <--- X3
                    [  ...  ]  <--- Xn Esto depende de la cantidad de variables independientes
                ]
        """
        #c[1:].dot(x.transpose())
        #c[1:] Se toman los coeficientes (B1, B2, B3, ..., Bn) NO se toma B0
        #c[1:].dot(x.transpose()) Se multiplica la matriz de coeficientes por la transpuesta de X
        #para obtener una matriz de Y con valores calculados por el modelo
        """
            xT = [
                    [1, 4, 7], <--- X1
                    [2, 5, 8], <--- X2
                    [3, 6, 9]  <--- X3
                    [  ...  ]  <--- Xn Esto depende de la cantidad de variables independientes
                ]

            c = [B1, B2, B3, ..., Bn]
            
            El resultado es una matriz de N columnas y una fila, donde N es la cantidad de registros
            en 'x' que es el conjunto de entrenamiento y una fila porque la matriz de coeficientes tiene una fila
            
            c.dot(xT) = [
                            (1*B1 + 2*B2 + 3*B3), (4*B1 + 5*B2 + 6*B3), (7*B1 + 8*B2 + 9*B3), ...
                        ]

        """
        #c[0]+c[1:].dot(x.transpose()) Se le suma el valor de B0 a todos los elementos de la matriz de Y calculada

        #c[0]+c[1:].dot(x.transpose())-y Se resta la Y calculada con la Y real
        
        temp = c[0]+c[1:].dot(x.transpose())-y

        #Se termina de calcular la función de costo
        t1 = 2*m
        t2 = float(1 / float(t1))
        t3 = temp**2
        t4 = sum(t3)
        t5 = t2 * t4
        
        #return (1/(2*m))*sum(temp**2)
        return t5

#!/usr/bin/env python
import math
import numpy as np
from random import randrange, uniform, shuffle
from Main import getModelo


class Nodo:
    def __init__(self, solucion=[], fitness=0):
        self.solucion = solucion
        self.fitness = fitness


# VARIABLES DE EVALUACION DEL FITNESS
# Número máximo de generaciones que va a tener el algoritmo
maximo_generaciones = 1000
arrAlpha = [0.1, 0.5, 0.01, 0.05, 0.001,
            0.005, 0.0001, 0.0005, 0.00001, 0.00005]
arrLambda = [0, 0.2, 0.5, 0.9, 1, 3, 3.5, 7, 0.75, 0.8]
arrMaxIt = [2500, 5000, 7500, 10000, 12500,
            15000, 17500, 20000, 22500, 25000]
arrKeepProv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

"""
*   Función que crea la población
"""


def inicializarPoblacion():
    global arrAlpha
    global arrLambda
    global arrMaxIt
    global arrKeepProv

    shuffle(arrAlpha)
    shuffle(arrLambda)
    shuffle(arrMaxIt)
    shuffle(arrKeepProv)

    poblacion = []

    print("Inicializando población")
    for i in range(len(arrAlpha)):
        solucion = [arrAlpha[i], arrMaxIt[i], arrLambda[i], arrKeepProv[i]]
        individuo = Nodo(solucion, evaluarFitness(solucion))
        poblacion.append(individuo)

    return poblacion  # Retorno la población ya creada


"""
*   Función que verifica si el algoritmo ya llegó a su fin
"""


def verificarCriterio(poblacion, generacion):
    global maximo_generaciones

    if generacion >= maximo_generaciones:
        return True

    # Calculo el valor fitness de los individuos
    for individuo in poblacion:
        individuo.fitness = evaluarFitness(individuo.solucion)
        # Si el fitness es menor o igual a fitness_mei
        if individuo.fitness <= 0:
            return True

    return None


"""
*   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
"""


def evaluarFitness(solucionIndividuo):
    model, fitness = getModelo(solucionIndividuo[0], solucionIndividuo[1],
                               solucionIndividuo[2], solucionIndividuo[3])

    return fitness


"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""


def seleccionarPadres(poblacion):
    padres = []

    poblacionOrdenada = sorted(poblacion, key=lambda item: item.fitness, reverse=True)[
        : len(poblacion)]  # Los ordena de mayor a menor

    for i in range(round(len(poblacionOrdenada)/2)):
        padres.append(poblacionOrdenada[i])

    return padres


"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
*   Se va a alternar los bits de ambos padres
*   Se va a tomar un bit del padre 1, un bit del padre 2 y así sucesivamente
"""


def cruzar(padre1, padre2):
    hijo = []
    for i in range(len(padre1)):
        # 50% de probabilidad de ser de algún padre
        hijo.append(padre1[i] if randrange(2) == 0 else padre2[i])

    return hijo  # Retorno al hijo ya cruzado


"""
*   Función que toma una solución y realiza la mutación
"""


def mutar(solucion):
    global arrAlpha
    solucion[randrange(len(arrAlpha))] = randrange(10)
    return solucion  # Retorno la misma solución, solo que ahora mutó


"""
*   Función que toma a los mejores padres y genera nuevos hijos
"""


def emparejar(padres):
    global arrAlpha
    total_hijos_a_crear = len(arrAlpha) - len(padres)
    pilaPadres = padres[:]

    # Creo un arreglo de hijos para luego ordenarlos
    hijos = []
    for i in range(total_hijos_a_crear):
        hijo = Nodo()
        pilaPadres = padres[:] if len(pilaPadres) <= 1 else pilaPadres
        hijo.solucion = cruzar(pilaPadres.pop().solucion,
                               pilaPadres.pop().solucion)
        hijo.solucion = mutar(hijo.solucion) if randrange(
            2) == 0 else hijo.solucion
        hijo.fitness = evaluarFitness(hijo.solucion)
        hijos.append(hijo)

    # Ordeno a los padres en orden ascendente, de mayor a menor
    padres = sorted(padres, key=lambda item: item.fitness, reverse=True)[
        :len(padres)]  # Los ordena de mayor a menor
    # Ordeno a los hijos en orden ascendente, de mayor a menor
    hijos = sorted(hijos, key=lambda item: item.fitness, reverse=True)[
        :len(hijos)]  # Los ordena de mayor a menor

    # La nueva población se hará de la siguiente manera:
    return np.concatenate((padres, hijos))


"""
*   Método para imprimir los datos de una población
"""


def imprimirIndividuo(individuo):
    print('Individuo: ', individuo.solucion, ' Fitness: ', individuo.fitness)


def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        imprimirIndividuo(individuo)


"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""


def ejecutar():
    print("Ejecutando algoritmo genético")
    generacion = 0
    poblacion = inicializarPoblacion()
    fin = verificarCriterio(poblacion, generacion)

    # Imprimo la población
    print('*************** GENERACION ', generacion, " ***************")
    imprimirPoblacion(poblacion)

    while(fin == None):
        padres = seleccionarPadres(poblacion)
        poblacion = emparejar(padres)
        generacion += 1
        fin = verificarCriterio(poblacion, generacion)

        # Imprimo la población
        print('*************** GENERACION ', generacion, " ***************")
        imprimirPoblacion(poblacion)

    # Obtengo la mejor solución y la muestro
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=True)[
        :1]  # Los ordena de mayor a menor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR INDIVIDUO***************')
    imprimirIndividuo(mejorIndividuo)


# Corro el algoritmo
ejecutar()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from random import randrange


class Nodo:
    def __init__(self, solucion=[], fitness=0, x=0):
        self.solucion = solucion
        self.fitness = fitness


# CONSTANTES DEL ALGORITMO
maximo_generaciones = 2  # Número máximo de generaciones que va a tener el algoritmo
poblacionInicial = 10  # Número de individuos a evaluar
solucion = [1, 5, 7, 8, 6, 9, 3, 4]  # Solución que esperamos encontrar


def getRandoms():
    global solucion
    randoms = []
    limit = len(solucion)
    for i in range(limit):
        randoms.append(randrange(10))
    return randoms


"""
*   Función que crea la población
"""


def inicializarPoblacion():
    global poblacionInicial
    poblacion = []

    for i in range(poblacionInicial):
        randoms = getRandoms()
        individuo = Nodo(randoms, evaluarFitness(randoms))
        poblacion.append(individuo)

    return poblacion  # Retorno la población ya creada


"""
*   Función que verifica si el algoritmo ya llegó a su fin
"""


def verificarCriterio(poblacion, generacion):
    # Si ya llegó al máximo de generaciones lo detengo
    if generacion >= maximo_generaciones:
        return True

    # Calculo el valor fitness de los individuos
    for individuo in poblacion:
        individuo.fitness = evaluarFitness(individuo.solucion)
        # Si el fitness es mayor o igual a 7
        if individuo.fitness >= 7:
            return True

    return None


"""
*   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
"""


def evaluarFitness(solucionIndividuo):
    global solucion
    fitness = 0
    for i in range(len(solucion)):
        fitness += 1 if solucion[i] == solucionIndividuo[i] else 0
    return fitness


"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""


def seleccionarPadres(poblacion):
    # Los padres se seleccionan por sus fitness
    padres = []

    # Ordeno a los padres en orden ascendente, de menor a mayor
    poblacionOrdenada = sorted(poblacion, key=lambda item: item.fitness, reverse=True)[
        : len(poblacion)]  # Los ordena de mayor a menor

    for i in range(5):
        padres.append(poblacionOrdenada[i])

    return padres


"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
*   Se va a alternar los bits de ambos padres
*   Se va a tomar un bit del padre 1, un bit del padre 2 y así sucesivamente
"""


def cruzar(padre1, padre2):
    hijo = [padre2[0], padre2[1], padre1[2], padre1[3],
            padre2[4], padre2[5], padre1[6], padre1[7]]
    return hijo  # Retorno al hijo ya cruzado


"""
*   Función que toma una solución y realiza la mutación
*   Se va a cambiar el bit con valor 0 más a la izquierda por 1
"""


def mutar(solucion):
    for i in range(0, len(solucion)):
        if randrange(1) == 1:
            # Cambio el valor por uno random de 0 - 9
            solucion[i] = randrange(9)
    return solucion  # Retorno la misma solución, solo que ahora mutó


"""
*   Función que toma a los mejores padres y genera nuevos hijos
"""


def emparejar(padres):
    # Se van a generar 2 nuevos hijos, se tienen 2 padres
    # Genero al hijo 1
    hijo1 = Nodo()
    hijo1.solucion = cruzar(padres[0].solucion, padres[1].solucion)
    hijo1.solucion = mutar(hijo1.solucion)

    # Genero al hijo 2
    hijo2 = Nodo()
    hijo2.solucion = cruzar(padres[2].solucion, padres[4].solucion)
    hijo2.solucion = mutar(hijo2.solucion)

    # Genero al hijo 3
    hijo3 = Nodo()
    hijo3.solucion = cruzar(padres[0].solucion, padres[2].solucion)
    hijo3.solucion = mutar(hijo3.solucion)

    # Genero al hijo 4
    hijo4 = Nodo()
    hijo4.solucion = cruzar(padres[2].solucion, padres[3].solucion)
    hijo4.solucion = mutar(hijo4.solucion)

    # Genero al hijo 5
    hijo5 = Nodo()
    hijo5.solucion = cruzar(padres[0].solucion, padres[4].solucion)
    hijo5.solucion = mutar(hijo5.solucion)

    # Ordeno a los padres en orden ascendente, de menor a mayor
    padres = sorted(padres, key=lambda item: item.fitness, reverse=True)[
        :len(padres)]  # Los ordena de menor a mayor

    # Creo un arreglo de hijos para luego ordenarlos
    hijos = [hijo1, hijo2, hijo3, hijo4, hijo5]
    # Ordeno a los hijos en orden ascendente, de menor a mayor
    hijos = sorted(hijos, key=lambda item: item.fitness, reverse=True)[
        :len(hijos)]  # Los ordena de menor a mayor

    # La nueva población se hará de la siguiente manera:
    return [padres[0], hijos[1], padres[1], hijos[0], padres[2], hijos[2], padres[3], hijos[3], padres[4], hijos[4]]


"""
*   Método para imprimir los datos de una población
"""


def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        print('Individuo: ', individuo.solucion,
              ' Fitness: ', individuo.fitness)


"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""


def ejecutar():
    # np.seterr(over='raise')
    print("Algoritmo corriendo")

    generacion = 0
    poblacion = inicializarPoblacion()
    fin = verificarCriterio(poblacion, generacion)

    # Imprimo la población
    print('*************** GENERACION ', generacion, " ***************")
    imprimirPoblacion(poblacion)

    while(fin == None):
        padres = seleccionarPadres(poblacion)
        poblacion = emparejar(padres)
        generacion += 1  # Lo pongo aquí porque en teoría ya se creó una nueva generación
        fin = verificarCriterio(poblacion, generacion)
        #generacion += 1

        # Imprimo la población
        print('*************** GENERACION ', generacion, " ***************")
        imprimirPoblacion(poblacion)

    # Obtengo la mejor solución y la muestro
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=True)[
        :1]  # Los ordena de menor a mayor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR INDIVIDUO***************')
    print('Individuo: ', mejorIndividuo.solucion,
          ' Fitness: ', mejorIndividuo.fitness)


# Corro el algoritmo
ejecutar()

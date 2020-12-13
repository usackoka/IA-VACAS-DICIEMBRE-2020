#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import math
from random import randrange, uniform


class Nodo:
    def __init__(self, solucion=[], fitness=0):
        self.solucion = solucion
        self.fitness = fitness


class NodoExcel:
    def __init__(self, proyecto1=0, proyecto2=0, proyecto3=0, proyecto4=0, notaReal=0):
        self.proyecto1 = proyecto1
        self.proyecto2 = proyecto2
        self.proyecto3 = proyecto3
        self.proyecto4 = proyecto4
        self.notaReal = notaReal


# CONSTANTES DEL ALGORITMO
data = [NodoExcel(75, 50, 90, 65, 71.75), NodoExcel(80, 95, 88, 80, 84.65), NodoExcel(
    20, 55, 60, 58, 52.45), NodoExcel(60, 28, 69, 50, 53.9)]  # Data cargada del excel
total_genes = 4  # Número de genes por individuo
maximo_generaciones = 100  # Número máximo de generaciones que va a tener el algoritmo
poblacionInicial = 30  # Número de individuos a evaluar

# VARIABLES DE EVALUACION DEL FITNESS
fitness_mai = 10  # Número a cumplir mayor o igual para fitness
fitness_mei = 10  # Número a cumplir menor o igual para fitness
promedioFitness = 0  # Número a comparar para el promedio de fitness en una solución


def getRandoms():
    global total_genes
    randoms = []
    for i in range(total_genes):
        randoms.append(uniform(-2.0, 2.0))
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


def verificarCriterio(poblacion, generacion, seleccion):
    global fitness_mai
    global fitness_mei
    global promedioFitness

    if seleccion == 'generacion':
        # Si ya llegó al máximo de generaciones lo detengo
        if generacion >= maximo_generaciones:
            return True
    elif seleccion == 'fitness_mai':
        # Calculo el valor fitness de los individuos
        for individuo in poblacion:
            individuo.fitness = evaluarFitness(individuo.solucion)
            # Si el fitness es mayor o igual a fitness_mai
            if individuo.fitness >= fitness_mai:
                return True
    elif seleccion == 'fitness_mei':
        # Calculo el valor fitness de los individuos
        for individuo in poblacion:
            individuo.fitness = evaluarFitness(individuo.solucion)
            # Si el fitness es menor o igual a fitness_mei
            if individuo.fitness <= fitness_mei:
                return True
    elif seleccion == 'promedio':
        # Calculo el valor fitness de los individuos
        result_fitness = []
        for individuo in poblacion:
            individuo.fitness = evaluarFitness(individuo.solucion)
            result_fitness.append(individuo.fitness)

        # saco el promedio de los fitness
        prom = 0
        for i in range(len(result_fitness)):
            prom += result_fitness[i]
        prom = prom / len(result_fitness)

        if prom == promedioFitness or promedioFitness == round(prom):
            return True

    return None


"""
*   Función que evalúa qué tan buena es una solución, devuelve el valor fitness de la solución
"""


def evaluarFitness(solucionIndividuo):
    global data
    global total_genes

    # Calculo el error cuadrático medio
    fitness = 0
    cantidad_de_datos = len(data)
    sumatorias = []
    for i in range(cantidad_de_datos):
        fila = data[i]
        nota_calculada = (fila.proyecto1*solucionIndividuo[0]) + (fila.proyecto2*solucionIndividuo[1]) + (
            fila.proyecto3 * solucionIndividuo[2]) + (fila.proyecto4 * solucionIndividuo[3])
        calculo = fila.notaReal - nota_calculada
        calculo = math.pow(calculo, 2)
        sumatorias.append(calculo)

    suma = 0
    for i in range(len(sumatorias)):
        suma += sumatorias[i]

    fitness = suma / cantidad_de_datos

    return fitness


"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""


def seleccionarPadres(poblacion, seleccion):
    padres = []

    # Ordeno a los padres en orden ascendente, de menor a mayor
    poblacionOrdenada = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[
        : len(poblacion)]  # Los ordena de menor a mayor

    if seleccion == 'fitness':
        for i in range(round(len(poblacionOrdenada)/2)):
            padres.append(poblacionOrdenada[i])
    elif seleccion == 'pares':
        for i in range(len(poblacion)):
            if i % 2 == 0:
                padres.append(poblacion[i])
    elif seleccion == 'impares':
        for i in range(len(poblacion)):
            if i % 2 != 0:
                padres.append(poblacion[i])
    if seleccion == 'aleatoria':
        for i in range(len(poblacion)):
            if randrange(2) == 0:
                padres.append(poblacion[i])

    return padres


"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
*   Se va a alternar los bits de ambos padres
*   Se va a tomar un bit del padre 1, un bit del padre 2 y así sucesivamente
"""


def cruzar(padre1, padre2):
    hijo = [padre1[0] if randrange(9) < 6 else padre2[0],
            padre1[1] if randrange(9) < 6 else padre2[1],
            padre1[2] if randrange(9) < 6 else padre2[2],
            padre1[3] if randrange(9) < 6 else padre2[3]
            ]
    return hijo  # Retorno al hijo ya cruzado


"""
*   Función que toma una solución y realiza la mutación
*   Se va a cambiar el bit con valor 0 más a la izquierda por 1
"""


def mutar(solucion):
    for i in range(len(solucion)):
        if randrange(2) == 1:
            # Cambio el valor por uno random de -2 a 2
            solucion[i] = uniform(-2, 2)
    return solucion  # Retorno la misma solución, solo que ahora mutó


"""
*   Función que toma a los mejores padres y genera nuevos hijos
"""


def emparejar(padres):
    global poblacionInicial  # Total de la población

    total_hijos_a_crear = poblacionInicial - len(padres)
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
    print('Individuo: ', individuo.solucion,
          ' Fitness: ', individuo.fitness)


def imprimirPoblacion(poblacion):
    for individuo in poblacion:
        imprimirIndividuo(individuo)


"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""


def ejecutar():
    generacion = 0
    poblacion = inicializarPoblacion()
    fin = verificarCriterio(poblacion, generacion, 'generacion')

    # Imprimo la población
    print('*************** GENERACION ', generacion, " ***************")
    imprimirPoblacion(poblacion)

    while(fin == None):
        padres = seleccionarPadres(poblacion, 'fitness')
        poblacion = emparejar(padres)
        generacion += 1
        fin = verificarCriterio(poblacion, generacion, 'generacion')

        # Imprimo la población
        print('*************** GENERACION ', generacion, " ***************")
        imprimirPoblacion(poblacion)

    # Obtengo la mejor solución y la muestro
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[
        :1]  # Los ordena de menor a mayor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR INDIVIDUO***************')
    imprimirIndividuo(mejorIndividuo)


# Corro el algoritmo
ejecutar()

#!/usr/bin/env python
import math
import numpy as np
from random import randrange, uniform, shuffle


class Nodo:
    def __init__(self, solucion=[], fitness=0):
        self.solucion = solucion
        self.fitness = fitness


poblacionInicial = 30  # Número de individuos a evaluar

# VARIABLES DE EVALUACION DEL FITNESS
# Número máximo de generaciones que va a tener el algoritmo
maximo_generaciones = 10
# Número N de filas y columnas
n = 3


def getArray():
    global n
    initial = []
    limite = n*n
    for i in range(limite+1):
        if i >= 0:
            initial.append(i)
    shuffle(initial)
    return initial


"""
*   Función que crea la población
"""


def inicializarPoblacion():
    global poblacionInicial
    poblacion = []

    for i in range(poblacionInicial):
        solucion = getArray()
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


def getRepetidos(solucionIndividuo):
    repetidos = 0
    unicos = []

    for i in range(len(solucionIndividuo)):
        if (solucionIndividuo[i] not in unicos):
            unicos.append(solucionIndividuo[i])

    return len(solucionIndividuo) - len(unicos)


def evaluarFitness(solucionIndividuo):
    global n
    fitness = 0

    # Suma común
    suma_comun = (n * (math.pow(n, n) + 1)) / 2

    # Repetidos
    repetidos = getRepetidos(solucionIndividuo)

    # suma diferencias
    suma_diferencias = abs(sumaFila(solucionIndividuo)-suma_comun) + \
        abs(sumaColumna(solucionIndividuo)-suma_comun) + \
        abs(sumaDiagonal(solucionIndividuo) - suma_comun)

    # fitness
    fitness = math.pow((1 + repetidos)*suma_diferencias+(repetidos), 2)

    return fitness


def sumaFila(solucionIndividuo):
    global n
    suma = 0

    for i in range(n):
        suma = suma + solucionIndividuo[i]

    return suma


def sumaColumna(solucionIndividuo):
    global n
    suma = 0

    for i in range(n):
        suma = suma + solucionIndividuo[i*n]

    return suma


def sumaDiagonal(solucionIndividuo):
    global n
    suma = 0

    for i in range(n):
        suma = suma + solucionIndividuo[i*n+i]

    return suma


"""
*   Función que toma a los mejores padres para luego crear una nueva generación
"""


def seleccionarPadres(poblacion):
    padres = []

    # Ordeno a los padres en orden ascendente, de menor a mayor
    poblacionOrdenada = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[
        : len(poblacion)]  # Los ordena de menor a mayor

    for i in range(round(len(poblacionOrdenada)/2)):
        padres.append(poblacionOrdenada[i])

    return padres


"""
*   Función que toma dos soluciones padres y las une para formar una nueva solución hijo
*   Se va a alternar los bits de ambos padres
*   Se va a tomar un bit del padre 1, un bit del padre 2 y así sucesivamente
"""


def cruzar(padre1, padre2):
    global n
    total_genes = n * n

    hijo = []
    for i in range(total_genes):
        hijo.append(padre1[i] if i % 2 == 0 else padre2[i])

    return hijo  # Retorno al hijo ya cruzado


"""
*   Función que toma una solución y realiza la mutación
"""


def mutar(solucion):
    for i in range(len(solucion)):
        if randrange(2) == 1 and i != len(solucion) - 1:
            # Cambio el valor por uno random de -2 a 2
            temp = solucion[i]
            solucion[i] = solucion[i + 1]
            solucion[i+1] = temp
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
    global n
    temp = 0
    print('==== Individuo ====')
    for i in range(len(individuo.solucion)):
        if (temp == n):
            print('')
            temp = 0
        print(str(individuo.solucion[i]) +
              (" | " if temp < n-1 else ""), end="")
        temp = temp + 1
    print('')
    print(' Fitness: ', individuo.fitness)


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
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[
        :1]  # Los ordena de menor a mayor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR INDIVIDUO***************')
    imprimirIndividuo(mejorIndividuo)


# Corro el algoritmo
ejecutar()

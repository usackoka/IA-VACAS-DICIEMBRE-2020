#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import math
import json
from random import randrange, uniform
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)


class Nodo:
    def __init__(self, solucion=[], fitness=0):
        self.solucion = solucion
        self.fitness = fitness


class NodoExcel:
    def __init__(self, proyecto1=0, proyecto2=0, proyecto3=0, proyecto4=0, notaReal=0):
        self.proyecto1 = float(proyecto1)
        self.proyecto2 = float(proyecto2)
        self.proyecto3 = float(proyecto3)
        self.proyecto4 = float(proyecto4)
        self.notaReal = float(notaReal)


# CONSTANTES DEL ALGORITMO
data = []  # Data cargada del excel
total_genes = 4  # Número de genes por individuo
poblacionInicial = 30  # Número de individuos a evaluar

# VARIABLES DE EVALUACION DEL FITNESS
# Número máximo de generaciones que va a tener el algoritmo
maximo_generaciones = 1000
fitness_mei = 0.40  # Número a cumplir menor o igual para fitness
promedioFitness = 0.40  # Número a comparar para el promedio de fitness en una solución

# VARIABLES DEL MODELO
criterioFinalizacion = 'generacion'
criterioPadres = 'fitness'
mejorIndividuo = Nodo()
nombreDoc = 'excel.csv'


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
    global fitness_mei
    global promedioFitness
    global maximo_generaciones

    if seleccion == 'generacion':
        # Si ya llegó al máximo de generaciones lo detengo
        if generacion >= maximo_generaciones:
            return True
    elif seleccion == 'fitness':
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


def calcularNota(proyecto1, proyecto2, proyecto3, proyecto4):
    proyecto1 = float(proyecto1)
    proyecto2 = float(proyecto2)
    proyecto3 = float(proyecto3)
    proyecto4 = float(proyecto4)

    global mejorIndividuo
    print('=============== CALCULANDO NOTA ===============')
    notaCalculada = mejorIndividuo.solucion[0] * proyecto1 + \
        mejorIndividuo.solucion[1] * proyecto2 + \
        mejorIndividuo.solucion[2] * proyecto3 + \
        mejorIndividuo.solucion[3] * proyecto4
    print('NOTA CALCULADA: ', notaCalculada)


"""
*   Método que ejecutará el algoritmo genético para obtener
*   los coeficientes del filtro
"""


def ejecutar():
    global criterioFinalizacion
    global criterioPadres
    global mejorIndividuo
    global nombreDoc

    generacion = 0
    poblacion = inicializarPoblacion()
    fin = verificarCriterio(poblacion, generacion, criterioFinalizacion)

    # Imprimo la población
    print('*************** GENERACION ', generacion, " ***************")
    imprimirPoblacion(poblacion)

    while(fin == None):
        padres = seleccionarPadres(poblacion, criterioPadres)
        poblacion = emparejar(padres)
        generacion += 1
        fin = verificarCriterio(poblacion, generacion, criterioFinalizacion)

        # Imprimo la población
        print('*************** GENERACION ', generacion, " ***************")
        imprimirPoblacion(poblacion)

    # Obtengo la mejor solución y la muestro
    arregloMejorIndividuo = sorted(poblacion, key=lambda item: item.fitness, reverse=False)[
        :1]  # Los ordena de menor a mayor
    mejorIndividuo = arregloMejorIndividuo[0]

    print('\n\n*************** MEJOR INDIVIDUO***************')
    imprimirIndividuo(mejorIndividuo)

    f = open('bitacora.txt', 'a')
    f.write("\n\n\n============== BITACORA ==============")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("\nFECHA Y HORA: "+str(dt_string))
    f.write("\nNOMBRE DEL DOCUMENTO: "+nombreDoc)
    f.write("\nCRITERIO DE FINALIZACION: "+criterioFinalizacion)
    f.write("\nCRITERIO DE SELECCION DE PADRES: "+criterioPadres)
    f.write("\nNUMERO DE GENERACIONES: "+str(generacion))
    f.write("\nMEJOR SOLUCION: "+str(mejorIndividuo.solucion))

    f.close()

    return jsonify(
        generaciones=generacion,
        mejorSolucion=mejorIndividuo.solucion
    )


@app.route('/')
def hello_world():
    return jsonify(
        response='Hellow world!',
    )


@app.route('/calcular-nota', methods=['POST'])
def calcular_nota():
    if request.method == 'POST':
        dataExcel = request.json
        calcularNota(dataExcel['proyecto1'], dataExcel['proyecto2'],
                     dataExcel['proyecto3'], dataExcel['proyecto4'])

    return jsonify(
        data='default response',
    )


@app.route('/generar-modelo', methods=['POST'])
def generar_modelo():
    if request.method == 'POST':
        global criterioFinalizacion
        global criterioPadres
        print('=========== SETEANDO CRITERIOS ===========')
        dataExcel = request.json
        criterioFinalizacion = dataExcel['finalizacion']
        criterioPadres = dataExcel['padres']
        print('=========== CRITERIOS SETEADOS CON ÉXITO ===========')
        print('=========== EJECUTANDO MODELO ======================')
        return ejecutar()

    return jsonify(
        data='default response',
    )


@app.route('/data-excel', methods=['GET', 'POST'])
def set_data():
    if request.method == 'POST':
        global data
        global nombreDoc
        print('=========== SETEANDO LA DATA DEL EXCEL ===========')
        data = []
        dataExcel = request.json
        nombreDoc = dataExcel['nombreDoc']
        for i in range(len(dataExcel['data'])):
            row = dataExcel['data'][i]
            try:
                data.append(NodoExcel(row['proyecto1'], row['proyecto2'],
                                      row['proyecto3'], row['proyecto4'],
                                      row['notaReal']))
            except Exception as e:
                print(row, 'iteración: ', i)
                raise

        print('=========== DATA SETEADA CON ÉXITO ===========')

    return jsonify(
        data='default response',
    )


if __name__ == '__main__':
    CORS(app)
    app.run()

# Corro el algoritmo
# ejecutar()

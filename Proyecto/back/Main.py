from Util.ReadFile import get_dataFile
from Util import Plotter
from Neural_Network.Data import Data
from Neural_Network.Model import NN_Model
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

train_X, train_Y, val_X, val_Y, minEdad, maxEdad, minAnio, maxAnio, minDistancia, maxDistancia = get_dataFile()
train_set = Data(train_X, train_Y)
val_set = Data(val_X, val_Y)

# Se define las dimensiones de las capas
# capas1 = [Cantidad de variables que tiene el problema, capa 1, capa 2, Capa de salida]
# se tendría una red neuronal de 3 capas, la capa de entrada NO se toma en cuenta
capas1 = [train_set.n, 10, 5, 4, 1]


def getModelo(alpha, iterations, lambd, keep_prob):
    # Se define el modelo
    nn1 = NN_Model(train_set, capas1, alpha=alpha,
                   iterations=iterations, lambd=lambd, keep_prob=keep_prob)
    # Se entrena el modelo
    nn1.training(False)
    print('Entrenamiento Modelo')
    nn1.predict(train_set)
    print("prueba modelo")
    fitness = nn1.predict(val_set)

    return nn1, fitness


modelo, x = getModelo(0.005, 10000, 0.2, 1.0)


def predecir(genero, edad, anio, distancia):
    edad = (edad - minEdad) / (maxEdad - minEdad)
    anio = (anio - minAnio) / (maxAnio - minAnio)
    distancia = (distancia - minDistancia) / (maxDistancia - minDistancia)
    arr = [[genero, edad, anio, distancia]]
    arr = np.array(arr).T

    # print(arr)
    dt = Data(arr, [[0]])

    print("--------------------------------")
    var = modelo.predict2(dt)

    print(var)
    return var


# predecir(1, 20, 2020, 0)

@app.route('/predecir', methods=['POST'])
def generar_modelo():
    if request.method == 'POST':
        dataExcel = request.json
        edad = dataExcel['edad']
        anio = dataExcel['anio']
        distancia = dataExcel['distancia']
        genero = dataExcel['genero']

        res = predecir(float(genero), float(edad),
                       float(anio), float(distancia))

        return jsonify(
            response=str("Se retira :c" if res == 0 else "Se mantiene c:"),
        )

    return jsonify(
        data='default response',
    )


if __name__ == '__main__':
    CORS(app)
    app.run()

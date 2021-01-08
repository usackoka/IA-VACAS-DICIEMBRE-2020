import csv
import numpy as np


def get_dataFile():
    with open('./datasets/DatasetNum.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    data.pop(0)  # quito la cabecera de los datos

    print(data[0])

    data = np.array(data).T

    data = np.float_(data)
    # Escalamiento variables
    arrEdad = (data[2])
    arrAnio = (data[3])
    arrDistancia = (data[4])

    minEdad = min(arrEdad)
    maxEdad = max(arrEdad)
    minAnio = min(arrAnio)
    maxAnio = max(arrAnio)
    minDistancia = min(arrDistancia)
    maxDistancia = max(arrDistancia)

    data[2] = [(x - minEdad) / (maxEdad - minEdad) for x in data[2]]  # Edad
    data[3] = [(x - minAnio) / (maxAnio - minAnio) for x in data[3]]  # Anio
    data[3] = [(x - minDistancia) / (maxDistancia - minDistancia)
               for x in data[4]]  # Distancia

    data = data.T
    train_X = data[0: int(len(data) * 0.7)]
    val_X = data[int(len(data) * 0.7): len(data)]

    train_X = list(np.array(train_X).T)
    val_X = list(np.array(val_X).T)

    # print(train_X)
    # exit()

    train_Y = [train_X.pop(0)]  # Estado
    val_Y = [val_X.pop(0)]

    train_X = np.array(train_X)
    val_X = np.array(val_X)

    train_Y = np.array(train_Y)
    val_Y = np.array(val_Y)

    print(len(data))
    print(len(train_X[0]))

    return train_X, train_Y, val_X, val_Y, minEdad, maxEdad, minAnio, maxAnio, minDistancia, maxDistancia

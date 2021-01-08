import math
import csv
import numpy as np


def haversine(lat1, lon1, lat2, lon2):
    rad = math.pi/180
    dlat = lat2-lat1
    dlon = lon2-lon1
    R = 6372.795477598
    a = (math.sin(rad*dlat/2))**2 + math.cos(rad*lat1) * \
        math.cos(rad*lat2)*(math.sin(rad*dlon/2))**2
    distancia = 2*R*math.asin(math.sqrt(a))
    return distancia


with open('./datasets/Dataset.csv', newline='') as f:
    reader = csv.reader(f)
    dataData = list(reader)

with open('./datasets/Municipios.csv', newline='') as f:
    reader = csv.reader(f)
    dataMuni = list(reader)

dataMuni[0].append("distancia")
for i in range(1, len(dataMuni)):
    distancia = haversine(14.589246, -90.551449,
                          float(dataMuni[i][3]), float(dataMuni[i][4]))
    dataMuni[i].append(distancia)

dataset = []
dataset.append(["Estado", "Genero", "edad", "Anio", "Distancia"])
for i in range(1, len(dataData)):
    estado = 1 if dataData[i][0] == "Activo" else 0
    genero = 1 if dataData[i][1] == "MASCULINO" else 0
    edad = dataData[i][2]
    anio = dataData[i][7]
    distancia = 0
    for j in range(0, len(dataMuni)):
        if(dataMuni[j][0] == dataData[i][3] and dataMuni[j][1] == dataData[i][5]):
            distancia = dataMuni[j][len(dataMuni[j]) - 1]
            break
    dataset.append([estado, genero, edad, anio, distancia])

myFile = open('./datasets/DataSetNum.csv', 'w', newline="")
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(dataset)

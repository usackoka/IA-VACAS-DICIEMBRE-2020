import os
import shutil
import numpy as np
from os import remove
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from FileManagement import File
from Logistic_Regression.Model import Model
from Logistic_Regression.Data import Data
from Logistic_Regression import Plotter


from PIL import Image

# Inicio de declaracion de arreglos
all_img = []


app = Flask(__name__)

contenido = os.listdir('./Datasets/USAC')
for imagen in contenido:
    image = Image.open('./Datasets/USAC' + "\\" + imagen)
    data = np.array(image)
    dato = [data, 1]
    all_img.append(dato)

contenido = os.listdir('./Datasets/Landivar')
for imagen in contenido:
    image = Image.open('./Datasets/Landivar' + "\\" + imagen)
    data = np.array(image)
    dato = [data, 2]
    all_img.append(dato)

contenido = os.listdir('./Datasets/Mariano')
for imagen in contenido:
    image = Image.open('./Datasets/Mariano' + "\\" + imagen)
    data = np.array(image)
    dato = [data, 3]
    all_img.append(dato)


contenido = os.listdir('./Datasets/Marroquin')
for imagen in contenido:
    image = Image.open('./Datasets/Marroquin' + "\\" + imagen)
    data = np.array(image)
    dato = [data, 4]
    all_img.append(dato)


np.random.shuffle(all_img)


def nuevo_modelo(alph, sset):
    model1 = Model(sset[0], sset[1], reg=False, alpha=alph, lam=150)
    model1.training()

    return model1


def addImagenesAComp(direccion_img):
    contenido = os.listdir('./upload/')

    menorA5 = len(contenido) <= 5

    arrResultado = []
    if(not menorA5):
        # Universidad, aciertos , fallos, %
        arrResultado = [["Usac", 0, 0, "--"], ["Landivar", 0, 0,
                                               "--"], ["Mariano", 0, 0, "--"], ["Marroquin", 0, 0, "--"]]
    for imagen in contenido:
        image = Image.open('./upload/' + imagen)
        data = np.array(image)
        direccion_img.append(imagen)

        nombreImg = imagen
        imagen = (imagen + "").lower().split("_")[0]

        c = np.array([data])
        data_x = c.reshape(-1, c.shape[0]).T
        toComp = np.append([1], data_x[0])

        if(menorA5):

            similitud = 0
            es = "--"
            resUsac = modUsac.predict2(toComp)
            resLandivar = modLandivar.predict2(toComp)
            resMariano = modMariano.predict2(toComp)
            resMarro = modMarro.predict2(toComp)

            if(resUsac > similitud):
                es = "USAC"
                similitud = resUsac
            if(resMariano > similitud):
                es = "MARIANO"
                similitud = resMariano
            if(resMarro > similitud):
                es = "Marro"
                similitud = resMarro
            if(resLandivar > similitud):
                es = "Landivar"
                similitud = resLandivar

            arrResultado.append([nombreImg, es, similitud])

        else:
            if(imagen == "usac"):
                if(modUsac.predict(toComp) == 1):
                    arrResultado[0][1] += 1
                else:
                    arrResultado[0][2] += 1
                arrResultado[0][3] = (
                    arrResultado[0][1] / (arrResultado[0][1] + arrResultado[0][2])) * 100
            elif(imagen == "landivar"):
                if(modLandivar.predict(toComp) == 1):
                    arrResultado[1][1] += 1
                else:
                    arrResultado[1][2] += 1
                arrResultado[1][3] = (
                    arrResultado[1][1] / (arrResultado[1][1] + arrResultado[1][2])) * 100
            elif(imagen == "mariano"):
                if(modMariano.predict(toComp) == 1):
                    arrResultado[2][1] += 1
                else:
                    arrResultado[2][2] += 1
                arrResultado[2][3] = (
                    arrResultado[2][1] / (arrResultado[2][1] + arrResultado[2][2])) * 100
            elif(imagen == "marroquin"):
                if(modMarro.predict(toComp) == 1):
                    arrResultado[3][1] += 1
                else:
                    arrResultado[3][2] += 1
                arrResultado[3][3] = (
                    arrResultado[3][1] / (arrResultado[3][1] + arrResultado[3][2])) * 100
            else:
                print("imagen desconocida")

    print(arrResultado)
    return str(arrResultado)


def obtener_set(comparar):
    train_img = []
    train_pertenece = [[]]

    test_img = []
    test_es = [[]]
    for i in range(0, int(len(all_img) * .8)):
        train_img.append(all_img[i][0])
        n = 0
        if(all_img[i][1] == comparar):
            n = 1
        train_pertenece[0].append(n)
    for i in range(int(len(all_img) * .8), len(all_img)):
        test_img.append(all_img[i][0])
        n = 0
        if(all_img[i][1] == comparar):
            n = 1
        test_es[0].append(n)

    train_img = np.array(train_img)
    test_img = np.array(test_img)

    train_pertenece = np.array(train_pertenece)
    test_es = np.array(test_es)

    train_arr = train_img.reshape(train_img.shape[0], -1).T
    test_arr = test_img.reshape(test_img.shape[0], -1).T

    train_set = Data(train_arr, train_pertenece, 255)
    test_set = Data(test_arr, test_es, 255)

    return [train_set, test_set]


@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        folder = './upload'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

        filename = ""

        files = request.files
        files = request.files.getlist("file[]")

        filename = ""
        for file in files:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            filename = secure_filename(file.filename)
            file.save(os.path.join('./upload/', filename))
        direcciones = []
        return addImagenesAComp(direcciones)
    return '''
    <!doctype html>
    <title>201503712</title>
    <h1>Practica 2 - Oscar Cuéllar - 201503712</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file[]" multiple>
      <input type="submit" value="Upload">
    </form>
    '''


@app.route('/img/<filename>')
def uploaded_file(filename):
    return send_from_directory('./upload', filename)
    # return app.config['UPLOAD_FOLDER'] + " " + filename


setUsac = obtener_set(1)
seLandivar = obtener_set(2)
setMariano = obtener_set(3)
setMarro = obtener_set(4)

if(False):
    print("modelo 1")
    modUsac1 = nuevo_modelo(0.001, setUsac)
    modUsac2 = nuevo_modelo(0.0001, setUsac)
    modUsac3 = nuevo_modelo(0.00001, setUsac)
    modUsac4 = nuevo_modelo(0.000001, setUsac)
    modUsac5 = nuevo_modelo(0.0000001, setUsac)

    Plotter.show_Model([modUsac1, modUsac2, modUsac3, modUsac4, modUsac5])
    exit()

if(False):
    modLandivar1 = nuevo_modelo(0.001,    seLandivar)
    modLandivar2 = nuevo_modelo(0.0001,   seLandivar)
    modLandivar3 = nuevo_modelo(0.00001,  seLandivar)
    modLandivar4 = nuevo_modelo(0.000001, seLandivar)
    modLandivar5 = nuevo_modelo(0.0000001, seLandivar)

    Plotter.show_Model([modLandivar1, modLandivar2,
                        modLandivar3, modLandivar4, modLandivar5])
    exit()

if(False):
    modMariano1 = nuevo_modelo(0.001,     setMariano)
    modMariano2 = nuevo_modelo(0.0001,    setMariano)
    modMariano3 = nuevo_modelo(0.00001,   setMariano)
    modMariano4 = nuevo_modelo(0.000001,  setMariano)
    modMariano5 = nuevo_modelo(0.0000001, setMariano)

    # MOD AQUI

    Plotter.show_Model(
        [modMariano1, modMariano2, modMariano3, modMariano4, modMariano5])
    exit()

if(False):
    modMarro1 = nuevo_modelo(0.001,     setMarro)
    modMarro2 = nuevo_modelo(0.0001,    setMarro)
    modMarro3 = nuevo_modelo(0.00001,   setMarro)
    modMarro4 = nuevo_modelo(0.000001,  setMarro)
    modMarro5 = nuevo_modelo(0.0000001, setMarro)

    Plotter.show_Model([modMarro1, modMarro2, modMarro3, modMarro4, modMarro5])
    exit()

modUsac = nuevo_modelo(0.0001, setUsac)
modLandivar = nuevo_modelo(0.0001, seLandivar)
modMariano = nuevo_modelo(0.001, setMariano)
modMarro = nuevo_modelo(0.0001, setMarro)

#Plotter.show_Model([modUsac, modLandivar, modMariano, modMarro])

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True, port=5000)

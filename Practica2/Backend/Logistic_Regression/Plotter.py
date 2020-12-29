from Logistic_Regression.Model import Model
import matplotlib.pyplot as chart


def show_picture(pixels):
    chart.imshow(pixels)
    chart.show()


def show_Model(models):
    for model in models:
        chart.plot(model.bitacora, label=str(model.alpha))
    chart.ylabel('Costo')
    chart.xlabel('Iteraciones')
    legend = chart.legend(loc='upper center', shadow=True)
    chart.show()

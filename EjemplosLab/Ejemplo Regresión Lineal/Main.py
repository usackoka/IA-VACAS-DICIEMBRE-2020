from FileManagement import File
from Linear_Regression.Model import Model
import matplotlib.pyplot as chart

data = File.read_file("Test.csv")
model = Model(data)
model.training()

chart.plot(model.bitacora)
chart.show()


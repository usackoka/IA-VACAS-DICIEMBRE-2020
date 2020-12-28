import csv
import numpy as np


def read_file(path):
    data = []
    with open(path) as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    result = np.array(data)
    np.random.shuffle(result)

    #print(result)
    return result.astype(float)

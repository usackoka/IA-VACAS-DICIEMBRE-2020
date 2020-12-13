from random import randrange


class Nodo:
    def __init__(self, solucion=[], izquierda=None, derecha=None):
        self.solucion = solucion
        self.izquierda = izquierda
        self.derecha = derecha


matrizSolucion = [['A', 'B'], ['C', '#']]
puzzles = ['A', 'B', 'C', '#']


def dibujaMatriz(M):
    for i in range(len(M)):
        print('[', end='', sep=''),
        for j in range(len(M[i])):
            print('{:>3s}'.format(str(M[i][j])), end=''),
        print(']')


def generarEstadoInicial():
    global puzzles
    matrizInicial = []
    ingresados = []

    # primera fila
    azar1 = randrange(len(puzzles))
    while azar1 in ingresados:
        azar1 = randrange(len(puzzles))
    ingresados.append(azar1)

    azar2 = randrange(len(puzzles))
    while azar2 in ingresados:
        azar2 = randrange(len(puzzles))
    ingresados.append(azar2)

    matrizInicial.append([puzzles[azar1], puzzles[azar2]])

    # segunda fila
    azar1 = randrange(len(puzzles))
    while azar1 in ingresados:
        azar1 = randrange(len(puzzles))
    ingresados.append(azar1)

    azar2 = randrange(len(puzzles))
    while azar2 in ingresados:
        azar2 = randrange(len(puzzles))
    ingresados.append(azar2)

    matrizInicial.append([puzzles[azar1], puzzles[azar2]])

    return matrizInicial


def moverFila(matriz):
    for i in range(len(matriz)):
        t1 = matriz[i][0]
        t2 = matriz[i][1]
        if t1 == '#' or t2 == '#':
            temp = matriz[i][0]
            matriz[i][0] = matriz[i][1]
            matriz[i][1] = temp
    return matriz

def moverColumna(matriz):
    for i in range(len(matriz)):
        t1 = matriz[i][0]
        t2 = matriz[i][1]
        if t1 == '#' or t2 == '#':
            temp = matriz[i][0]
            matriz[i][0] = matriz[i][1]
            matriz[i][1] = temp
    return matriz


def profundidad():
    global matrizSolucion
    print('=============== METODO PROFUNDIDAD =================')
    matrizInicial = generarEstadoInicial()
    print('ESTADO INICIAL: ')
    dibujaMatriz(matrizInicial)


def amplitud():
    print('=============== METODO AMPLITUD =================')
    matrizInicial = generarEstadoInicial()
    print('ESTADO INICIAL: ')
    dibujaMatriz(matrizInicial)
    izquierda = moverFila(matrizInicial)
    print('ESTADO MOVIDO: ')
    dibujaMatriz(izquierda)


def main():
    print('======== OSCAR RENE CUELLAR MANCILLA ========')
    print('*********************************************')
    print('*    1. Búsqueda en profundidad             *')
    print('*    2. Búsqueda en amplitud                *')
    print('*********************************************')
    try:
        opcion = int(input("\nSeleccione una opción: "))
        if opcion == 1:
            profundidad()
        elif opcion == 2:
            amplitud()
        else:
            main()
    except ValueError:
        main()


main()

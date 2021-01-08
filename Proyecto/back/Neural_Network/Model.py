import numpy as np
#np.set_printoptions(threshold=100000) #Esto es para que al imprimir un arreglo no me muestre puntos suspensivos


class NN_Model:

    def __init__(self, train_set, layers, alpha=0.3, iterations=300000, lambd=0, keep_prob=1):
        self.data = train_set
        self.alpha = alpha
        self.max_iteration = iterations
        self.lambd = lambd
        self.kp = keep_prob
        # Se inicializan los pesos
        self.parametros = self.Inicializar(layers)

    def Inicializar(self, layers):
        parametros = {}
        L = len(layers)
        print('layers:', layers)
        for l in range(1, L):
            #np.random.randn(layers[l], layers[l-1])
            #Crea un arreglo que tiene layers[l] arreglos, donde cada uno de estos arreglos tiene layers[l-1] elementos con valores aleatorios
            #np.sqrt(layers[l-1] se saca la raiz cuadrada positiva de la capa anterior ---> layers[l-1]
            parametros['W'+str(l)] = np.random.randn(layers[l], layers[l-1]) / np.sqrt(layers[l-1])
            parametros['b'+str(l)] = np.zeros((layers[l], 1))
            #print(layers[l], layers[l-1], np.random.randn(layers[l], layers[l-1]))
            #print(np.sqrt(layers[l-1]))
            #print(np.random.randn(layers[l], layers[l-1]) / np.sqrt(layers[l-1]))

        return parametros

    def training(self, show_cost=False):
        self.bitacora = []
        for i in range(0, self.max_iteration):
            y_hat, temp = self.propagacion_adelante(self.data)
            cost = self.cost_function(y_hat)
            gradientes = self.propagacion_atras(temp)
            self.actualizar_parametros(gradientes)
            if i % 50 == 0:
                self.bitacora.append(cost)
                if show_cost:
                    print('Iteracion No.', i, 'Costo:', cost, sep=' ')



    def propagacion_adelante(self, dataSet):
        X = dataSet.x
        temporal = []
        L = len(self.parametros) // 2
        for i in range(0, L):
            if( i == L -1): 
                WFIN = self.parametros[ "W" + str(L) ]
                bFin = self.parametros[ "b" + str(L) ]

                ZFin = np.dot(WFIN, X) + bFin
                AFin = self.activation_function('sigmoide', ZFin)

                temporal.append(ZFin)
                temporal.append(AFin)
                temporal = tuple(temporal)

                return AFin, temporal
            W = self.parametros["W" + str(i + 1)]
            b = self.parametros["b" + str(i + 1)]
            Z = np.dot(W, X) + b
            A = self.activation_function('relu', Z)
            D = np.random.rand(A.shape[0], A.shape[1]) #Se generan número aleatorios para cada neurona
            D = (D < self.kp).astype(int) #Mientras más alto es kp mayor la probabilidad de que la neurona permanezca
            A *= D
            A /= self.kp
            temporal.append(Z)
            temporal.append(A)
            temporal.append(D)
            X = A
       
        return None


    def propagacion_atras(self, temporal):
        # Se obtienen los datos
        m = self.data.m
        Y = self.data.y
        X = self.data.x

        arrAux = {}
        cont = 1
        AAnt = None
        dZ = None
        i = 0
        ZFin = None
        AFin = None
        while(True):
            AAnt = AFin
            ZFin = temporal[i]   
            AFin = temporal[i + 1]   

            arrAux["Z" + str(cont)] = ZFin
            i += 1
            arrAux["A" + str(cont)] = AFin
            i += 1

            if(i == len(temporal)):
                break

            arrAux["D" + str(cont)] = temporal[i]
            i += 1
            cont += 1
  
        W = self.parametros["W" + str(cont)]
        # Derivadas parciales de la ultima capa
        dZ = AFin - Y

        gradientes = {}

        i = cont

        dW = (1 / m) * np.dot(dZ, AAnt.T) + (self.lambd / m) * W
        db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)
        gradientes["dZ" + str(i)] = dZ
        gradientes["dW" + str(i)] = dW
        gradientes["db" + str(i)] = db
        iAux = 0
        while(True):
            if(iAux == cont - 1):
                return gradientes
            i -= 1
            W = self.parametros["W" + str(i + 1)]
            dA = np.dot(W.T, dZ)   
            D = arrAux["D" + str(i)]
            A = arrAux["A" + str(i)]
            W = self.parametros["W" + str(i)]
            dA *= D
            dA /= self.kp
            dZ = np.multiply(dA, np.int64(A > 0))
            AAnt = X
            if(i != 1): 
                AAnt = arrAux["A" + str(i - 1)]
            W = self.parametros["W" + str(i)]
            dW = (1 / m) * np.dot(dZ, AAnt.T) + (self.lambd / m) * W
            db = (1 / m) * np.sum(dZ, axis=1, keepdims=True)

            gradientes["dZ" + str(i)] = dZ
            gradientes["dW" + str(i)] = dW
            gradientes["db" + str(i)] = db
            gradientes["dA" + str(i)] = dA
            iAux += 1

        return None
    
    
    def actualizar_parametros(self, grad):
        # Se obtiene la cantidad de pesos
        L = len(self.parametros) // 2
        for k in range(L):
            self.parametros["W" + str(k + 1)] -= self.alpha * grad["dW" + str(k + 1)]
            self.parametros["b" + str(k + 1)] -= self.alpha * grad["db" + str(k + 1)]

    def cost_function(self, y_hat):
        # Se obtienen los datos
        Y = self.data.y
        m = self.data.m
        # Se hacen los calculos
        temp = np.multiply(-np.log(y_hat), Y) + np.multiply(-np.log(1 - y_hat), 1 - Y)
        result = (1 / m) * np.nansum(temp)
        # Se agrega la regularizacion L2
        if self.lambd > 0:
            L = len(self.parametros) // 2
            suma = 0
            for i in range(L):
                suma += np.sum(np.square(self.parametros["W" + str(i + 1)]))
            result += (self.lambd/(2*m)) * suma
        return result

    def predict(self, dataSet):
        # Se obtienen los datos
        m = dataSet.m
        Y = dataSet.y
        p = np.zeros((1, m), dtype= np.int)
        # Propagacion hacia adelante
        y_hat, temp = self.propagacion_adelante(dataSet)
        # Convertir probabilidad
        for i in range(0, m):
            p[0, i] = 1 if y_hat[0, i] > 0.5 else 0
        exactitud = np.mean((p[0, :] == Y[0, ]))
        print("Exactitud: " + str(exactitud))
        return exactitud


    def predict(self, dataSet):
        # Se obtienen los datos
        m = dataSet.m
        Y = dataSet.y
        p = np.zeros((1, m), dtype= np.int)
        # Propagacion hacia adelante
        y_hat, temp = self.propagacion_adelante(dataSet)
        # Convertir probabilidad
        for i in range(0, m):
            p[0, i] = 1 if y_hat[0, i] > 0.5 else 0
        exactitud = np.mean((p[0, :] == Y[0, ]))
        print("Exactitud: " + str(exactitud))
        return exactitud

    def predict2(self, dataSet):
        # Se obtienen los datos
        m = dataSet.m
        Y = dataSet.y
        p = np.zeros((1, m), dtype= np.int)
        # Propagacion hacia adelante
        y_hat, temp = self.propagacion_adelante(dataSet)
        # Convertir probabilidad
        for i in range(0, m):
            p[0, i] = 1 if y_hat[0, i] > 0.5 else 0
        return p[0][0]



    def activation_function(self, name, x):
        result = 0
        if name == 'sigmoide':
            result = 1/(1 + np.exp(-x))
        elif name == 'tanh':
            result = np.tanh(x)
        elif name == 'relu':
            result = np.maximum(0, x)
        
        #print('name:', name, 'result:', result)
        return result
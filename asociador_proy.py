def asoc(pruebas, clases,nombre):
    resultados=[]
    import numpy as n

    archivo = open("instancia_claseExplicacion_test.txt")
    contenido = archivo.readlines()

    X = contenido[3:3+int(contenido[1])]
    X = [i.split("\t") for i in X]
    X = [list(map(int, i)) for i in X]

    Y = contenido[3+int(contenido[1]):]
    Y = [i.split("\t") for i in Y]
    Y = [list(map(int, i)) for i in Y]

    X = n.array(X)
    Y = n.array(Y)

    Paso1 = X.dot(X.T)
    Paso2 = n.linalg.inv(Paso1)
    Xpseudo = X.T.dot(Paso2)

    W = Y.dot(Xpseudo)

    print("X:")
    print(X)

    print("Y:")
    print(Y)

    print("W:")
    print(W)

    #################################################################################################
    #################################################################################################
    ### EVALUACION DE LOS CASOS DE PRUEBA
    #################################################################################################
    #################################################################################################

    auxpruebas =[]
    for i in range(len(pruebas)):
        del pruebas[i][0][4]
        auxpruebas.append(pruebas[i][0])
    print(auxpruebas)
    auxpruebas = n.array(auxpruebas)
    print(auxpruebas)
    auxpruebas=auxpruebas.T
    print(auxpruebas)

    print("Prueba...")


    casosCorrectos = 0

    X=auxpruebas
    #CLASE SALIDA1  SALIDA 2  SALIDA 3
    Clases = clases

    for i in range(X.shape[1]): #para cada uno de los casos/registros de prueba
        print("Prueba del Caso ", i + 1)
        casoi = X[:,i]
        print("Caso Analizado: ")
        print(casoi)

        Ycasoi = W.dot(casoi)
        print("Salidas Generadas: ")
        print(Ycasoi)

        IndexMaxYcasoi = list(Ycasoi).index(max(Ycasoi))

        print("Clase Asignada: ", Clases[IndexMaxYcasoi])
        resultados.append(Clases[IndexMaxYcasoi])

    return resultados
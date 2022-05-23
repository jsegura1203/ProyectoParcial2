def metodo(pruebas,nombre):
    def Euclidiana(A, B):
        distancia = 0
        if(len(A)<=len(B)):
            tam=len(A)
        else:
            tam=len(B)
        for i in range(tam):
            distancia += (A[i]-B[i])**2
        distancia = distancia ** (1/2)
        distancia = round(distancia, 2)
        return distancia

    archivo = open(nombre,"r")
    contenido = archivo.readlines()

    lista = [linea.split(",") for linea in contenido]

    instancia = [ [ list(map(float,x[:len(x)-1])), x[len(x)-1].strip("\n") ] for x in lista ]

    prueba=[]
    prueba = pruebas

    ##############################################################################
    ###DEFINIR EL VALOR DE "K"  - Un número entre 1 y el total de registros de la instancia (entrenamiento)
    K = 5
    ##############################################################################

    contAciertos = 0 #contador de aciertos obtenidos en la clasificación
    respKnn=[]
    for registroNC in prueba: #para recorrer a todos los registros de prueba y aplicar al algoritmo K-NN
        #print("Clasificación del registro: ")
        #print(registroNC) #registor de prueba procesado para su clasificacion

        NC = registroNC #vector de caracteristicas del registro actual de prueba

        estructuraDatos = {} #inicializacion de la estructura de datos

        for NoCaso, i in enumerate(instancia):
            distancia_NC_i = Euclidiana(NC[0], i[0])
            #print(distancia_NC_i)
            estructuraDatos[NoCaso] = distancia_NC_i

        #print(estructuraDatos)  # La distancia de los registros con el registroNC

        ordenado = sorted(estructuraDatos.items(), key=lambda x: x[1]) #ordena los registros
        #de menor a mayor de acuerdo con la distancia con el registroNC
        #print(ordenado)

        temporalK = []
        for i in range(K):
            NoCaso = ordenado[i][0]
            #print(etiqueta)
            registro = instancia[NoCaso]
            #print(registro)
            temporalK.append(registro[1]) #obtencion de la etiqueta

        #print("Clases de los vectores más cercanos al registro NC:")
        #print(temporalK)  #los primeros K vectores

        from statistics import multimode  #<<<- realizado unicamente para fines academicos, no se recomienda poner la importacion aqui
        moda = multimode(temporalK)
        respKnn.append(moda[0])  # si existe más de una moda se queda con la primera de ellas

        #print("Clase asignada por el KNN: "  + str(respKnn))
        #print("\n")
    return respKnn



import serial as connector #para conectar con Arduino

import sys
import time
import threading
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal

import KNN
import asociador_proy as asoc
import discretizador_proy as discretizador
import naive_proy as naive

from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QRadioButton

qtCreatorFile = "proyecto.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btn_conectar.clicked.connect(self.conectar)
        self.btn_iniciar.clicked.connect(self.iniciar)
        self.btn_resultados.clicked.connect(self.resultados)
        self.arduino = None #null en java
        self.nombre="iris_completa"
        self.cargar()
        self.fila=0
        self.datos=[]
        self.respuestas=[]
        self.copialista=[]

        #instancia a trabajar

    # Área de los Slots
    def cargar(self):
        discretizador.discretiza(self.nombre)
        archivo = open("arreglo.txt")
        contenido = archivo.readlines()
        self.clase = []
        for i in contenido:
            self.clase.append(i.strip("\n"))
        fila=0
        for clase in self.clase:
            self.clases.insertRow(fila)
            celda=QTableWidgetItem(clase)
            self.clases.setItem(fila,0,celda)
            fila+=1

    def resultados(self):
        if(self.radio_knn.isChecked()):
            valor=[]
            valor=KNN.metodo(self.datos, self.nombre+"_generado.csv")
            self.respuestas=valor
            print(self.respuestas)
            for i in range (len(self.respuestas)):
                for j in range(len(self.clase)):
                    if(self.respuestas[i]==self.clase[j]):
                        self.arduino.write(j.__str__().encode())
                        print(j)
                        time.sleep(3)
        else:
            if(self.radio_asociador.isChecked()):
                valor=[]
                valor = asoc.asoc(self.datos,self.clase, self.nombre+"_generado.csv")
                self.respuestas = valor
                print(self.respuestas)
                for i in range(len(self.respuestas)):
                    for j in range(len(self.clase)):
                        if (self.respuestas[i] == self.clase[j]):
                            self.arduino.write(j.__str__().encode())
                            print(j)
                            time.sleep(3)
            else:
                if(self.radio_naive.isChecked()):
                    valor = []
                    valor = naive.naive(self.datos, self.nombre + "_generado.csv",self.clase)
                    self.respuestas = valor
                    print(self.respuestas)
                    for i in range(len(self.respuestas)):
                        for j in range(len(self.clase)):
                            if (self.respuestas[i] == self.clase[j]):
                                self.arduino.write(j.__str__().encode())
                                print(j)
                                time.sleep(3)

    def conectar(self):
        try:
            if self.arduino == None:
                com = "COM"+ self.txt_com.text()
                self.arduino =  connector.Serial(com, baudrate=9600, timeout=1)
                print("Conexión Inicializada")
                self.btn_conectar.setText("DESCONECTAR")
                self.txt_com.setEnabled(False)
            elif self.arduino.isOpen():
                self.btn_conectar.setText("RECONECTAR")
                self.arduino.close()
                print("Conexion Cerrada")
            else:
                self.btn_conectar.setText("DESCONECTAR")
                self.arduino.open()
                print("Conexion Reconectada")
        except Exception as e:
            print(str(e))

    def iniciar(self):
        flag=True
        if self.arduino != None:
            if self.arduino.isOpen():  ##otra opción: checar que el texto del boton sea desconectar
                try:
                    while(flag):
                        self.lista=self.leer()
                        if(self.lista!=None):
                            print(self.lista)
                            if(len(self.lista)==7):
                                if(self.lista[5]=="1" or self.lista[6]=="1"):
                                    flag=False
                    if(flag==False):
                        self.label_atributo1.setText(self.lista[0]+"")
                        self.label_atributo2.setText(self.lista[1]+"")
                        self.label_atributo3.setText(self.lista[2]+"")
                        self.label_atributo4.setText(self.lista[3]+"")
                        self.label_atributo5.setText(self.lista[4]+"")
                        if(self.lista[6]=="1"):
                            self.copialista = [list(map(int, self.lista[:5])), 0]
                            print(self.copialista[0])
                            self.datos.append(self.copialista)
                            print("datos")
                            print(self.datos)
                            columna=0
                            self.tabla.insertRow(self.fila)
                            for valor in self.copialista[0]:
                                celda = QTableWidgetItem(valor.__str__())
                                self.tabla.setItem(self.fila, columna, celda)
                                columna += 1
                            self.fila+1

                except Exception as e:
                    print(str(e))
            else:
                print("La conexión esta cerrada actualmente")
        else:
            print("Aun no se ha realizado la conexion con Arduino")

    def leer(self):
        cadena = self.arduino.readline().decode().strip("\r\n")
        if(cadena!=""):
            if(cadena[0]=="I" and cadena[len(cadena)-1]=="T"):
                cadena=cadena[1:len(cadena)-1]
                lista=cadena.split(";")
                return lista


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
2

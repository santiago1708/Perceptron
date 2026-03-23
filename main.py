from objeto import objeto
import random
from perceptronLogica import Perceptron
import utilidades as funciones



#Datos de entrenamiento-------------------------------------------------
objetosEntrenamiento = []
funciones.crear_objetos(100, True, objetosEntrenamiento, True)


#Comprobacion de la existencia de datos---------------------------------
print("Datos de entrenamiento--------------------------------")
for i, obj in enumerate(objetosEntrenamiento):
    print(f"{i + 1}. {obj.informacion()}")


#Creacion del perceptron-----------------------------------------------
neurona = Perceptron(0.1, 100)


#Entrenamiento---------------------------------------------------------
neurona.entrenamiento_perceptron(objetosEntrenamiento)


#Creacion de nuevos objetos y puesta prueba del perceptron-------------
objetos = []

#Pruebas---------------------------------------------------------------
#funciones.crear_multiples_objetos(neurona, objetos)
#funciones.crear_un_objeto(neurona, objetos)













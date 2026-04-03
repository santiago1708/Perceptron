from objeto import objeto
import random
import numpy as np

#Funcion para crear objetos--------------------------------------------------------------
def crear_objetos(cantidadObjetos, entrenamiento, lista_objetos, pos_automaticas):
    limite_1 = -10
    limite_2 = 10
  
    if cantidadObjetos > 0:
        for i in range(cantidadObjetos):
            if pos_automaticas == True:
                x = random.uniform(limite_1, limite_2)
                y = random.uniform(limite_1, limite_2)
                z = random.uniform(limite_1, limite_2)
            else:
                try:
                    x = float(input("X: "))
                    y = float(input("Y: "))
                    z = float(input("z: "))

                    if limite_de_rangos(limite_1, limite_2, x, y, z): 
                        return

                except ValueError:
                    print("El ingreso de un dato fue incorrecto")
                    return
                
            if entrenamiento == True:
                sumatoria = x + y + z
                
                # NUEVA LÓGICA DE 3 CLASES
                if sumatoria > 5:
                    obj = objeto(x, y, z, 0, (255, 0, 0))      # Rojo
                elif sumatoria < -5:
                    obj = objeto(x, y, z, 2, (0, 0, 255))      # Azul
                else:
                    obj = objeto(x, y, z, 1, (0, 255, 0))      # Verde
            else:    
                obj = objeto(x, y, z, None, (0, 0, 0))
            
            lista_objetos.append(obj)
    else:
        print("No fue posible realizar esta accion por que el valor ingresado es menor a 1")


#Funcion para crear cantidad n de objetos--------------------------------------------------------------
def crear_multiples_objetos(perceptron, arreglo):
    
    try:
        cantidad_objetos = int(input("Ingrese la cantidad de objetos: "))
    except ValueError:
        print("Debes ingresar un número entero")
        cantidad_objetos = 0
    
    crear_objetos(cantidad_objetos, False, arreglo, True)
    
    print("Datos no entrenados----------------------------")
    for i, obj in enumerate(arreglo):
        print(f"{i + 1}. {obj.informacion()}")
        clase = perceptron.calcular_desicion(obj)
        obj.clase = clase
        if clase == 0:
            obj.color = (255, 0, 0)
        else:
            obj.color = (0, 0, 255)
        print(f"{i + 1}. {obj.informacion()}")
        
#Funcion para crear un solo objeto--------------------------------------------------------------
def crear_un_objeto(perceptron, arreglo):
    print("1 Objeto**************")
    crear_objetos(1, False, arreglo, False)
    print("Datos no entrenados----------------------------")
    for i, obj in enumerate(arreglo):
        print(f"{i + 1}. {obj.informacion()}")
        clase = perceptron.calcular_desicion(obj)
        obj.clase = clase
        if clase == 0:
            obj.color = (255, 0, 0)
        else:
            obj.color = (0, 0, 255)
        print(f"{i + 1}. {obj.informacion()}")
#"Excepcion"
def limite_de_rangos(rango_1, rango_2, posX, posY, posZ):
    if posX < rango_1 or posX > rango_2:
        print(F"El valor de X debe estar entre {rango_1} y {rango_2}")
        return True
    elif posY < rango_1 or posY > rango_2:
        print(F"El valor de Y debe estar entre {rango_1} y {rango_2}")
        return True
    elif posZ < rango_1 or posZ > rango_2:
        print(F"El valor de Z debe estar entre {rango_1} y {rango_2}")
        return True
    else:
        return False
    

def generar_nube(cantidad, media, desviacion, distribucion):
    lista_objetos = []
    
    for i in range(cantidad):
        if distribucion == "normal":
            x = np.random.normal(media, desviacion)
            y = np.random.normal(media, desviacion)
            z = np.random.normal(media, desviacion)
        elif distribucion == "uniforme":
            x = np.random.uniform(media - desviacion, media + desviacion)
            y = np.random.uniform(media - desviacion, media + desviacion)
            z = np.random.uniform(media - desviacion, media + desviacion)
        elif distribucion == "exponencial":
            x = np.random.exponential(desviacion) + media
            y = np.random.exponential(desviacion) + media
            z = np.random.exponential(desviacion) + media

        sumatoria = x + y + z
        
        if sumatoria > 5:
            color = (255, 0, 0)      # Rojo
            clase = 0
        elif sumatoria < -5:
            color = (0, 0, 255)      # Azul
            clase = 2
        else:
            color = (0, 255, 0)      # Verde
            clase = 1
    
        obj = objeto(x, y, z, clase, color)
        lista_objetos.append(obj)

    return lista_objetos
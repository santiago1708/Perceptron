import random
from objeto import objeto 

class Perceptron:

    def __init__(self, tasa_aprendizaje, epocas):
        self.peso_1 = random.uniform(-10, 10)
        self.peso_2 = random.uniform(-10, 10)
        self.peso_3 = random.uniform(-10, 10)
        self.sesgo = 1
        self.tasa_aprendizaje = tasa_aprendizaje
        self.maximo_epocas = epocas
        self.epocas_recorridas = 0
        self.historial_errores = []
        self.historial_pesos = []
    
    def calcular_desicion(self, objeto):
        resultado = (self.peso_1 * objeto.posX) + (self.peso_2 * objeto.posY) + (self.peso_3 * objeto.posZ) + self.sesgo
        print(f"Funcion desicion: resultado: {resultado}, recorriendo epoca: {self.epocas_recorridas}")
        if resultado >= 0:
            return 1
        else:
            return 0
    

    def entrenamiento_perceptron(self, objetosEntrenamiento):

        salida = False

        while salida != True:

            self.epocas_recorridas += 1

            error_total = 0
            for i, obj in enumerate(objetosEntrenamiento):
                print(f"  Objeto {i+1} | Pesos: ({round(self.peso_1,3)}, {round(self.peso_2,3)}, {round(self.peso_3,3)}) | Sesgo: {round(self.sesgo,3)}")
                neurona = self.calcular_desicion(obj)
                error = obj.clase - neurona

                self.peso_1 += self.tasa_aprendizaje * error * obj.posX
                self.peso_2 += self.tasa_aprendizaje * error * obj.posY
                self.peso_3 += self.tasa_aprendizaje * error * obj.posZ
                self.sesgo += self.tasa_aprendizaje * error

                error_total += abs(error)

                print(f"  Objeto {i+1} | Real: {obj.clase} | Predicho: {neurona} | Error: {error} | Pesos: ({round(self.peso_1,3)}, {round(self.peso_2,3)}, {round(self.peso_3,2)}) | Sesgo: {round(self.sesgo,3)}")
            

            self.historial_errores.append(error_total)
            self.historial_pesos.append([self.peso_1, self.peso_2, self.peso_3, self.sesgo])

            print(f"\nEpocas finalizadas {self.epocas_recorridas} | Error total: {error_total}")

            print(f"Errores: {self.historial_errores}")
            print(f"pesos y sesgo: {self.historial_pesos}")
            
            

            if error_total == 0:
                print(f"El error fue 0 en la epoca {self.epocas_recorridas}")
                salida = True
            elif self.epocas_recorridas == self.maximo_epocas:
                print(f"Se alcanzó el máximo de {self.maximo_epocas} epocas")
                salida = True

#Reinicio del perceptron--------------------------------------
    def reiniciar_perceptron(self):
        self.peso_1 = random.uniform(-10, 10)
        self.peso_2 = random.uniform(-10, 10)
        self.peso_3 = random.uniform(-10, 10)
        self.sesgo = 1
        self.epocas_recorridas = 0
        self.historial_errores = []
        self.historial_pesos = []


    
        
        
        

    
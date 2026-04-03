import random
from objeto import objeto

class Perceptron:

    def __init__(self, tasa_aprendizaje, epocas):
        self.peso_1 = random.uniform(-10, 10)
        self.peso_2 = random.uniform(-10, 10)
        self.peso_3 = random.uniform(-10, 10)
        self.sesgo = 1
        
        self.peso_1_plano2 = random.uniform(-10, 10)
        self.peso_2_plano2 = random.uniform(-10, 10)
        self.peso_3_plano2 = random.uniform(-10, 10)
        self.sesgo_plano2 = 1
        
        self.tasa_aprendizaje = tasa_aprendizaje
        self.maximo_epocas = epocas
        self.epocas_recorridas = 0
        self.historial_errores = []
        self.historial_errores_plano1 = []
        self.historial_errores_plano2 = []
        self.historial_pesos = []
    
    def calcular_desicion_plano1(self, objeto):
        resultado = (self.peso_1 * objeto.posX) + (self.peso_2 * objeto.posY) + \
                    (self.peso_3 * objeto.posZ) + self.sesgo
        if resultado >= 0:
            return 1
        else:
            return 0
    
    def calcular_desicion_plano2(self, objeto):
        resultado = (self.peso_1_plano2 * objeto.posX) + (self.peso_2_plano2 * objeto.posY) + \
                    (self.peso_3_plano2 * objeto.posZ) + self.sesgo_plano2
        if resultado >= 0:
            return 1
        else:
            return 0
    
    def predecir_clase(self, objeto):
        salida_plano1 = self.calcular_desicion_plano1(objeto)
        salida_plano2 = self.calcular_desicion_plano2(objeto)
        
        if salida_plano1 == 1:
            return 0
        elif salida_plano2 == 1:
            return 2
        else:
            return 1

    def entrenamiento_perceptron(self, objetosEntrenamiento):
        salida = False

        while salida != True:

            self.epocas_recorridas += 1

            error_total_plano1 = 0
            error_total_plano2 = 0
            
            # ===== ENTRENAMIENTO PLANO 1 =====
            for i, obj in enumerate(objetosEntrenamiento):
                clase_real_p1 = 1 if obj.clase == 0 else 0
                prediccion_p1 = self.calcular_desicion_plano1(obj)
                error_p1 = clase_real_p1 - prediccion_p1

                self.peso_1 += self.tasa_aprendizaje * error_p1 * obj.posX
                self.peso_2 += self.tasa_aprendizaje * error_p1 * obj.posY
                self.peso_3 += self.tasa_aprendizaje * error_p1 * obj.posZ
                self.sesgo += self.tasa_aprendizaje * error_p1

                error_total_plano1 += abs(error_p1)

            # ===== ENTRENAMIENTO PLANO 2 =====
            for i, obj in enumerate(objetosEntrenamiento):
                clase_real_p2 = 1 if obj.clase == 2 else 0
                prediccion_p2 = self.calcular_desicion_plano2(obj)
                error_p2 = clase_real_p2 - prediccion_p2

                self.peso_1_plano2 += self.tasa_aprendizaje * error_p2 * obj.posX
                self.peso_2_plano2 += self.tasa_aprendizaje * error_p2 * obj.posY
                self.peso_3_plano2 += self.tasa_aprendizaje * error_p2 * obj.posZ
                self.sesgo_plano2 += self.tasa_aprendizaje * error_p2

                error_total_plano2 += abs(error_p2)

            # Guardar errores y pesos
            self.historial_errores_plano1.append(error_total_plano1)
            self.historial_errores_plano2.append(error_total_plano2)
            self.historial_errores.append(error_total_plano1 + error_total_plano2)
            
            self.historial_pesos.append([
                self.peso_1, self.peso_2, self.peso_3, self.sesgo,
                self.peso_1_plano2, self.peso_2_plano2, self.peso_3_plano2, self.sesgo_plano2
            ])

            print(f"Época {self.epocas_recorridas} | Error P1: {error_total_plano1} | Error P2: {error_total_plano2} | Total: {error_total_plano1 + error_total_plano2}")

            if error_total_plano1 == 0 and error_total_plano2 == 0:
                print(f"Convergencia en época {self.epocas_recorridas}")
                salida = True
            elif self.epocas_recorridas == self.maximo_epocas:
                print(f"Máximo de épocas alcanzado: {self.maximo_epocas}")
                salida = True

    def reiniciar_perceptron(self):
        """Reinicia ambos planos"""
        self.peso_1 = random.uniform(-10, 10)
        self.peso_2 = random.uniform(-10, 10)
        self.peso_3 = random.uniform(-10, 10)
        self.sesgo = 1
        
        self.peso_1_plano2 = random.uniform(-10, 10)
        self.peso_2_plano2 = random.uniform(-10, 10)
        self.peso_3_plano2 = random.uniform(-10, 10)
        self.sesgo_plano2 = 1
        
        self.epocas_recorridas = 0
        self.historial_errores = []
        self.historial_errores_plano1 = []
        self.historial_errores_plano2 = []
        self.historial_pesos = []
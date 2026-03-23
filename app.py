from flask import Flask, request, jsonify
from perceptronLogica import Perceptron
from objeto import objeto
import utilidades as funciones

app = Flask(__name__) #Ojo no olvidar: Esto crea el servidor le dice a flask donde esta
#Creacion del perceptron
objetos_entrenamiento = []

neurona = Perceptron(0.1, 1000)

#cuando alguien llame a esta URL, ejecuta esta función
@app.route('/crear_objetos_entrenamiento', methods=['GET']) #POST GET
def crear_objetos_entrenamiento():
    objetos_entrenamiento.clear()
    
    funciones.crear_objetos(300, True, objetos_entrenamiento, True)
    lista_obj_entrenamiento = []
    for obj in objetos_entrenamiento:
        lista_obj_entrenamiento.append({
            "x": obj.posX,
            "y": obj.posY,
            "z": obj.posZ,
            "clase": obj.clase,
            "color": obj.color
        })
    return jsonify({"objetos":lista_obj_entrenamiento})


@app.route('/entrenamiento', methods = ['GET'])
def entrenamiento():

    neurona.reiniciar_perceptron()
    neurona.entrenamiento_perceptron(objetos_entrenamiento)
    return jsonify({"mensaje": "Entrenamiento completado", "epocas": neurona.epocas_recorridas})
    

    

@app.route('/metricas', methods = ['GET'])
def metricas():

    return jsonify({
    "historial_errores": neurona.historial_errores,
    "historial_pesos": neurona.historial_pesos,
    "epocas_recorridas": neurona.epocas_recorridas
    })


#Creacion de la recta
@app.route('/plano', methods=['GET'])
def plano():
    return jsonify({
        "peso_1": neurona.peso_1,
        "peso_2": neurona.peso_2,
        "peso_3": neurona.peso_3,
        "sesgo": neurona.sesgo
    })


#Inicializar el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
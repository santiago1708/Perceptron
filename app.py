from flask import Flask, request, jsonify
from perceptronLogica import Perceptron
from objeto import objeto
import utilidades as funciones

app = Flask(__name__)
lista_objetos = []

neurona = Perceptron(0.1, 1000)

@app.route('/crear_objetos_entrenamiento', methods=['GET'])
def crear_objetos_entrenamiento():
    lista_objetos.clear()
    
    funciones.crear_objetos(300, True, lista_objetos, True)
    lista_obj_entrenamiento = []
    for obj in lista_objetos:
        lista_obj_entrenamiento.append({
            "x": obj.posX,
            "y": obj.posY,
            "z": obj.posZ,
            "clase": obj.clase,
            "color": obj.color
        })
    return jsonify({"objetos":lista_obj_entrenamiento})


@app.route('/entrenamiento', methods=['GET'])
def entrenamiento():
    neurona.reiniciar_perceptron()
    neurona.entrenamiento_perceptron(lista_objetos)
    return jsonify({
        "mensaje": "Entrenamiento completado", 
        "epocas": neurona.epocas_recorridas
    })
    

@app.route('/metricas', methods=['GET'])
def metricas():
    # Convertir listas a arrays de forma explícita
    return jsonify({
        "historial_errores": [int(x) for x in neurona.historial_errores],
        "historial_errores_plano1": [int(x) for x in neurona.historial_errores_plano1],
        "historial_errores_plano2": [int(x) for x in neurona.historial_errores_plano2],
        "historial_pesos": [{"pesos": [float(p) for p in epoca]} for epoca in neurona.historial_pesos],
        "epocas_recorridas": neurona.epocas_recorridas
    })


# DOS ENDPOINTS PARA LOS DOS PLANOS
@app.route('/plano1', methods=['GET'])
def plano1():
    return jsonify({
        "peso_1": neurona.peso_1,
        "peso_2": neurona.peso_2,
        "peso_3": neurona.peso_3,
        "sesgo": neurona.sesgo
    })

@app.route('/plano2', methods=['GET'])
def plano2():
    return jsonify({
        "peso_1": neurona.peso_1_plano2,
        "peso_2": neurona.peso_2_plano2,
        "peso_3": neurona.peso_3_plano2,
        "sesgo": neurona.sesgo_plano2
    })


@app.route('/generar_nube', methods=['POST'])
def generar_nube():
    global lista_objetos
    lista_objetos.clear()

    data = request.json
    cantidad = int(data['cantidad'])
    media = float(data['media'])
    desviacion = float(data['desviacion'])
    distribucion = data['distribucion']

    lista_objetos = funciones.generar_nube(cantidad, media, desviacion, distribucion)

    lista_obj_nube = []
    for obj in lista_objetos:
        lista_obj_nube.append({
            "x": obj.posX,
            "y": obj.posY,
            "z": obj.posZ,
            "clase": obj.clase,
            "color": obj.color
        })

    return jsonify({"objetos": lista_obj_nube})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
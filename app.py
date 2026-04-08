from flask import Flask, request, jsonify
from perceptronLogica import Perceptron
from objeto import objeto
import utilidades as funciones

app = Flask(__name__)
lista_objetos = []
num_clases = 2
clases_con_nube = set()

neurona = Perceptron(0.1, 1000)

@app.route('/crear_objetos_entrenamiento', methods=['GET'])
def crear_objetos_entrenamiento():
    global lista_objetos, clases_con_nube
    lista_objetos.clear()
    clases_con_nube.clear()
    
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


@app.route('/set_num_clases', methods=['POST'])
def set_num_clases():
    global num_clases, clases_con_nube, lista_objetos
    data = request.json
    num_clases = int(data['num_clases'])
    clases_con_nube.clear()
    lista_objetos.clear()
    return jsonify({
        "mensaje": f"Número de clases establecido a {num_clases}",
        "num_clases": num_clases
    })


@app.route('/generar_nube', methods=['POST'])
def generar_nube():
    global lista_objetos, clases_con_nube

    data = request.json
    clase = data.get('clase', None)
    if clase is not None:
        clase = int(clase)
    cantidad = int(data['cantidad'])
    media = float(str(data['media']).replace(',', '.'))
    desviacion = float(str(data['desviacion']).replace(',', '.'))
    distribucion = data['distribucion']

    if clase is None:
        # Comportamiento anterior: reemplazar todos los objetos con asignación automática
        lista_objetos.clear()
        clases_con_nube.clear()
        nuevos_objetos = funciones.generar_nube(cantidad, media, desviacion, distribucion)
        lista_objetos.extend(nuevos_objetos)
        for obj in nuevos_objetos:
            clases_con_nube.add(obj.clase)
    else:
        # Nuevo comportamiento: agregar objetos de la clase indicada sin borrar las demás
        nuevos_objetos = funciones.generar_nube(cantidad, media, desviacion, distribucion, clase)
        lista_objetos.extend(nuevos_objetos)
        clases_con_nube.add(clase)

    lista_obj_nube = []
    for obj in nuevos_objetos:
        lista_obj_nube.append({
            "x": obj.posX,
            "y": obj.posY,
            "z": obj.posZ,
            "clase": obj.clase,
            "color": obj.color
        })

    nubes_completas = len(clases_con_nube) >= num_clases

    return jsonify({
        "objetos": lista_obj_nube,
        "clases_con_nube": list(clases_con_nube),
        "nubes_completas": nubes_completas,
        "num_clases_requeridas": num_clases
    })


@app.route('/reset_nubes', methods=['POST'])
def reset_nubes():
    global lista_objetos, clases_con_nube
    lista_objetos.clear()
    clases_con_nube.clear()
    return jsonify({
        "mensaje": "Nubes reiniciadas",
        "clases_con_nube": [],
        "nubes_completas": False
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
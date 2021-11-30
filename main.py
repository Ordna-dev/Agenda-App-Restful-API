from flask import Flask, jsonify, request

from conexion import crear_usuario, iniciar_sesion
from conexion import insertar_contacto, get_contactos, get_contacto, modificar_contacto, eliminar_contacto, get_contactos_usuario

app = Flask(__name__)

@app.route("/api/v1/usuarios", methods=["POST"])
@app.route("/api/v1/usuarios/<int:id>/contactos", methods=["GET"])
def usuario():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)

            if crear_usuario(data['correo'], data['contrasena']):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "existe"})
        except:
            return jsonify({"code": "error"})
    elif request.method == "GET" and id is not None:
        return jsonify(get_contactos_usuario(id))

@app.route("/api/v1/sesiones", methods=["POST"])
def sesion():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            correo = data['correo']
            contra = data['contrasena']
            id, ok = iniciar_sesion(correo, contra)
            if ok:
                return jsonify({"code": "ok", "id": id})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"})

@app.route("/api/v1/contactos", methods=["GET", "POST"])
@app.route("/api/v1/contactos/<int:id>", methods=["GET", "PATCH", "DELETE"])
def peliculas(id=None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)
            if insertar_contacto(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "error"})
    elif request.method == "GET" and id is None:
        return jsonify(get_contactos())
    elif request.method == "GET" and id is not None:
        return jsonify(get_contacto(id))
    elif request.method == "PATCH" and id is not None and request.is_json:
        data = request.get_json()
        columna = data['columna']
        valor = data['valor']
        print(data)
        if modificar_contacto(id, columna, valor):
            return jsonify({'code': "ok"})
        else:
            return jsonify({'code': "no"})
    elif request.method == "DELETE" and id is not None:
        if eliminar_contacto(id):
            return jsonify(code='ok')
        else:
            return jsonify(code='ok')

app.run(debug=True) 
import mysql.connector

bd = mysql.connector.connect(
    user='alejandro', password='naruto11',
    database='agenda')

cursor = bd.cursor()

def get_usuarios():
    consulta = "SELECT * FROM usuario"

    cursor.execute(consulta)
    usuarios = []
    for row in cursor.fetchall():
        usuario = {
            'id': row[0],
            'correo_usuario': row[1],
            'contrasena': row[2]
        }
        usuarios.append(usuario)
    return usuarios

def existe_usuario(correo):
    query = "SELECT COUNT(*) FROM usuario WHERE correo_usuario = %s"
    cursor.execute(query, (correo,))

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

import hashlib
def crear_usuario(correo, contra):
    if existe_usuario(correo):
        return False
    else:
        h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest()
        insertar = "INSERT INTO usuario(correo_usuario, contrasena) VALUES(%s, %s)"
        cursor.execute(insertar, (correo, h))
        bd.commit()

        return True

def iniciar_sesion(correo, contra):
    h = hashlib.new('sha256', bytes(contra, 'utf-8'))
    h = h.hexdigest()
    query = "SELECT id FROM usuario WHERE correo_usuario = %s AND contrasena = %s"
    cursor.execute(query, (correo, h))
    id = cursor.fetchone()
    if id:
        return id[0], True
    else:
        return None, False

def insertar_contacto(contacto):
    nombre = contacto['nombre']
    telefono = contacto['telefono']
    correo = contacto['correo']
    facebook = contacto['facebook']
    linkedin = contacto['linkedin']
    twitter = contacto['twitter']
    foto = contacto['foto']
    usuarioId = contacto['usuarioId']

    insertar = "INSERT INTO contactos \
        (nombre, telefono, correo, facebook, linkedin, twitter, foto, usuarioId) \
        VALUES (%s, %s ,%s, %s, %s, %s, %s, %s)"
    cursor.execute(insertar, 
    (nombre, telefono, correo, facebook, linkedin, twitter, foto, usuarioId))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_contactos():
    query = "SELECT id, nombre, telefono, correo, facebook, linkedin, twitter, foto FROM contactos"
    cursor.execute(query)
    contactos = []
    for row in cursor.fetchall():
        pelicula = {
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'correo': row[3],
            'facebook': row[4],
            'linkedin': row[5],
            'twitter': row[6],
            'foto': row[7] 
        }
        contactos.append(pelicula)

    return contactos

def get_contacto(id):
    query = "SELECT * FROM contactos WHERE id = %s"
    cursor.execute(query, (id,))
    contacto = {}
    row = cursor.fetchone()
    if row:
        contacto['id'] = row[0]
        contacto['nombre'] = row[1]
        contacto['telefono'] = row[2]
        contacto['correo'] = row[3]
        contacto['facebook'] = row[4]
        contacto['linkedin'] = row[5]
        contacto['twitter'] = row[6]
        contacto['foto'] = row[7]

    return contacto

def modificar_contacto(id, columna, valor):
    update = f"UPDATE contactos SET {columna} = %s WHERE id = %s" 
    cursor.execute(update, (valor, id))
    bd.commit()
    if cursor.rowcount:  
        return True
    else:
        return False

def eliminar_contacto(id):
    eliminar = "DELETE from contactos WHERE id = %s"
    cursor.execute(eliminar, (id,))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_contactos_usuario(id):
    query = "SELECT * FROM contactos WHERE usuarioId = %s"
    cursor.execute(query, (id,))
    contactos = []
    for row in cursor.fetchall():
        pelicula = {
            'id': row[0],
            'nombre': row[1],
            'telefono': row[2],
            'correo': row[3],
            'facebook': row[4],
            'linkedin': row[5],
            'twitter': row[6],
            'foto': row[7] 
        }
        contactos.append(pelicula)
    return contactos
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flasgger import Swagger
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'roundhouse.proxy.rlwy.net'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SHJSCKWuVJLXMBXmHjwYrrfNwWJhJoCp'
app.config['MYSQL_DB'] = 'railway'
app.config['MYSQL_PORT'] = 35483
app.secret_key = 'tu_clave_secreta'

mysql = MySQL(app)

# Swagger UI Configuration
swagger = Swagger(app)

# API Routes

@app.route('/')
def home():
    """Welcome Endpoint
    ---
    responses:
      200:
        description: Welcome to the Usuarios API
    """
    return jsonify({
        "message": "Welcome to the Usuarios API",
        "endpoints": {
            "GET all users": "/usuarios",
            "GET single user": "/usuarios/<id>",
            "POST create user": "/usuarios",
            "PUT update user": "/usuarios/<id>",
            "DELETE delete user": "/usuarios/<id>"
        }
    })

@app.route('/usuarios', methods=['GET'])
def get_all_users():
    """Get All Users
    ---
    responses:
      200:
        description: List of all users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              usuario:
                type: string
              correo:
                type: string
              is_admin:
                type: boolean
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    cursor.close()

    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'usuario': row[1],
            'correo': row[2],
            'is_admin': bool(row[4])
        })
    return jsonify(users)

@app.route('/usuarios/<int:id>', methods=['GET'])
def get_user(id):
    """Get a Single User by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the user
    responses:
      200:
        description: User object
        schema:
          type: object
          properties:
            id:
              type: integer
            usuario:
              type: string
            correo:
              type: string
            is_admin:
              type: boolean
      404:
        description: User not found
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        user = {
            'id': row[0],
            'usuario': row[1],
            'correo': row[2],
            'is_admin': bool(row[4])
        }
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/usuarios', methods=['POST'])
def create_user():
    """Create a New User
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
            correo:
              type: string
            contraseña:
              type: string
            is_admin:
              type: boolean
    responses:
      201:
        description: User created successfully
    """
    data = request.json
    usuario = data.get('usuario')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    is_admin = data.get('is_admin', 0)

    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO usuarios (usuario, correo, contraseña, is_admin)
        VALUES (%s, %s, %s, %s)
    """, (usuario, correo, contraseña, is_admin))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_user(id):
    """Update a User
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the user to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            usuario:
              type: string
            correo:
              type: string
            contraseña:
              type: string
            is_admin:
              type: boolean
    responses:
      200:
        description: User updated successfully
    """
    data = request.json
    usuario = data.get('usuario')
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    is_admin = data.get('is_admin')

    cursor = mysql.connection.cursor()
    cursor.execute("""
        UPDATE usuarios
        SET usuario = %s, correo = %s, contraseña = %s, is_admin = %s
        WHERE id = %s
    """, (usuario, correo, contraseña, is_admin, id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User updated successfully'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_user(id):
    """Delete a User
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the user to delete
    responses:
      200:
        description: User deleted successfully
    """
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User deleted successfully'})

    #Metodos para el pronosticador
    # Obtener todos los equipos
@app.route('/equipos', methods=['GET'])
def get_all_equipos():
    """Obtener todos los equipos
    ---
    responses:
      200:
        description: Lista de equipos
        schema:
          type: array
          items:
            type: object
            properties:
              id_equipo:
                type: integer
              nombre:
                type: string
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM equipos")
    rows = cursor.fetchall()
    cursor.close()

    equipos = [{'id_equipo': row[0], 'nombre': row[1]} for row in rows]
    return jsonify(equipos)

# Obtener un equipo por ID
@app.route('/equipos/<int:id_equipo>', methods=['GET'])
def get_equipo(id_equipo):
    """Obtener un equipo por ID
    ---
    parameters:
      - name: id_equipo
        in: path
        type: integer
        required: true
        description: ID del equipo a buscar
    responses:
      200:
        description: Equipo encontrado
      404:
        description: Equipo no encontrado
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s", (id_equipo,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        equipo = {'id_equipo': row[0], 'nombre': row[1]}
        return jsonify(equipo)
    return jsonify({'error': 'Equipo no encontrado'}), 404

# Crear un equipo
@app.route('/equipos', methods=['POST'])
def create_equipo():
    """Crear un nuevo equipo
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
    responses:
      201:
        description: Equipo creado exitosamente
    """
    data = request.json
    nombre = data.get('nombre')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO equipos (nombre) VALUES (%s)", (nombre,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Equipo creado exitosamente'}), 201

# Actualizar un equipo
@app.route('/equipos/<int:id_equipo>', methods=['PUT'])
def update_equipo(id_equipo):
    """Actualizar un equipo
    ---
    parameters:
      - name: id_equipo
        in: path
        type: integer
        required: true
        description: ID del equipo a actualizar
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
    responses:
      200:
        description: Equipo actualizado exitosamente
    """
    data = request.json
    nombre = data.get('nombre')

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE equipos SET nombre = %s WHERE id_equipo = %s", (nombre, id_equipo))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Equipo actualizado exitosamente'})

# Eliminar un equipo
@app.route('/equipos/<int:id_equipo>', methods=['DELETE'])
def delete_equipo(id_equipo):
    """Eliminar un equipo
    ---
    parameters:
      - name: id_equipo
        in: path
        type: integer
        required: true
        description: ID del equipo a eliminar
    responses:
      200:
        description: Equipo eliminado exitosamente
    """
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM equipos WHERE id_equipo = %s", (id_equipo,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Equipo eliminado exitosamente'})
  
#Obtener equipo por nombre
@app.route('/equipos/nombre/<string:nombre_equipo>', methods=['GET'])
def get_equipo_por_nombre(nombre_equipo):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM equipos WHERE nombre LIKE %s", (f"%{nombre_equipo}%",))
    rows = cursor.fetchall()
    cursor.close()

    if rows:
        equipos = [{'id_equipo': row[0], 'nombre': row[1]} for row in rows]
        return jsonify(equipos)

    return jsonify([]), 200

    #tabla campeonatos
    # Obtener todos los campeonatos
@app.route('/campeonatos', methods=['GET'])
def get_all_campeonatos():
    """Obtener todos los campeonatos
    ---
    responses:
      200:
        description: Lista de campeonatos
        schema:
          type: array
          items:
            type: object
            properties:
              id_campeonato:
                type: integer
              id_equipo:
                type: integer
              copas_nacionales:
                type: integer
              copas_internacionales:
                type: integer
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM campeonatos")
    rows = cursor.fetchall()
    cursor.close()

    campeonatos = [{
        'id_campeonato': row[0],
        'id_equipo': row[1],
        'copas_nacionales': row[2],
        'copas_internacionales': row[3]
    } for row in rows]
    return jsonify(campeonatos)

# Obtener un campeonato por ID
@app.route('/campeonatos/<int:id_campeonato>', methods=['GET'])
def get_campeonato(id_campeonato):
    """Obtener un campeonato por ID
    ---
    parameters:
      - name: id_campeonato
        in: path
        type: integer
        required: true
        description: ID del campeonato a buscar
    responses:
      200:
        description: Campeonato encontrado
      404:
        description: Campeonato no encontrado
    """
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM campeonatos WHERE id_campeonato = %s", (id_campeonato,))
    row = cursor.fetchone()
    cursor.close()

    if row:
        campeonato = {
            'id_campeonato': row[0],
            'id_equipo': row[1],
            'copas_nacionales': row[2],
            'copas_internacionales': row[3]
        }
        return jsonify(campeonato)
    return jsonify({'error': 'Campeonato no encontrado'}), 404

# Crear un campeonato
@app.route('/campeonatos', methods=['POST'])
def create_campeonato():
    """Crear un nuevo campeonato
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_equipo:
              type: integer
            copas_nacionales:
              type: integer
            copas_internacionales:
              type: integer
    responses:
      201:
        description: Campeonato creado exitosamente
    """
    data = request.json
    id_equipo = data.get('id_equipo')
    copas_nacionales = data.get('copas_nacionales', 0)
    copas_internacionales = data.get('copas_internacionales', 0)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO campeonatos (id_equipo, copas_nacionales, copas_internacionales) VALUES (%s, %s, %s)",
        (id_equipo, copas_nacionales, copas_internacionales)
    )
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Campeonato creado exitosamente'}), 201

# Actualizar un campeonato
@app.route('/campeonatos/<int:id_campeonato>', methods=['PUT'])
def update_campeonato(id_campeonato):
    """Actualizar un campeonato
    ---
    parameters:
      - name: id_campeonato
        in: path
        type: integer
        required: true
        description: ID del campeonato a actualizar
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            id_equipo:
              type: integer
            copas_nacionales:
              type: integer
            copas_internacionales:
              type: integer
    responses:
      200:
        description: Campeonato actualizado exitosamente
    """
    data = request.json
    id_equipo = data.get('id_equipo')
    copas_nacionales = data.get('copas_nacionales', 0)
    copas_internacionales = data.get('copas_internacionales', 0)

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE campeonatos SET id_equipo = %s, copas_nacionales = %s, copas_internacionales = %s WHERE id_campeonato = %s",
        (id_equipo, copas_nacionales, copas_internacionales, id_campeonato)
    )
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Campeonato actualizado exitosamente'})

# Eliminar un campeonato
@app.route('/campeonatos/<int:id_campeonato>', methods=['DELETE'])
def delete_campeonato(id_campeonato):
    """Eliminar un campeonato
    ---
    parameters:
      - name: id_campeonato
        in: path
        type: integer
        required: true
        description: ID del campeonato a eliminar
    responses:
      200:
        description: Campeonato eliminado exitosamente
    """
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM campeonatos WHERE id_campeonato = %s", (id_campeonato,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({'message': 'Campeonato eliminado exitosamente'})



if __name__ == '__main__':
    app.run(debug=True)

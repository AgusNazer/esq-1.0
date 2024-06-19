from flask import Blueprint, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Obtener las variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


users = Blueprint('users', __name__)

@users.route('/create_user', methods=['POST'])
def create_user():
    if request.headers['Content-Type'] != 'application/json':
       return jsonify({"error": "Unsupported Media Type"}), 415
    
    data = request.get_json()
   
    #Validar datos de entrada
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    username = data['username']
    email = data['email']
    password = data['password']  # Asegúrate de encriptar la contraseña en un caso real
    
     # Asegúrate de encriptar la contraseña en un caso real

    # Aquí es donde agregarías la lógica para guardar el usuario en la base de datos

   # Conectar a PostgreSQL
    try:
        connect = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Conexión exitosa")
        
        cur = connect.cursor()
        
        # Insertar el usuario en la base de datos
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        connect.commit()
        
        cur.close()
        connect.close()

        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        print(f"Error en la conexión: {e}")
        return jsonify({"error": "Failed to create user"}), 500

# Nota: Este archivo asume que tienes una tabla 'users' en tu base de datos PostgreSQL
# con columnas 'username', 'email' y 'password' para almacenar la información del usuario
from flask import Flask
from flask import Blueprint, request, jsonify
import psycopg2 
import os
from dotenv import load_dotenv
from src.routes.user import users

load_dotenv()

# Obtener las variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/users')

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
    
    connect.commit()
    cur.close()
    connect.close()

except Exception as e:
    print(f"Error en la conexión: {e}")


@app.route('/')
def hello_world():
    return 'Hello, World'

if __name__ == '__main__':
    app.run(debug=True)
# tests para app y connections.
from app import app
from config_db import engine, SessionLocal
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

def test_db_connection():
    # Crear una sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    # Realizar una consulta de prueba
    result = session.execute(text('SELECT 1'))
    assert result.fetchone() == (1,)

def test_flask_route():
    client = app.test_client()

    # Ejecutar una solicitud a la ruta que accede a la base de datos
    response = client.get('/users/get_all_users')

    assert response.status_code == 200
    assert isinstance(response.json, list)

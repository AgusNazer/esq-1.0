# import psycopg2 
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Obtener las variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Verificar que las variables de entorno se están cargando correctamente
print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")

# Crear la cadena de conexión
DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

print(f"DATABASE_URL: {DATABASE_URL}")
# DATABASE_URL = "postgresql://postgresqlesq_user:SSextFcn6tNv4n3KVagpUN2MSNitaX3M@dpg-cpsd3tt6l47c73e3jr00-a.oregon-postgres.render.com/postgresqlesq"
# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta línea no es necesaria ya que SQLAlchemy se encarga de la conexión
# print("Conexión a la base de datos exitosa")

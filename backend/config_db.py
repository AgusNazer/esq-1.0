# import psycopg2 
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

load_dotenv()

# Obtener las variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Crear la cadena de conexión
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DATABASE_URL = "postgresql://postgres:Alma2022@localhost:5432/esq1.0"

#render postgre
# DATABASE_URL = f"postgresql://esq1_0_user:PydlM33zqjJW9KHNd93A2XqN61aUIlxu@dpg-cptl40d2ng1s73e2sc80-a.oregon-postgres.render.com/esq1_0"

print(f"DB_USER: {DB_USER}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")

engine = create_engine(DATABASE_URL)


# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta línea no es necesaria ya que SQLAlchemy se encarga de la conexión
print("Conexión a la base de datos exitosa")

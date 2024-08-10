import psycopg2 
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

# Obtener las variables de entorno
DB_USER = os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# local-pgadmin desarrollo
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


#railway
# DATABASE_URL = ""

#render postgre
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD= os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')
# DB_NAME = os.getenv('DB_NAME')



engine = create_engine(DATABASE_URL)


# Crear una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta línea no es necesaria ya que SQLAlchemy se encarga de la conexión
print("Conexión a la base de datos exitosa")

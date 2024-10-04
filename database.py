from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:988156699Ms@localhost:5432/songs_db"

# Reemplaza 'user', 'password', 'localhost', y 'songs_db' con los valores de tu base de datos PostgreSQL.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Definición del modelo de la tabla de canciones
class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String, index=True)
    cover_url = Column(String, index=True)

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

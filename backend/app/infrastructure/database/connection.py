# app/infrastructure/database/connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from ...core.config import settings

# Crear Engine(motor) de SQLAlchemy
engine = create_engine(
    settings.database_url,
    echo=settings.debug, #SQL queries en consolo si debug=True
    pool_pre_ping=True, #Verificar la conexión antes de usar
    pool_size=5, #Tamaño de pool de conexiones
    max_overflow=10 #Conexiones extra permitidas
)

#Crear sesión local
SessionLocal= sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obtener la sesion de la BD
    Yields: Session: Sesion de SQLAlchamy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    Solo para desarrollo - en produccion usa Alembic
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)
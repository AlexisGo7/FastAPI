"""Configuracion central de la conexion entre SQLAlchemy y SQLite."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite guarda la base en este archivo relativo a la raiz del proyecto.
DATABASE_URL = "sqlite:///./device_systems.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    """Activa las claves foraneas, desactivadas por defecto en SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Fabrica una sesion independiente para cada solicitud de la API.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base que registra la metadata de todos los modelos ORM.
Base = declarative_base()
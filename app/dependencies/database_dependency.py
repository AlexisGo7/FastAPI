"""Dependencias reutilizables de FastAPI para acceder a la base de datos."""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Entrega una sesion y garantiza su cierre al terminar la solicitud."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
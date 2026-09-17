"""Modelo ORM que relaciona usuarios con dispositivos prestados."""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Loan(Base):
    """Registro de un prestamo activo o historico."""

    __tablename__ = "loans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Las claves foraneas garantizan que ambas entidades existan.
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    device_id = Column(
        Integer,
        ForeignKey("devices.id"),
        nullable=False
    )

    loan_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Permanece vacia mientras el prestamo siga activo.
    return_date = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String,
        nullable=False
    )

    # Relaciones bidireccionales para consultas y respuestas detalladas.
    user = relationship(
        "User",
        back_populates="loans"
    )

    device = relationship(
        "Device",
        back_populates="loans"
    )
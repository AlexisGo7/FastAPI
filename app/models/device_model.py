"""Modelo ORM de los dispositivos disponibles para prestamo."""

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Device(Base):
    """Equipo tecnologico que puede prestarse y conservar historial."""

    __tablename__ = "devices"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    # El serial identifica fisicamente el equipo y no puede repetirse.
    serial_number = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    device_type = Column(
        String,
        nullable=False
    )

    brand = Column(
        String,
        nullable=True
    )

    # Se actualiza al crear o devolver un prestamo.
    is_available = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Un dispositivo puede aparecer en muchos prestamos historicos.
    loans = relationship(
        "Loan",
        back_populates="device"
    )
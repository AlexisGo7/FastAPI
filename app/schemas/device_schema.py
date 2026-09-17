"""Schemas Pydantic para crear, actualizar y responder dispositivos."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


# Lista cerrada de tipos aceptados por la API.
DeviceType = Literal["laptop", "tablet", "proyector", "camara", "router", "monitor"]


class DeviceCreate(BaseModel):
    """Datos necesarios para registrar un dispositivo."""

    name: str = Field(..., min_length=2, max_length=150)
    serial_number: str = Field(..., min_length=2, max_length=100)
    device_type: DeviceType
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool = True


class DeviceUpdate(DeviceCreate):
    """PUT reutiliza todas las validaciones de DeviceCreate."""

    pass


class DevicePatch(BaseModel):
    """Campos opcionales para modificar parcialmente un dispositivo."""

    name: str | None = Field(default=None, min_length=2, max_length=150)
    serial_number: str | None = Field(default=None, min_length=2, max_length=100)
    device_type: DeviceType | None = None
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool | None = None


class DeviceResponse(DeviceCreate):
    """Respuesta publica con identificador y fecha de creacion."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

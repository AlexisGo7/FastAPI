"""Schemas Pydantic para validar entradas y salidas de usuarios."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
    """Datos requeridos para registrar un usuario."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre del usuario"
    )

    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario"
    )

    role: Literal["admin", "support", "user"] = Field(
        ...,
        description="Rol del usuario"
    )

    is_active: bool = Field(
        default=True,
        description="Estado del usuario"
    )


class UserUpdate(BaseModel):
    """Datos completos requeridos por la operacion PUT."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: EmailStr

    role: Literal["admin", "support", "user"]

    is_active: bool


class UserPatch(BaseModel):
    """Campos opcionales aceptados por la operacion PATCH."""

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: EmailStr | None = None

    role: Literal["admin", "support", "user"] | None = None

    is_active: bool | None = None


class UserResponse(BaseModel):
    """Representacion publica de un usuario almacenado."""

    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool
    created_at: datetime

    # Permite construir la respuesta directamente desde un objeto ORM.
    model_config = ConfigDict(from_attributes=True)
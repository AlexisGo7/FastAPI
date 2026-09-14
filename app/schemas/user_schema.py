from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Literal


class UserCreate(BaseModel):
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
    name: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    email: EmailStr

    role: Literal["admin", "support", "user"]

    is_active: bool


class UserPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    email: EmailStr | None = None

    role: Literal["admin", "support", "user"] | None = None

    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
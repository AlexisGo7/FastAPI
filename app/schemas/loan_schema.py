"""Schemas Pydantic para prestamos y respuestas con relaciones."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.device_schema import DeviceType


# Estados de negocio permitidos para el ciclo de vida de un prestamo.
LoanStatus = Literal["active", "returned", "overdue"]


class LoanCreate(BaseModel):
    """Identifica al usuario y al dispositivo que se desean relacionar."""

    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    """Schema reservado para cambios controlados del estado."""

    status: LoanStatus


class UserSummary(BaseModel):
    """Informacion minima del usuario dentro de un detalle de prestamo."""

    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class DeviceSummary(BaseModel):
    """Informacion minima del dispositivo dentro de un detalle."""

    id: int
    name: str
    serial_number: str
    device_type: DeviceType

    model_config = ConfigDict(from_attributes=True)


class LoanResponse(BaseModel):
    """Respuesta plana usada en crear y devolver prestamos."""

    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: LoanStatus

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    """Respuesta enriquecida con los datos relacionados por join."""

    # El ORM usa id, pero la API expone el nombre mas descriptivo loan_id.
    loan_id: int = Field(validation_alias="id", serialization_alias="loan_id")
    loan_date: datetime
    return_date: datetime | None
    status: LoanStatus
    user: UserSummary
    device: DeviceSummary

    model_config = ConfigDict(from_attributes=True)

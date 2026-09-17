from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


DeviceType = Literal["laptop", "tablet", "proyector", "camara", "router", "monitor"]


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    serial_number: str = Field(..., min_length=2, max_length=100)
    device_type: DeviceType
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool = True


class DeviceUpdate(DeviceCreate):
    pass


class DevicePatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    serial_number: str | None = Field(default=None, min_length=2, max_length=100)
    device_type: DeviceType | None = None
    brand: str | None = Field(default=None, max_length=100)
    is_available: bool | None = None


class DeviceResponse(DeviceCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

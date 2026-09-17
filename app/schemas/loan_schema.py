from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.device_schema import DeviceType


LoanStatus = Literal["active", "returned", "overdue"]


class LoanCreate(BaseModel):
    user_id: int
    device_id: int


class LoanUpdate(BaseModel):
    status: LoanStatus


class UserSummary(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class DeviceSummary(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: DeviceType

    model_config = ConfigDict(from_attributes=True)


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: datetime | None
    status: LoanStatus

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    loan_id: int = Field(validation_alias="id", serialization_alias="loan_id")
    loan_date: datetime
    return_date: datetime | None
    status: LoanStatus
    user: UserSummary
    device: DeviceSummary

    model_config = ConfigDict(from_attributes=True)

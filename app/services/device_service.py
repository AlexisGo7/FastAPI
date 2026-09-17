from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def get_device_by_id(db: Session, device_id: int) -> Device | None:
    return db.scalar(select(Device).where(Device.id == device_id))


def get_device_by_serial_number(db: Session, serial_number: str) -> Device | None:
    return db.scalar(select(Device).where(Device.serial_number == serial_number))


def get_devices(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
) -> list[Device]:
    statement = select(Device)

    if device_type is not None:
        statement = statement.where(Device.device_type == device_type)
    if is_available is not None:
        statement = statement.where(Device.is_available == is_available)
    if brand is not None:
        statement = statement.where(Device.brand.ilike(f"%{brand}%"))
    if search is not None:
        pattern = f"%{search}%"
        statement = statement.where(
            Device.name.ilike(pattern) | Device.serial_number.ilike(pattern)
        )

    statement = statement.order_by(Device.name)
    return list(db.scalars(statement).all())


def create_device(db: Session, device_data: DeviceCreate) -> Device:
    device = Device(**device_data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, device: Device, device_data: DeviceUpdate) -> Device:
    for field, value in device_data.model_dump().items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device: Device, device_data: DevicePatch) -> Device:
    changes = device_data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device: Device) -> None:
    db.delete(device)
    db.commit()

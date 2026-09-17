"""Operaciones CRUD y busquedas avanzadas de dispositivos."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DevicePatch, DeviceUpdate


def get_device_by_id(db: Session, device_id: int) -> Device | None:
    """Busca un dispositivo por identificador."""
    return db.scalar(select(Device).where(Device.id == device_id))


def get_device_by_serial_number(db: Session, serial_number: str) -> Device | None:
    """Busca por serial para proteger la restriccion unique."""
    return db.scalar(select(Device).where(Device.serial_number == serial_number))


def get_devices(
    db: Session,
    device_type: str | None = None,
    is_available: bool | None = None,
    brand: str | None = None,
    search: str | None = None,
) -> list[Device]:
    """Lista equipos con filtros combinables y busqueda textual."""
    statement = select(Device)

    if device_type is not None:
        statement = statement.where(Device.device_type == device_type)
    if is_available is not None:
        statement = statement.where(Device.is_available == is_available)
    # ilike permite buscar sin distinguir mayusculas y minusculas.
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
    """Registra un equipo y devuelve su version sincronizada con la DB."""
    device = Device(**device_data.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, device: Device, device_data: DeviceUpdate) -> Device:
    """Reemplaza todos los datos editables del equipo."""
    for field, value in device_data.model_dump().items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device: Device, device_data: DevicePatch) -> Device:
    """Aplica unicamente los campos presentes en la solicitud."""
    changes = device_data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device: Device) -> None:
    """Elimina el equipo; la FK protege su historial de prestamos."""
    db.delete(device)
    db.commit()

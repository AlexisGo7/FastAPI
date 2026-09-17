"""Endpoints HTTP para el inventario de dispositivos."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import (
    DeviceCreate,
    DevicePatch,
    DeviceResponse,
    DeviceType,
    DeviceUpdate,
)
from app.services import device_service


router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    response_description="Dispositivo creado correctamente",
)
def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    """Registra un equipo y protege la unicidad de su serial."""
    if device_service.get_device_by_serial_number(db, device_data.serial_number):
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    try:
        return device_service.create_device(db, device_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")


@router.get("", response_model=list[DeviceResponse], summary="Listar dispositivos")
def get_devices(
    device_type: DeviceType | None = Query(default=None),
    is_available: bool | None = Query(default=None),
    brand: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """Lista dispositivos aplicando filtros opcionales."""
    return device_service.get_devices(db, device_type, is_available, brand, search)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Buscar dispositivo por ID")
def get_device(device_id: int, db: Session = Depends(get_db)):
    """Busca un dispositivo por ID."""
    device = device_service.get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo completo")
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db),
):
    """Reemplaza todos los datos de un dispositivo."""
    device = device_service.get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    duplicate = device_service.get_device_by_serial_number(db, device_data.serial_number)
    if duplicate and duplicate.id != device_id:
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    try:
        return device_service.update_device(db, device, device_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo parcialmente")
def patch_device(
    device_id: int,
    device_data: DevicePatch,
    db: Session = Depends(get_db),
):
    """Actualiza parcialmente un dispositivo."""
    device = device_service.get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if device_data.serial_number is not None:
        duplicate = device_service.get_device_by_serial_number(db, device_data.serial_number)
        if duplicate and duplicate.id != device_id:
            raise HTTPException(status_code=400, detail="El número de serie ya está registrado")
    try:
        return device_service.patch_device(db, device, device_data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El número de serie ya está registrado")


@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar dispositivo")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Elimina un dispositivo sin historial; si lo tiene devuelve 409."""
    device = device_service.get_device_by_id(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    try:
        device_service.delete_device(db, device)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="No se puede eliminar un dispositivo con historial de préstamos")

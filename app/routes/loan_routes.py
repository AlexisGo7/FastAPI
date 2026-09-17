"""Endpoints para prestamos, devoluciones e historiales relacionados."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.device_schema import DeviceType
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse, LoanResponse, LoanStatus
from app.services import device_service, loan_service, user_service


router = APIRouter(prefix="/loans", tags=["Loans"])
related_router = APIRouter(tags=["Loans"])


@router.post(
    "",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    response_description="Préstamo creado correctamente",
)
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    """Crea un prestamo activo despues de validar sus relaciones."""
    if user_service.get_user_by_id(db, loan_data.user_id) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    device = device_service.get_device_by_id(db, loan_data.device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    # Un equipo no puede tener dos prestamos activos simultaneamente.
    if not device.is_available:
        raise HTTPException(status_code=409, detail="El dispositivo no está disponible")

    return loan_service.create_loan(db, loan_data)


@router.get("", response_model=list[LoanDetailResponse], summary="Listar préstamos con filtros")
def get_loans(
    loan_status: LoanStatus | None = Query(default=None, alias="status"),
    user_email: str | None = Query(default=None),
    device_type: DeviceType | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """Lista prestamos con filtros por estado, usuario y tipo de equipo."""
    return loan_service.get_loans(db, loan_status, user_email, device_type)


@router.get("/details", response_model=list[LoanDetailResponse], summary="Consultar detalles de préstamos")
def get_loan_details(
    loan_status: LoanStatus | None = Query(default=None, alias="status"),
    user_email: str | None = Query(default=None),
    device_type: DeviceType | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """Devuelve prestamos con usuario y dispositivo anidados."""
    return loan_service.get_loan_details(
        db,
        status=loan_status,
        user_email=user_email,
        device_type=device_type,
    )


@related_router.get("/users/{user_id}/loans", response_model=list[LoanDetailResponse], summary="Préstamos de un usuario")
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    """Consulta el historial completo de un usuario."""
    if user_service.get_user_by_id(db, user_id) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return loan_service.get_user_loans(db, user_id)


@related_router.get("/devices/{device_id}/loans", response_model=list[LoanDetailResponse], summary="Historial de un dispositivo")
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    """Consulta el historial completo de un dispositivo."""
    if device_service.get_device_by_id(db, device_id) is None:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return loan_service.get_device_loans(db, device_id)


@router.get("/{loan_id}", response_model=LoanDetailResponse, summary="Buscar préstamo por ID")
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    """Busca un prestamo por ID con sus relaciones cargadas."""
    loan = loan_service.get_loan_by_id(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Devolver dispositivo")
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    """Cierra un prestamo y vuelve a habilitar el dispositivo."""
    loan = loan_service.get_loan_by_id(db, loan_id)
    if loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    if loan.status == "returned":
        raise HTTPException(status_code=409, detail="El préstamo ya fue devuelto")
    return loan_service.return_loan(db, loan)

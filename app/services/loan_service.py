"""Logica de prestamos, relaciones y consultas con joins."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate


def get_loan_by_id(db: Session, loan_id: int) -> Loan | None:
    """Obtiene un prestamo junto con usuario y dispositivo relacionados."""
    statement = (
        select(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .where(Loan.id == loan_id)
    )
    return db.scalar(statement)


def get_loans(
    db: Session,
    status: str | None = None,
    user_email: str | None = None,
    device_type: str | None = None,
) -> list[Loan]:
    """Consulta prestamos usando joins y filtros opcionales."""
    statement = (
        select(Loan)
        .join(Loan.user)
        .join(Loan.device)
        .options(joinedload(Loan.user), joinedload(Loan.device))
    )

    # Los joins permiten filtrar por columnas de User y Device en una consulta.
    if status is not None:
        statement = statement.where(Loan.status == status)
    if user_email is not None:
        statement = statement.where(User.email.ilike(f"%{user_email}%"))
    if device_type is not None:
        statement = statement.where(Device.device_type == device_type)

    statement = statement.order_by(Loan.loan_date.desc())
    return list(db.scalars(statement).unique().all())


def get_loan_details(db: Session, **filters: str | None) -> list[Loan]:
    """Expone la consulta enriquecida usada por el endpoint de detalles."""
    return get_loans(
        db,
        status=filters.get("status"),
        user_email=filters.get("user_email"),
        device_type=filters.get("device_type"),
    )


def get_user_loans(db: Session, user_id: int) -> list[Loan]:
    """Devuelve el historial de prestamos de un usuario."""
    return get_loans_for_column(db, Loan.user_id == user_id)


def get_device_loans(db: Session, device_id: int) -> list[Loan]:
    """Devuelve el historial de prestamos de un dispositivo."""
    return get_loans_for_column(db, Loan.device_id == device_id)


def get_loans_for_column(db: Session, condition) -> list[Loan]:
    """Reutiliza la consulta relacionada con una condicion concreta."""
    statement = (
        select(Loan)
        .join(Loan.user)
        .join(Loan.device)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .where(condition)
        .order_by(Loan.loan_date.desc())
    )
    return list(db.scalars(statement).unique().all())


def create_loan(db: Session, loan_data: LoanCreate) -> Loan:
    """Crea un prestamo activo y bloquea el equipo como no disponible."""
    loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active",
    )
    # Las rutas validan la existencia; aqui se actualiza el estado atomico.
    device = db.scalar(select(Device).where(Device.id == loan_data.device_id))
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return get_loan_by_id(db, loan.id)


def return_loan(db: Session, loan: Loan) -> Loan:
    """Marca el prestamo como devuelto y libera el dispositivo."""
    loan.status = "returned"
    loan.return_date = datetime.utcnow()
    loan.device.is_available = True
    db.commit()
    db.refresh(loan)
    return get_loan_by_id(db, loan.id)

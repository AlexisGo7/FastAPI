"""Endpoints HTTP para crear y administrar usuarios."""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserUpdate
)
from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario"
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Crea un usuario y rechaza emails repetidos."""
    # La consulta previa permite devolver un error claro antes del constraint SQL.
    existing_user = user_service.get_user_by_email(
        db,
        user_data.email
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    try:
        return user_service.create_user(
            db,
            user_data
        )

    except IntegrityError:
        # El rollback deja la sesion reutilizable despues de un error SQL.
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )


@router.get(
    "",
    response_model=list[UserResponse],
    summary="Listar usuarios"
)
def get_users(
    role: Literal["admin", "support", "user"] | None = Query(
        default=None
    ),
    is_active: bool | None = Query(
        default=None
    ),
    order_by: Literal["name", "created_at"] = Query(
        default="name"
    ),
    db: Session = Depends(get_db)
):
    """Lista usuarios usando filtros validados por FastAPI."""
    return user_service.get_users(
        db,
        role=role,
        is_active=is_active,
        order_by=order_by
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Buscar usuario por ID"
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Devuelve un usuario o responde 404 si no existe."""
    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo"
)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Reemplaza todos los datos editables de un usuario."""
    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    existing_email = user_service.get_user_by_email(
        db,
        user_data.email
    )

    if existing_email and existing_email.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    try:
        return user_service.update_user(
            db,
            user,
            user_data
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcialmente"
)
def patch_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db)
):
    """Actualiza solo los campos enviados por el cliente."""
    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    if user_data.email is not None:
        existing_email = user_service.get_user_by_email(
            db,
            user_data.email
        )

        if existing_email and existing_email.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )

    try:
        return user_service.patch_user(
            db,
            user,
            user_data
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Elimina un usuario existente y devuelve 204 sin contenido."""
    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    user_service.delete_user(
        db,
        user
    )

    return None
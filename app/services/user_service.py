"""Operaciones de persistencia para el recurso User."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserPatch, UserUpdate


def get_user_by_id(db: Session, user_id: int) -> User | None:
	"""Busca un usuario por su clave primaria."""
	return db.scalar(select(User).where(User.id == user_id))


def get_user_by_email(db: Session, email: str) -> User | None:
	"""Busca un usuario por email para validar duplicados."""
	return db.scalar(select(User).where(User.email == email))


def get_users(
	db: Session,
	role: str | None = None,
	is_active: bool | None = None,
	order_by: str = "name",
) -> list[User]:
	"""Lista usuarios aplicando filtros y el orden solicitado."""
	statement = select(User)

	# Los filtros se agregan solo cuando el cliente los envia.
	if role is not None:
		statement = statement.where(User.role == role)

	if is_active is not None:
		statement = statement.where(User.is_active == is_active)

	# La ruta limita order_by a estas dos opciones mediante Literal.
	if order_by == "created_at":
		statement = statement.order_by(User.created_at)
	else:
		statement = statement.order_by(User.name)

	return list(db.scalars(statement).all())


def create_user(db: Session, user_data: UserCreate) -> User:
	"""Convierte el schema en ORM, guarda y refresca el usuario."""
	user = User(**user_data.model_dump())
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
	"""Reemplaza todos los campos editables de un usuario."""
	for field, value in user_data.model_dump().items():
		setattr(user, field, value)

	db.commit()
	db.refresh(user)
	return user


def patch_user(db: Session, user: User, user_data: UserPatch) -> User:
	"""Actualiza solo los campos enviados en la solicitud PATCH."""
	# exclude_unset evita modificar campos que el cliente no incluyo.
	changes = user_data.model_dump(exclude_unset=True, exclude_none=True)

	for field, value in changes.items():
		setattr(user, field, value)

	db.commit()
	db.refresh(user)
	return user


def delete_user(db: Session, user: User) -> None:
	"""Elimina un usuario y confirma la transaccion."""
	db.delete(user)
	db.commit()

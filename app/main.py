from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models.user_model import User
from app.routes.user_routes import router as user_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="device_systems",
    description="API de gestión de usuarios con FastAPI y SQLAlchemy",
    version="1.0.0"
)


app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": "device_systems funcionando correctamente"
    }
from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models.user_model import User

Base.metadata.create_all(bind=engine)

app=FastAPI (
    title="device_systems",
    description="API de gestion de usuarios con FastAPI y SQLAlchemy"
    version="1.0.0"

)

@app.get("/")
def root():
    return{
        "message":"devide"
    }
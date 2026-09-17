from fastapi import FastAPI

from app.models.user_model import User
from app.models.device_model import Device
from app.models.loan_model import Loan

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import related_router as loan_related_router
from app.routes.loan_routes import router as loan_router


app = FastAPI(
    title="device_systems",
    description="API de gestión de usuarios, dispositivos y préstamos con FastAPI y SQLAlchemy",
    version="1.0.0"
)


app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)
app.include_router(loan_related_router)


@app.get("/")
def root():
    return {
        "message": "device_systems funcionando correctamente"
    }
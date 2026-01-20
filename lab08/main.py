from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from lab_fastapi.db import engine
from lab_fastapi.models import Base
from lab_fastapi.routers import auth, orders

app = FastAPI(title="Lab FastAPI Orders")

# CORS básico (para front local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas (para el lab; en real usarías Alembic)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(orders.router)

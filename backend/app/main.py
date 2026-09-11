from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db, Base, engine
from app.api import auth, usuarios

# Se importan los modelos para que SQLAlchemy los registre en Base.metadata
from app.models import rol, usuario  # noqa: F401

app = FastAPI(
    title="Veterinaria API",
    description="Sistema de gestión para una veterinaria - Proyecto académico",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    # Crea las tablas si no existen. Válido para desarrollo;
    # en Fase 8 (pruebas y despliegue) esto se migra a Alembic.
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    """
    Endpoint raíz. Sirve únicamente para verificar que el backend
    está vivo y respondiendo correctamente.
    """
    return {
        "mensaje": "Veterinaria API funcionando correctamente",
        "estado": "ok",
    }


@app.get("/health")
def health_check():
    """
    Endpoint de salud (health check) básico, sin tocar la base de datos.
    """
    return {"status": "healthy"}


@app.get("/health/db")
def health_check_db(db: Session = Depends(get_db)):
    """
    Endpoint temporal para verificar que el backend puede
    conectarse y ejecutar consultas reales contra PostgreSQL.
    """
    resultado = db.execute(text("SELECT 1")).scalar()
    return {"database": "connected", "resultado": resultado}


app.include_router(auth.router)
app.include_router(usuarios.router)
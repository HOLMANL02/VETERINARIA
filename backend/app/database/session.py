from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# Motor de conexión: administra el "pool" de conexiones físicas hacia PostgreSQL.
engine = create_engine(settings.DATABASE_URL)

# Fábrica de sesiones: cada request del API abrirá y cerrará su propia sesión.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredarán TODOS los modelos (Usuario, Cliente, Mascota, etc.)
# Esto es Herencia aplicada de forma central: cada modelo hereda de Base
# y automáticamente queda registrado para la creación de tablas.
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos para usar como dependencia
    de FastAPI (Inyección de Dependencias).

    Cada endpoint que necesite hablarle a la BD recibirá una sesión
    nueva, y esta función garantiza que siempre se cierre correctamente,
    incluso si ocurre un error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
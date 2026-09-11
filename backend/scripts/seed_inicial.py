"""
Ejecutar UNA vez para poblar los roles básicos y crear el primer administrador.

Uso (dentro del contenedor backend, WORKDIR ya es /app):
    docker compose exec backend python scripts/seed_inicial.py
"""
import sys
import os

# Aseguramos que /app (donde vive el paquete "app") esté en el sys.path,
# sin importar si el script se invoca como "scripts/seed_inicial.py"
# o desde otra carpeta.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal, Base, engine
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.security.password import hash_password

ROLES = ["administrador", "veterinario", "recepcionista", "auxiliar", "caja", "cliente"]

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    for nombre in ROLES:
        if not db.query(Rol).filter(Rol.nombre == nombre).first():
            db.add(Rol(nombre=nombre))
    db.commit()

    admin_rol = db.query(Rol).filter(Rol.nombre == "administrador").first()
    if not db.query(Usuario).filter(Usuario.correo == "admin@veterinaria.com").first():
        db.add(Usuario(
            nombre="Administrador",
            correo="admin@veterinaria.com",
            password_hash=hash_password("CambiarEsta123!"),
            rol_id=admin_rol.id,
        ))
        db.commit()
        print("Usuario admin creado: admin@veterinaria.com / CambiarEsta123!  (cámbiala ya)")
    else:
        print("El usuario admin ya existía, no se modificó.")
finally:
    db.close()

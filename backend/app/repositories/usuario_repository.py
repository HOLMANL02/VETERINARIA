"""
Repositorio de Usuario: única capa que ejecuta consultas contra PostgreSQL
para esta entidad. Los services nunca importan SQLAlchemy directamente.
"""
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.security.password import hash_password


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_correo(self, correo: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.correo == correo).first()

    def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        return self.db.get(Usuario, usuario_id)

    def listar(self) -> list[Usuario]:
        return self.db.query(Usuario).all()

    def crear(self, datos: UsuarioCreate) -> Usuario:
        usuario = Usuario(
            nombre=datos.nombre,
            correo=datos.correo,
            password_hash=hash_password(datos.password),
            rol_id=datos.rol_id,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

from sqlalchemy.orm import Session

from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate
from app.models.usuario import Usuario
from app.services.exceptions import CorreoYaRegistradoError


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def crear_usuario(self, datos: UsuarioCreate) -> Usuario:
        if self.repo.obtener_por_correo(datos.correo) is not None:
            raise CorreoYaRegistradoError()
        return self.repo.crear(datos)

    def listar_usuarios(self) -> list[Usuario]:
        return self.repo.listar()

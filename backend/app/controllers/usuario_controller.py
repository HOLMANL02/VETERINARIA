from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.services.usuario_service import UsuarioService
from app.services.exceptions import CorreoYaRegistradoError


class UsuarioController:
    def __init__(self, db: Session):
        self.service = UsuarioService(db)

    def crear(self, datos: UsuarioCreate) -> UsuarioOut:
        try:
            usuario = self.service.crear_usuario(datos)
        except CorreoYaRegistradoError:
            raise HTTPException(status.HTTP_409_CONFLICT, "Ese correo ya está registrado")
        return UsuarioOut.model_validate(usuario)

    def listar(self) -> list[UsuarioOut]:
        return [UsuarioOut.model_validate(u) for u in self.service.listar_usuarios()]

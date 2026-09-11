"""
Servicio de autenticación: valida credenciales, valida que el usuario esté
activo (sección 16 del documento) y emite los tokens JWT.
"""
from sqlalchemy.orm import Session

from app.repositories.usuario_repository import UsuarioRepository
from app.security.password import verify_password
from app.security.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.exceptions import (
    CredencialesInvalidasError,
    UsuarioInactivoError,
    TokenInvalidoError,
)


class AuthService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def login(self, datos: LoginRequest) -> TokenResponse:
        usuario = self.repo.obtener_por_correo(datos.correo)
        if usuario is None or not verify_password(datos.password, usuario.password_hash):
            raise CredencialesInvalidasError()

        if not usuario.esta_activo():
            raise UsuarioInactivoError()

        access = create_access_token(usuario.id, usuario.rol.nombre)
        refresh = create_refresh_token(usuario.id)
        return TokenResponse(access_token=access, refresh_token=refresh)

    def refrescar(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if payload is None or payload.get("type") != "refresh":
            raise TokenInvalidoError()

        usuario = self.repo.obtener_por_id(int(payload["sub"]))
        if usuario is None or not usuario.esta_activo():
            raise TokenInvalidoError()

        access = create_access_token(usuario.id, usuario.rol.nombre)
        nuevo_refresh = create_refresh_token(usuario.id)
        return TokenResponse(access_token=access, refresh_token=nuevo_refresh)

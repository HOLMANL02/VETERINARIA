from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.services.auth_service import AuthService
from app.services.exceptions import (
    CredencialesInvalidasError,
    UsuarioInactivoError,
    TokenInvalidoError,
)


class AuthController:
    def __init__(self, db: Session):
        self.service = AuthService(db)

    def login(self, datos: LoginRequest) -> TokenResponse:
        try:
            return self.service.login(datos)
        except CredencialesInvalidasError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Correo o contraseña incorrectos")
        except UsuarioInactivoError:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "El usuario está desactivado")

    def refrescar(self, datos: RefreshRequest) -> TokenResponse:
        try:
            return self.service.refrescar(datos.refresh_token)
        except TokenInvalidoError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token inválido o expirado")

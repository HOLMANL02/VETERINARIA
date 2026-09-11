"""
Dependencias de FastAPI para proteger endpoints.
RNF-02: los permisos se validan en el backend, no solo en la interfaz.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.security.jwt_handler import decode_token
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credenciales_invalidas

    usuario = UsuarioRepository(db).obtener_por_id(int(payload["sub"]))
    if usuario is None or not usuario.esta_activo():
        raise credenciales_invalidas

    return usuario


def require_roles(*roles_permitidos: str):
    """Factory de dependencia: valida que el rol del usuario esté autorizado."""

    def verificador(usuario: Usuario = Depends(get_current_user)) -> Usuario:
        if usuario.rol.nombre not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción",
            )
        return usuario

    return verificador

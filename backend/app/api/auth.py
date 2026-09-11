from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.usuario import UsuarioOut
from app.controllers.auth_controller import AuthController
from app.security.dependencies import get_current_user
from app.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    return AuthController(db).login(datos)


@router.post("/refresh", response_model=TokenResponse)
def refresh(datos: RefreshRequest, db: Session = Depends(get_db)):
    return AuthController(db).refrescar(datos)


@router.get("/me", response_model=UsuarioOut)
def obtener_usuario_actual(usuario: Usuario = Depends(get_current_user)):
    return usuario
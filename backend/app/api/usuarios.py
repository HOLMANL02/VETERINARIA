from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioOut
from app.controllers.usuario_controller import UsuarioController
from app.security.dependencies import require_roles

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.post("", response_model=UsuarioOut, dependencies=[Depends(require_roles("administrador"))])
def crear_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioController(db).crear(datos)


@router.get("", response_model=list[UsuarioOut], dependencies=[Depends(require_roles("administrador"))])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioController(db).listar()

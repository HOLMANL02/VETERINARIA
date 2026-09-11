from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.rol import Rol
from app.schemas.rol import RolOut
from app.security.dependencies import require_roles

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=list[RolOut], dependencies=[Depends(require_roles("administrador"))])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(Rol).order_by(Rol.nombre).all()
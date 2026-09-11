from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.controllers.cliente_controller import ClienteController
from app.security.dependencies import require_roles

router = APIRouter(prefix="/clients", tags=["Clientes"])

PUEDE_GESTIONAR_CLIENTES = require_roles("administrador", "recepcionista")


@router.post("", response_model=ClienteOut, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(PUEDE_GESTIONAR_CLIENTES)])
def crear_cliente(datos: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteController(db).crear(datos)


@router.get("", response_model=list[ClienteOut],
            dependencies=[Depends(PUEDE_GESTIONAR_CLIENTES)])
def listar_clientes(buscar: str | None = None, db: Session = Depends(get_db)):
    return ClienteController(db).listar(buscar)


@router.get("/{cliente_id}", response_model=ClienteOut,
            dependencies=[Depends(PUEDE_GESTIONAR_CLIENTES)])
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return ClienteController(db).obtener(cliente_id)


@router.put("/{cliente_id}", response_model=ClienteOut,
            dependencies=[Depends(PUEDE_GESTIONAR_CLIENTES)])
def actualizar_cliente(cliente_id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):
    return ClienteController(db).actualizar(cliente_id, datos)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(PUEDE_GESTIONAR_CLIENTES)])
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    ClienteController(db).eliminar(cliente_id)
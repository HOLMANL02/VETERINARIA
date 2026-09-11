from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.services.cliente_service import ClienteService
from app.services.exceptions import ClienteNoEncontradoError, ClienteConMascotasError


class ClienteController:
    def __init__(self, db: Session):
        self.service = ClienteService(db)

    def crear(self, datos: ClienteCreate) -> ClienteOut:
        cliente = self.service.crear_cliente(datos)
        return ClienteOut.model_validate(cliente)

    def listar(self, buscar: str | None) -> list[ClienteOut]:
        return [ClienteOut.model_validate(c) for c in self.service.listar_clientes(buscar)]

    def obtener(self, cliente_id: int) -> ClienteOut:
        try:
            cliente = self.service.obtener_cliente(cliente_id)
        except ClienteNoEncontradoError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
        return ClienteOut.model_validate(cliente)

    def actualizar(self, cliente_id: int, datos: ClienteUpdate) -> ClienteOut:
        try:
            cliente = self.service.actualizar_cliente(cliente_id, datos)
        except ClienteNoEncontradoError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
        return ClienteOut.model_validate(cliente)

    def eliminar(self, cliente_id: int) -> None:
        try:
            self.service.eliminar_cliente(cliente_id)
        except ClienteNoEncontradoError:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
        except ClienteConMascotasError:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "No se puede eliminar: el cliente tiene mascotas asociadas",
            )
from sqlalchemy.orm import Session

from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.services.exceptions import ClienteNoEncontradoError, ClienteConMascotasError


class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def crear_cliente(self, datos: ClienteCreate) -> Cliente:
        return self.repo.crear(datos)

    def listar_clientes(self, buscar: str | None = None) -> list[Cliente]:
        return self.repo.listar(buscar)

    def obtener_cliente(self, cliente_id: int) -> Cliente:
        cliente = self.repo.obtener_por_id(cliente_id)
        if cliente is None:
            raise ClienteNoEncontradoError()
        return cliente

    def actualizar_cliente(self, cliente_id: int, datos: ClienteUpdate) -> Cliente:
        cliente = self.obtener_cliente(cliente_id)
        return self.repo.actualizar(cliente, datos)

    def eliminar_cliente(self, cliente_id: int) -> None:
        cliente = self.obtener_cliente(cliente_id)
        if self.repo.tiene_mascotas(cliente):
            raise ClienteConMascotasError()
        self.repo.eliminar(cliente)
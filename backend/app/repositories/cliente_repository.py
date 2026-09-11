"""
Repositorio de Cliente: única capa que ejecuta consultas contra PostgreSQL
para esta entidad. Los services nunca importan SQLAlchemy directamente.
"""
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, cliente_id: int) -> Cliente | None:
        return self.db.get(Cliente, cliente_id)

    def listar(self, buscar: str | None = None) -> list[Cliente]:
        query = self.db.query(Cliente)
        if buscar:
            query = query.filter(Cliente.nombres.ilike(f"%{buscar}%"))
        return query.order_by(Cliente.nombres).all()

    def crear(self, datos: ClienteCreate) -> Cliente:
        cliente = Cliente(**datos.model_dump())
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def actualizar(self, cliente: Cliente, datos: ClienteUpdate) -> Cliente:
        cambios = datos.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(cliente, campo, valor)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def tiene_mascotas(self, cliente: Cliente) -> bool:
        return len(cliente.mascotas) > 0

    def eliminar(self, cliente: Cliente) -> None:
        self.db.delete(cliente)
        self.db.commit()
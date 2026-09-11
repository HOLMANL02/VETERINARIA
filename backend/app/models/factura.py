from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Factura(Base):
    """
    Entidad de dominio Factura (sección 10): documento de cobro.
    Regla de negocio (sección 16): las facturas conservan sus detalles
    (precio guardado en detalle_factura) aunque cambien luego los
    precios del catálogo de servicios/medicamentos.
    """
    __tablename__ = "facturas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    impuestos: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="pendiente", nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="facturas")
    detalles: Mapped[list["DetalleFactura"]] = relationship(back_populates="factura")
    pagos: Mapped[list["Pago"]] = relationship(back_populates="factura")

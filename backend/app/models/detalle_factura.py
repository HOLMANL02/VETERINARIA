from typing import Optional

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class DetalleFactura(Base):
    """
    Entidad de dominio DetalleFactura (sección 9): línea de una factura,
    referenciando un servicio o un medicamento (uno de los dos, no ambos).
    """
    __tablename__ = "detalle_factura"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    factura_id: Mapped[int] = mapped_column(ForeignKey("facturas.id"), nullable=False)
    servicio_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("servicios.id"), nullable=True
    )
    medicamento_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("medicamentos.id"), nullable=True
    )
    cantidad: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    factura: Mapped["Factura"] = relationship(back_populates="detalles")
    servicio: Mapped[Optional["Servicio"]] = relationship(back_populates="detalles")

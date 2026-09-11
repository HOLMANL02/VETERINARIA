from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Pago(Base):
    """
    Entidad de dominio Pago (sección 10): registro de pago de una factura.
    """
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    factura_id: Mapped[int] = mapped_column(ForeignKey("facturas.id"), nullable=False)
    metodo: Mapped[str] = mapped_column(String(30), nullable=False)  # efectivo, tarjeta, etc.
    valor: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="confirmado", nullable=False)

    factura: Mapped["Factura"] = relationship(back_populates="pagos")

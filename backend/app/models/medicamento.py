from typing import Optional

from sqlalchemy import String, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.mixins import TimestampMixin


class Medicamento(Base, TimestampMixin):
    """
    Entidad de dominio Medicamento (sección 10): producto y existencia
    dentro del inventario (RF-13).
    """
    __tablename__ = "medicamentos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    stock_minimo: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)

    tratamientos: Mapped[list["Tratamiento"]] = relationship(back_populates="medicamento")
    movimientos: Mapped[list["MovimientoInventario"]] = relationship(
        back_populates="medicamento"
    )

    def stock_bajo(self) -> bool:
        """Regla de negocio (RF-14): alerta cuando el stock llega al mínimo."""
        return self.stock <= self.stock_minimo

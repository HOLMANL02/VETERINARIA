from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class MovimientoInventario(Base):
    """
    Entidad de dominio MovimientoInventario (sección 10): entrada,
    salida o ajuste de inventario de medicamentos (RF-13).
    """
    __tablename__ = "movimientos_inventario"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    medicamento_id: Mapped[int] = mapped_column(
        ForeignKey("medicamentos.id"), nullable=False
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)  # entrada | salida | ajuste
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    lote: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)

    medicamento: Mapped["Medicamento"] = relationship(back_populates="movimientos")

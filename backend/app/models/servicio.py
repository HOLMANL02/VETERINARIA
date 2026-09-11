from typing import Optional

from sqlalchemy import String, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Servicio(Base):
    """
    Entidad de dominio Servicio (sección 9): servicio facturable
    (consulta, procedimiento, etc.), usado en detalle_factura.
    """
    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="activo", nullable=False)

    detalles: Mapped[list["DetalleFactura"]] = relationship(back_populates="servicio")

from datetime import date
from typing import Optional

from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Vacuna(Base):
    """
    Entidad de dominio Vacuna (sección 10): registro de vacunación (RF-11).
    """
    __tablename__ = "vacunas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    mascota_id: Mapped[int] = mapped_column(ForeignKey("mascotas.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_aplicacion: Mapped[date] = mapped_column(Date, nullable=False)
    proxima_dosis: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    lote: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    mascota: Mapped["Mascota"] = relationship(back_populates="vacunas")

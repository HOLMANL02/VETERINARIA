from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.mixins import TimestampMixin


class HistoriaClinica(Base, TimestampMixin):
    """
    Entidad de dominio HistoriaClinica (sección 10): historial médico
    de una mascota. Relación 1 a 1 con Mascota (RF-09).
    Solo personal autorizado puede modificarla (regla de negocio, sección 16).
    """
    __tablename__ = "historias_clinicas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    mascota_id: Mapped[int] = mapped_column(
        ForeignKey("mascotas.id"), unique=True, nullable=False
    )
    fecha_apertura: Mapped[date] = mapped_column(Date, nullable=False)
    antecedentes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    mascota: Mapped["Mascota"] = relationship(back_populates="historia_clinica")
    consultas: Mapped[list["Consulta"]] = relationship(back_populates="historia")

from datetime import date
from typing import Optional

from sqlalchemy import String, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.mixins import TimestampMixin


class Mascota(Base, TimestampMixin):
    """
    Entidad de dominio Mascota (sección 10): paciente veterinario y sus datos.
    Regla de negocio (sección 16): una mascota siempre debe estar
    asociada a un cliente/responsable (cliente_id no es nulo).
    """
    __tablename__ = "mascotas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    especie: Mapped[str] = mapped_column(String(50), nullable=False)
    raza: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    sexo: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    peso: Mapped[Optional[float]] = mapped_column(Numeric(6, 2), nullable=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    cliente: Mapped["Cliente"] = relationship(back_populates="mascotas")
    historia_clinica: Mapped[Optional["HistoriaClinica"]] = relationship(
        back_populates="mascota", uselist=False
    )
    citas: Mapped[list["Cita"]] = relationship(back_populates="mascota")
    vacunas: Mapped[list["Vacuna"]] = relationship(back_populates="mascota")

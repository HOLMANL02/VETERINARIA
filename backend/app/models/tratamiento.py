from typing import Optional

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Tratamiento(Base):
    """
    Entidad de dominio Tratamiento (sección 10): medicamento, dosis
    y plan terapéutico asociado a una consulta (RF-12).
    """
    __tablename__ = "tratamientos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    consulta_id: Mapped[int] = mapped_column(ForeignKey("consultas.id"), nullable=False)
    medicamento_id: Mapped[int] = mapped_column(
        ForeignKey("medicamentos.id"), nullable=False
    )
    dosis: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    frecuencia: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    duracion: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    indicaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    consulta: Mapped["Consulta"] = relationship(back_populates="tratamientos")
    medicamento: Mapped["Medicamento"] = relationship(back_populates="tratamientos")

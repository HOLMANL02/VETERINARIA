from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Consulta(Base):
    """
    Entidad de dominio Consulta (sección 10): atención realizada por
    un veterinario, asociada siempre a una historia clínica (RF-10).
    """
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    historia_id: Mapped[int] = mapped_column(
        ForeignKey("historias_clinicas.id"), nullable=False
    )
    veterinario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    examen: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    diagnostico: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tratamiento: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    historia: Mapped["HistoriaClinica"] = relationship(back_populates="consultas")
    tratamientos: Mapped[list["Tratamiento"]] = relationship(back_populates="consulta")

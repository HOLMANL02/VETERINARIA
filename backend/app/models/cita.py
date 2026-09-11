from datetime import datetime
from typing import Optional

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Cita(Base):
    """
    Entidad de dominio Cita (sección 10): programación y estado de una atención.
    Regla de negocio (sección 16): no se debe permitir una cita activa en el
    mismo horario para el mismo veterinario (se valida en services/, no aquí).
    """
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    mascota_id: Mapped[int] = mapped_column(ForeignKey("mascotas.id"), nullable=False)
    veterinario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    motivo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="programada", nullable=False)
    # estados esperados: programada, confirmada, atendida, cancelada

    mascota: Mapped["Mascota"] = relationship(back_populates="citas")

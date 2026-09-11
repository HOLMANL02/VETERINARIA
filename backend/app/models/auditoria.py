from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, DateTime, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Auditoria(Base):
    """
    Entidad de dominio Auditoria (sección 10): registro de acciones
    relevantes del sistema (RF-18 / RNF-10).
    """
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fecha_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    detalle: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

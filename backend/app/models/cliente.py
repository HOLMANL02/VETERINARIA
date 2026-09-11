from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.mixins import TimestampMixin


class Cliente(Base, TimestampMixin):
    """
    Entidad de dominio Cliente (sección 10 del documento):
    propietario/responsable de una o más mascotas.
    """
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )  # opcional: solo si el cliente también tiene acceso al portal (rol "cliente")
    nombres: Mapped[str] = mapped_column(String(150), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    correo: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    direccion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    mascotas: Mapped[list["Mascota"]] = relationship(back_populates="cliente")
    facturas: Mapped[list["Factura"]] = relationship(back_populates="cliente")

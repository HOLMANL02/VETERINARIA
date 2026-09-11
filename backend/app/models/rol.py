from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class Rol(Base):
    """
    Rol del sistema (administrador, veterinario, recepcionista, auxiliar,
    caja, cliente) según sección 6 del documento de requerimientos.
    """
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="rol")

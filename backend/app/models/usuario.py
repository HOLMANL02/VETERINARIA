from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base
from app.models.mixins import TimestampMixin


class Usuario(Base, TimestampMixin):
    """
    Entidad de dominio Usuario.
    Responsabilidad (sección 10 del documento): autenticación, estado y datos básicos.
    La contraseña NUNCA se guarda en texto plano (RNF-01): solo su hash.
    """
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)  # activo/inactivo (RF-03)

    rol: Mapped["Rol"] = relationship(back_populates="usuarios")

    def esta_activo(self) -> bool:
        """Un usuario desactivado no puede iniciar sesión (regla de negocio, sección 16)."""
        return self.estado

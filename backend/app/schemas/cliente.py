from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class ClienteCreate(BaseModel):
    """RF-05: datos requeridos para registrar un cliente/propietario."""

    nombres: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = None
    usuario_id: Optional[int] = None  # solo si el cliente también accede al portal (rol "cliente")


class ClienteUpdate(BaseModel):
    """Todos los campos opcionales: permite actualizar solo lo que cambió."""

    nombres: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = None


class ClienteOut(BaseModel):
    id: int
    nombres: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    direccion: Optional[str] = None
    usuario_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
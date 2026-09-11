from pydantic import BaseModel, EmailStr, ConfigDict


class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    password: str
    rol_id: int


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol_id: int
    estado: bool

    model_config = ConfigDict(from_attributes=True)

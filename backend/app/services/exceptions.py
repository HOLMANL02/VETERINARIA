class CredencialesInvalidasError(Exception):
    """Correo no existe o contraseña incorrecta."""


class UsuarioInactivoError(Exception):
    """El usuario está desactivado y no puede iniciar sesión (regla de negocio)."""


class CorreoYaRegistradoError(Exception):
    """Ya existe un usuario con ese correo."""


class TokenInvalidoError(Exception):
    """El token JWT es inválido, expiró o no es del tipo esperado."""

class ClienteNoEncontradoError(Exception):
    """No existe un cliente con el id solicitado."""


class ClienteConMascotasError(Exception):
    """No se puede eliminar un cliente que todavía tiene mascotas asociadas (RF-05)."""

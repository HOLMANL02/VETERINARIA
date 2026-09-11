from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Clase que centraliza y valida toda la configuración de la aplicación.

    Al heredar de BaseSettings (Pydantic), automáticamente lee las
    variables de entorno definidas en el archivo .env y las valida
    con tipos de datos, evitando errores silenciosos por variables
    mal escritas o faltantes.
    """

    # Base de datos
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # JWT (lo usaremos en la Fase de autenticación)
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    @property
    def DATABASE_URL(self) -> str:
        """
        Construye la cadena de conexión que SQLAlchemy necesita,
        en lugar de tenerla escrita manualmente en otro lugar.
        """
        return (
            f"postgresql+psycopg2://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"


# Instancia única (patrón Singleton simple) que se importa
# desde cualquier parte de la aplicación.
settings = Settings()
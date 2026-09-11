# Imagen base: Python liviano (slim reduce tamaño y superficie de ataque)
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y fuerza logs sin buffer (mejor para ver logs en Docker)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos primero requirements.txt (aprovecha la cache de Docker si el código cambia pero las dependencias no)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código del backend
COPY . .

# Puerto interno donde correrá FastAPI (Nginx hablará con este puerto, NO el navegador)
EXPOSE 8000

# Comando por defecto al iniciar el contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
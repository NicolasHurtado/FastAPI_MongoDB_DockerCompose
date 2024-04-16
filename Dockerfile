FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Copia el archivo requirements.txt al directorio /app
COPY ./src/requirements.txt /app/requirements.txt

# Instala las dependencias desde requirements.txt
RUN pip install --upgrade pip --no-cache-dir -r /app/requirements.txt


COPY ./src /app

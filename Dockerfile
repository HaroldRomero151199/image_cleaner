# ✅ Usa una imagen oficial, estable y más compatible con rembg (3.10 recomendado)
FROM python:3.10-slim

# ✅ Define el directorio de trabajo
WORKDIR /app

# ✅ Instala solo las dependencias necesarias para rembg (onnxruntime necesita libgl1)
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ✅ Copia e instala requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ✅ Copia todo el código de la app
COPY . .

# ✅ Asegura que exista la carpeta `static` (aunque puedes dejar que el código la cree dinámicamente si prefieres)
RUN mkdir -p /app/static

# ✅ Expón el puerto (FastAPI por defecto es 8000)
EXPOSE 8000

# ✅ Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


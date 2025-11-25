# Dockerfile con soporte GPU
# Usa una imagen base de NVIDIA con CUDA 12.x y cuDNN
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# Evita que Python genere archivos .pyc y habilita logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala Python 3.10 y dependencias del sistema
# libgl1-mesa-glx es necesario para opencv-python (usado por rembg)
RUN apt-get update && \
    apt-get install -y python3.10 python3.10-dev python3-pip libgl1-mesa-glx && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia e instala requerimientos primero para aprovechar cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y onnxruntime

# Copia todo el código de la app
COPY . .

# Crea la carpeta static si no existe
RUN mkdir -p /app/static

# Expón el puerto
EXPOSE 8000

# Comando para iniciar la aplicación
# Ejecuta desde /app, llamando al módulo app.main
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

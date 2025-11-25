# Product Image Cleaner

Servicio web FastAPI para subir imágenes de productos y quitar el fondo automáticamente usando rembg.

## Características

- Subir imágenes de productos
- Quitar fondo automáticamente
- API REST para listar y descargar imágenes
- Soporte para GPU (más rápido)

## Instalación y Uso (Docker)

Este proyecto está diseñado para ejecutarse con Docker. Por defecto, intenta utilizar la GPU para un procesamiento óptimo.

### Prerrequisitos

1.  **Docker** y **Docker Compose** instalados.
2.  **(Solo para modo GPU)**: Drivers de NVIDIA y [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) instalados en el host.

### Pasos para ejecutar

1.  **Construir y arrancar el servicio:**
    ```bash
    docker-compose up --build
    ```

2.  **Verificar funcionamiento:**
    - Documentación API: http://localhost:8000/docs
    - Estado del hardware: http://localhost:8000/ (debería mostrar `"using_gpu": true` si la GPU está activa)

### ¿Tienes problemas o no tienes GPU? (Modo CPU)

El archivo `docker-compose.yml` está configurado por defecto para **exigir** una GPU NVIDIA. Si no tienes una GPU o no tienes configurado el NVIDIA Container Toolkit, el contenedor no iniciará.

Para correrlo solo con **CPU**, edita el archivo `docker-compose.yml` y **comenta o elimina** la sección `deploy`:

```yaml
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
```

## Uso de la API

1.  Usa el endpoint `/upload/{ean}` para subir imágenes.
2.  Las imágenes procesadas se guardarán en `/static/{ean}/output/`.

## Estructura

- `app/` - Código de la aplicación
- `static/` - Imágenes subidas y procesadas
- `Dockerfile` - Imagen Docker (preparada para CUDA 12.x)
- `docker-compose.yml` - Configuración del servicio

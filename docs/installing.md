# Guía de Instalación

Sigue estos pasos para instalar y configurar el proyecto API WooCommerce:

## 1. Requisitos previos
- Python 3.10 o superior
- Acceso a una tienda WooCommerce (con claves API)
- Acceso a la terminal de Windows (PowerShell)
- No se requiere configuración de MySQL, ya que el almacenamiento local es solo mock

## 2. Clonar el repositorio
```
git clone https://github.com/AgustinMadygraf/api-woocommerce.git
```

## 3. Crear y activar entorno virtual
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 4. Instalar dependencias
```
pip install -r requirements.txt
```

## 5. Configurar variables de entorno
Copia el archivo `.env.example` y renómbralo a `.env`. Edita los valores según tu tienda WooCommerce:
```
URL=https://tu-tienda.com
CK=tu_consumer_key
CS=tu_consumer_secret
```

## 6. Ejecutar la API o CLI
- Para iniciar el servidor FastAPI:
  ```
  .\run.bat
  ```
- Para iniciar la interfaz CLI:
  ```
  .\run_cli.bat
  ```

## 7. Probar endpoints y comandos
Consulta la [API Documentation](API_documentation.md) para ejemplos de uso y endpoints disponibles.

## Notas adicionales
- Si tienes problemas con dependencias, revisa la versión de Python y el archivo `requirements.txt`.
- El sistema está diseñado para productos variables y sus variaciones.
- Los endpoints locales son mocks y no requieren base de datos.
- Puedes modificar el archivo `.env` para cambiar la configuración sin reiniciar el entorno.
- La CLI requiere Windows por dependencias específicas.

¿Necesitas ayuda? Revisa la documentación o contacta al autor del repositorio.
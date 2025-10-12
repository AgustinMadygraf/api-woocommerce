# Arquitectura del Proyecto API WooCommerce

Este documento describe la arquitectura y los principios de diseño aplicados en el proyecto.

## Principios

- **Clean Architecture:** Separación clara entre dominio, casos de uso, infraestructura y presentación.
- **SOLID:** Uso de interfaces (gateways), inyección de dependencias y entidades desacopladas.
- **Extensibilidad:** Permite agregar nuevas fuentes de datos, entidades y casos de uso sin modificar el núcleo.

## Estructura de Carpetas

- **src/entities/**  
  Modelos de dominio: representan productos, variaciones y estado del sistema.

- **src/use_cases/**  
  Casos de uso: lógica de negocio para obtener productos, variaciones y estado.

- **src/interface_adapter/gateways/**  
  Gateways: interfaces para acceso a datos (WooCommerce, LocalStore).

- **src/interface_adapter/presenters/**  
  Presentadores: transforman entidades en datos listos para la UI o API.

- **src/interface_adapter/controllers/**  
  Controladores: orquestan la interacción entre casos de uso, gateways y presentadores.

- **src/infrastructure/fastapi/**  
  Endpoints HTTP, integración con FastAPI.

- **src/infrastructure/cli/**  
  Interfaz de línea de comandos estilo AS400 IBM.

- **src/infrastructure/woocommerce/**  
  Integración directa con la API WooCommerce.

- **src/shared/**  
  Configuración, logging y utilidades comunes.

## Flujo de Datos

1. **Entrada:**  
   - FastAPI recibe requests HTTP.
   - CLI recibe comandos del usuario.

2. **Procesamiento:**  
   - Controladores llaman a casos de uso.
   - Casos de uso usan gateways para acceder a datos.

3. **Salida:**  
   - Presentadores transforman entidades en respuestas para la UI/API.

## Extender el Sistema

- Para agregar una nueva entidad:  
  Crear el modelo en `src/entities/` y el caso de uso en `src/use_cases/`.

- Para soportar una nueva fuente de datos:  
  Implementar un gateway en `src/interface_adapter/gateways/` y su cliente en `src/infrastructure/`.

- Para nuevos endpoints o comandos:  
  Crear el controlador y presentador correspondiente.

## Notas

- Los endpoints locales son mocks para pruebas/desarrollo, no persisten datos ni requieren base de datos.
- La integración con WooCommerce usa autenticación básica y la API v3.
- El sistema está preparado para paginación y manejo de errores en endpoints WooCommerce.
- No existen tests automatizados; se recomienda crear una carpeta `tests/` para futuras pruebas.
- La CLI requiere entorno Windows por dependencias específicas.

---

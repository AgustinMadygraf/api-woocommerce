# Integración API WooCommerce

Este proyecto proporciona una API modular y una interfaz CLI para interactuar con productos variables de WooCommerce y sus variaciones, siguiendo principios de Clean Architecture. Soporta tanto datos locales simulados (mock, sin persistencia real) como integración con la API de WooCommerce.

## Características
- Endpoints FastAPI para WooCommerce y datos locales simulados (mock)
- Interfaz CLI con estilo AS400
- Separación de responsabilidades: entidades, casos de uso, gateways, presentadores, controladores
- Configurable mediante archivo `.env` (ver `.env.example`)
- Paginación y manejo de errores en endpoints WooCommerce
- Arquitectura extensible para nuevas entidades y casos de uso

## Limitaciones actuales
- Solo soporta productos variables y sus variaciones
- Los endpoints locales son mocks, no persisten datos ni requieren base de datos
- No hay autenticación ni seguridad en la API propia
- No existen tests automatizados
- Requiere entorno Windows para la CLI

## Estructura del Proyecto
```

  entities/           # Modelos de dominio (productos, variaciones, estado del sistema)
  infrastructure/     # Clientes API, CLI, servidores FastAPI, integración WooCommerce
  interface_adapter/  # Gateways, controladores, presentadores
  shared/             # Configuración, logging
  use_cases/          # Lógica de negocio
  docs/               # Documentación
```

## Instalación
Consulta la [Guía de Instalación](docs/installing.md) para instrucciones paso a paso sobre cómo configurar el entorno, instalar dependencias y configurar el proyecto.

## Uso
- Configura tu archivo `.env` basado en `.env.example`
- Usa `run.bat` o `run_cli.bat` para iniciar el servidor FastAPI o la CLI
- Los endpoints y comandos de la CLI están documentados en la documentación de la API

## Documentación
- [Documentación de la API](docs/API_documentation.md)
- [Guía de Instalación](docs/installing.md)
- [Arquitectura del Proyecto](docs/architecture.md)

## Configuración
Define tus credenciales de WooCommerce y la URL de la API en el archivo `.env`:
```
URL=https://tu-tienda-woocommerce.com
CK=tu_consumer_key
CS=tu_consumer_secret
```

## Notas
- El proyecto actualmente se enfoca en productos variables y sus variaciones
- Los endpoints locales proveen datos simulados para pruebas y desarrollo, sin persistencia real
- La integración con WooCommerce utiliza la API v3 y autenticación básica

## Licencia
MIT

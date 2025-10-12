# API Documentation

Este documento describe los endpoints expuestos por el adaptador FastAPI para WooCommerce y para el almacenamiento local.

## Endpoints

### 1. Obtener estado del sistema WooCommerce

**GET /api/wp-json/wc/v3/system_status**  
**POST /api/wp-json/wc/v3/system_status**

**Descripción:**
Devuelve el estado actual del sistema WooCommerce.

---

## Endpoints de Almacenamiento Local

Los endpoints locales replican la estructura de los endpoints WooCommerce, pero bajo el prefijo `/api/LocalStore/wc/v3/`. La estructura de datos devuelta es más simple y contiene solo los campos necesarios para la operación.

### Ejemplo de endpoints locales:

- **GET /api/LocalStore/wc/v3/products**
- **GET /api/LocalStore/wc/v3/products/{id}/variations**
- **GET /api/LocalStore/wc/v3/system_status**

### Estructura de datos devuelta (local):

#### Producto variable
```json
{
  "ID_producto_variable": int,
  "formato": string,
  "color": string,
  "gramaje": string,
  "stock": int,
  "ultima_actualizacion": string
}
```

#### Producto variaciones
```json
{
  "id_produto_variaciones": int,
  "id_producto_variable": int,
  "es_manijas": bool,
  "id_impresion": int,
  "precio_final": float,
  "ultima_actualizacion": string
}
```

#### Impresión
```json
{
  "id_impresión": int,
  "es_impresión": bool,
  "cant_colores": int,
  "es_cara_simple": bool
}
```

### Paginación
Los endpoints locales aceptan los mismos parámetros de paginación que la API WooCommerce (`per_page`, `page`).

### Errores
La especificación de errores para los endpoints locales está pendiente de definición.

---

## Notas
- Los endpoints locales están pensados para operaciones rápidas y simples, devolviendo solo los campos esenciales.
- La estructura de los endpoints y parámetros es idéntica a la API WooCommerce, pero la respuesta puede variar en los campos incluidos.

## Dudas no resueltas

- La estructura exacta puede variar según la configuración y plugins de WooCommerce.
- No se puede garantizar que todos los campos estén presentes en todas las instalaciones WooCommerce.

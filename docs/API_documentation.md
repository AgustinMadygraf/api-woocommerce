# API Documentation

Este documento describe los endpoints expuestos por el adaptador FastAPI para WooCommerce.

## Endpoints

### 1. Obtener estado del sistema WooCommerce

**GET /api/wp-json/wc/v3/system_status**  
**POST /api/wp-json/wc/v3/system_status**

**Descripción:**
Devuelve el estado del sistema WooCommerce, incluyendo información de entorno, versión y plugins.

**Respuesta de ejemplo:**
```json
{
  "home_url": "https://tutienda.com",
  "version": "6.0.0",
  "environment": {
    "php_version": "7.4.1",
    "wp_version": "5.8.2",
    "server_info": "Apache/2.4.41 (Win64)"
  },
  "raw_data": {
    "environment": { /* ... */ },
    "database": { /* ... */ },
    "active_plugins": [ /* ... */ ]
  }
}
```

**Errores:**
- 500: Error inesperado
- Código y mensaje de error de WooCommerce si la API responde con error

---

### 2. Obtener productos variables

**GET /api/wp-json/wc/v3/products?product_type=variable**

**Descripción:**
Devuelve una lista de productos variables de WooCommerce.

**Parámetros:**
- `product_type`: Debe ser "variable". Si se envía otro valor, responde con error 400.

**Respuesta de ejemplo:**
```json
[
  {
    "id": 773,
    "name": "Camiseta",
    "type": "variable",
    "status": "publish",
    "price": "19.99",
    "attributes": [
      {
        "id": 1,
        "name": "Color",
        "options": ["Rojo", "Azul"]
      }
    ],
    "variations": [1234, 1235]
    // ...otros campos estándar de WooCommerce...
  }
]
```

**Errores:**
- 400: Solo se soporta type=variable en este endpoint
- 500: Error inesperado

---

### 3. Obtener variaciones de un producto variable

**GET /api/wp-json/wc/v3/products/{product_id}/variations**

**Descripción:**
Devuelve una lista paginada de variaciones para un producto variable.

**Parámetros:**
- `product_id`: ID del producto variable
- `per_page`: (opcional, default 10, min 1, max 100) Cantidad de variaciones por página
- `page`: (opcional, default 1, min 1) Número de página

**Respuesta de ejemplo:**
```json
[
  {
    "id": 1234,
    "sku": "CAM-ROJO-S",
    "price": "19.99",
    "attributes": [
      { "id": 1, "name": "Color", "option": "Rojo" },
      { "id": 2, "name": "Talla", "option": "S" }
    ],
    "stock_status": "instock",
    "image": {
      "id": 456,
      "src": "https://tutienda.com/wp-content/uploads/2022/01/camiseta-rojo-s.jpg"
    }
    // ...otros campos estándar de WooCommerce...
  }
]
```

**Errores:**
- 500: Error inesperado
- Código y mensaje de error de WooCommerce si la API responde con error

---

## Notas generales

- Todos los endpoints devuelven la estructura JSON estándar de WooCommerce.
- Los errores tienen formato `{ "detail": mensaje }`.
- No se requiere autenticación adicional en FastAPI, solo las credenciales CK y CS configuradas en el entorno.
- El sistema está diseñado para WooCommerce API v3.
- Si faltan variables de entorno requeridas, se devuelve error 500.

## Dudas no resueltas

- La estructura exacta puede variar según la configuración y plugins de WooCommerce.
- No se puede garantizar que todos los campos estén presentes en todas las instalaciones WooCommerce.

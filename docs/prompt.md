Estoy trabajando en el desarrollo de software y quiero implementar la siguiente mejora técnica: 

[describe aquí la mejora técnica].

1. Si tenés dudas razonables sobre cómo implementarla, hacé preguntas aclaratorias y tratá de responderlas basándote en buenas prácticas, documentación oficial o experiencia previa.
2. Si tenés claridad suficiente, indicame de forma directa y precisa:
   - Qué archivos debo crear y/o modificar
   - Qué cambios debo realizar
   - Si es posible, explicá brevemente por qué esa es la mejor opción

Respondé como si fueras un desarrollador senior con criterio técnico.


---



Estoy trabajando en un proyecto de software en Python, con una interfaz tipo CLI similar a AS400-IBM, y necesito incorporar la siguiente funcionalidad:

[nueva funcionalidad]

Antes de implementar esta funcionalidad, realizá una auditoría técnica del proyecto (asumiendo que tenés acceso al código base y a su estructura) para evaluar si se están aplicando correctamente las siguientes prácticas de ingeniería de software:

- Clean Architecture
- Principios SOLID
- Patrones de diseño relevantes
- Programación orientada a objetos (POO)

Tu respuesta debe tener **dos secciones claramente diferenciadas**:

---

**1. Auditoría Técnica:**
- Señalá aciertos y desviaciones respecto a las buenas prácticas mencionadas.
- Comentá si el diseño actual favorece la mantenibilidad, extensibilidad y testabilidad.
- Detectá posibles violaciones a la separación de capas o responsabilidades.

---

**2. Lista de tareas (en orden de prioridad):**
- Primero, proponé tareas de **refactorización** necesarias para corregir problemas o mejorar la estructura del código **sin añadir nueva funcionalidad**.
- Luego, indicá tareas para **incorporar la nueva funcionalidad** de forma progresiva, sin romper el entorno productivo ni interrumpir funcionalidades existentes.

Para cada tarea, especificá:
- Qué archivo/s se deben modificar o crear
- En qué carpeta/s deben ubicarse según esta estructura:

```

src/entities/
src/use_cases/
src/interface_adapter/controllers/
src/interface_adapter/gateways/
src/interface_adapter/presenters/
infrastructure/cli/
infrastructure/fastapi/
infrastructure/[libreria_externa]/

```

- Breve justificación de su ubicación
- Descripción de la responsabilidad del módulo

---

Respondé como si fueras un arquitecto de software senior, con experiencia en sistemas legacy y arquitectura limpia en Python. Tus recomendaciones deben ser accionables y tener en cuenta un entorno de producción sensible.

Estoy trabajando en el desarrollo de software y quiero implementar la siguiente mejora técnica: 

[describe aquí la mejora técnica].

1. Si tenés dudas razonables sobre cómo implementarla, hacé preguntas aclaratorias y tratá de responderlas basándote en buenas prácticas, documentación oficial o experiencia previa.
2. Si tenés claridad suficiente, indicame de forma directa y precisa:
   - Qué archivos debo crear y/o modificar
   - Qué cambios debo realizar
   - Si es posible, explicá brevemente por qué esa es la mejor opción

Respondé como si fueras un desarrollador senior con criterio técnico.


---


Estoy trabajando en un proyecto de software en Python con una interfaz CLI similar a AS400-IBM. Necesito incorporar la siguiente funcionalidad:

[nueva funcionalidad]

Antes de hacerlo, realizá una auditoría técnica del proyecto (asumiendo que tenés acceso a su estructura y propósito) para evaluar si se aplican correctamente Clean Architecture, principios SOLID, patrones de diseño y POO.

Tu respuesta debe tener dos secciones:

1. Análisis y recomendación:
   - Evaluá el estado actual del diseño, identificando aciertos y problemas.
   - Indicá si el proyecto está en condiciones de incorporar la nueva funcionalidad directamente o si primero es necesario realizar una refactorización.
   - Justificá brevemente tu recomendación en base a mantenibilidad, extensibilidad y estabilidad del sistema.

2. Plan de acción:
   - Si recomendás refactorizar, detallá las tareas necesarias para mejorar la estructura del código sin agregar nueva funcionalidad.
   - Si recomendás avanzar con la funcionalidad, explicá cómo implementarla de forma progresiva, sin romper el entorno productivo.
   - En ambos casos, especificá qué archivos crear o modificar, su ubicación dentro de esta estructura:

src/entities/  
src/use_cases/  
src/interface_adapter/controllers/  
src/interface_adapter/gateways/  
src/interface_adapter/presenters/  
infrastructure/cli/  
infrastructure/fastapi/  
infrastructure/[libreria_externa]/  

   - Explicá brevemente la responsabilidad de cada módulo y por qué esa ubicación es la adecuada.

Respondé como un arquitecto de software senior con experiencia en sistemas legacy y arquitectura limpia en Python.

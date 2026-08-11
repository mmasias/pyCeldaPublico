<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Formulario|Error (rango superado)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/wireframe-formulario.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/wireframe-error.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Crear un `PonderacionEvaluacion` de una `Guia`, exigiendo que la suma de las `PonderacionEvaluacion` de su mismo `SistemaEvaluacion` caiga en el rango `[ponderacionMinima, ponderacionMaxima]`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver modelo del dominio (`DirectorGrado --|> Profesor`).

**Primer `crearX()` del catálogo con `<<choice>>`**, cerrado en la discussion [#38](https://github.com/mmasias/pyCelda/discussions/38): el modelo de dominio documenta dos reglas de validación distintas para `PonderacionEvaluacion` (rango por `SistemaEvaluacion`, suma total de la Guía = 100%), pero [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), ya cerrado, solo aplica la segunda -- la primera necesitaba un caso de uso propio o quedaba documentada sin aplicarse nunca. El rango no se compara contra el valor introducido en solitario, sino contra **la suma de todas las `PonderacionEvaluacion` de la Guía que apuntan al mismo `SistemaEvaluacion`, incluida la que se está creando** -- por eso el formulario muestra, junto al selector, lo ya asignado en esa Guía para el `SistemaEvaluacion` elegido y el margen disponible, recalculado si el actor cambia de selector.

**Mecánica del rechazo**: la rama roja de la `<<choice>>` no bloquea futuros intentos -- rechaza este envío concreto ("no permite guardar") y vuelve al listado, mismo mecanismo de salida con nota distinta (sin rama nueva en el diagrama de contexto) que ya usa [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md), aplicado aquí después de la entrada de datos en vez de antes, por primera vez en el catálogo.

`PonderacionEvaluacion{descripcion, ponderacion}` es demasiado minimalista para diferir campos entre `crear` y `editar` -- mismo criterio que cerró [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md) en la revisión de L3 (issue [#24](https://github.com/mmasias/pyCelda/issues/24)): pide `SistemaEvaluacion`, `descripcion` y `ponderacion` de una vez, mismo formulario que `editarPonderacionEvaluacion()`.

**Datos en memoria**: como el resto de la sesión de edición de una `Guia`, la `PonderacionEvaluacion` creada no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACIONES_EVALUACION_ABIERTO --> PONDERACION_EVALUACION_ABIERTO : crearPonderacionEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PonderacionEvaluacion`
- Modelo del dominio -- `Guia *-d- PonderacionEvaluacion`, `PonderacionEvaluacion -> SistemaEvaluacion`, regla de rango documentada en el README
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre de dónde y cómo se valida el rango

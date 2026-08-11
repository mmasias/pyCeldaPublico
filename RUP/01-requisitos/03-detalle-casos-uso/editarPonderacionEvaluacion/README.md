<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Formulario|Error (rango superado)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/wireframe-formulario.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/wireframe-error.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Editar un `PonderacionEvaluacion` de una `Guia`, con la misma validación de rango que `crearPonderacionEvaluacion()`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Caso de uso reutilizado por `DirectorGrado`, misma ficha -- ver modelo del dominio (`DirectorGrado --|> Profesor`).

Misma mecánica de `<<choice>>` que [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md), cerrada en la discussion [#38](https://github.com/mmasias/pyCelda/discussions/38), con una diferencia de destino: aquí la rama roja no saca al actor de la `PonderacionEvaluacion` -- vuelve al mismo `PONDERACION_EVALUACION_ABIERTO` ("sin cambios"), mismo mecanismo que usa [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) al devolver su rama roja al mismo estado de origen. El cálculo de "ya asignado" excluye el propio valor anterior de esta `PonderacionEvaluacion` (se está reemplazando, no sumando aparte).

`SistemaEvaluacion` es editable igual que `descripcion`/`ponderacion` -- no hay ninguna razón de dominio para fijarlo tras la creación, mismo criterio de "todo editable" que [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md).

**Datos en memoria**: los cambios no se persisten hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACION_EVALUACION_ABIERTO --> PONDERACION_EVALUACION_ABIERTO : editarPonderacionEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PonderacionEvaluacion`
- Modelo del dominio -- `PonderacionEvaluacion{descripcion, ponderacion}`, `PonderacionEvaluacion -> SistemaEvaluacion`
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre de dónde y cómo se valida el rango

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarPonderacionEvaluacion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarPonderacionEvaluacion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md)|Desarrollo|Pruebas|
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
|**Actor**|`Profesor`; `DirectorPrograma` como corrección excepcional de la `Guia`|
|**Objetivo**|Editar un `PonderacionEvaluacion` de una `Guia`, con la misma validación de rango que `crearPonderacionEvaluacion()`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**`DirectorPrograma` como corrección excepcional.** Además del `Profesor`, el `DirectorPrograma` del `Programa` de la `Guia` puede ejecutar este caso de uso sobre ella, como corrección directa. Regla de transición: `Aprobada -> Borrador` (`revocarAprobacion()`) y `EnRevision -> Rechazada` (`rechazar()`); `Borrador` y `Rechazada` se mantienen. Cada transición real registra un `HistorialCambio` con `campo="estado"`, autor el Director y comentario "corrección directa del Director". Un `DirectorPrograma` que no dirige el `Programa` de la `Guia` recibe `404`. El Director no gana `enviarGuiaARevision()`: el envío a revisión sigue siendo del `Profesor`. Si el mismo email resuelve a `Profesor` que imparte la asignatura y a `DirectorPrograma`, gana la rama `Profesor` (sin transición de estado). La transición se aplica solo tras superar las validaciones (ponderación mayor que cero y `<<choice>>` del máximo): un `422` no cambia el estado de la `Guia`.

Misma mecánica de `<<choice>>` que [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) -- **corregida tras la fase de Análisis** (rebanada vertical del hilo `Guia`, 2026-08-18): valida el **máximo puntual** (el valor introducido, por sí solo, contra `ponderacionMaxima` del `SistemaEvaluacion`), no la suma de hermanas. Sin exclusión del valor anterior -- ya no hace falta, no hay suma de la que excluirlo. Diferencia de destino respecto a `crearPonderacionEvaluacion()`: aquí la rama roja no saca al actor de la `PonderacionEvaluacion` -- vuelve al mismo `PONDERACION_EVALUACION_ABIERTO` ("sin cambios"), mismo mecanismo que usa [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) al devolver su rama roja al mismo estado de origen.

`SistemaEvaluacion` es editable igual que `descripcion`/`ponderacion` -- no hay ninguna razón de dominio para fijarlo tras la creación, mismo criterio de "todo editable" que [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md).

**Suelo por instrumento** (issue [#298](https://github.com/mmasias/pyCelda/issues/298)): la rama roja de la `<<choice>>` cubre las dos mismas condiciones que en [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) -- editar un instrumento a `0` o a un valor negativo se rechaza con un `422` (`La ponderación de un instrumento debe ser mayor que cero`) y la `PonderacionEvaluacion` queda **sin cambios**; el techo sigue en `<= ponderacionMaxima` con el mensaje corregido "del sistema de evaluación" (H-10). Ver la ficha de `crearPonderacionEvaluacion()` para el porqué del `> 0` fijo (`ponderacionMinima` solo acota la suma; `ponderacionMaxima` acota instrumento individual *y* suma).

**Datos en memoria**: los cambios no se persisten hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACION_EVALUACION_ABIERTO --> PONDERACION_EVALUACION_ABIERTO : editarPonderacionEvaluacion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PonderacionEvaluacion`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PonderacionEvaluacion{descripcion, ponderacion}`, `PonderacionEvaluacion -> SistemaEvaluacion`
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre de dónde y cómo se valida el rango

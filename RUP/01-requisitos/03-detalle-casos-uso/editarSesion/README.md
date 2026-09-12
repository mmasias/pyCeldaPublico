<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/wireframe-formulario.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Editar `tipo` y `descripcion` de una `Sesion` de la `PlanificacionDocente`; el `numero` no es editable (correlativo automático)|
|**Tipo**|Secundario|
|**Nivel**|Subfunción|

</div>

**Sin `<<choice>>`, mismo motivo que [`crearSesion()`](../crearSesion/README.md)**: sin enlace estructural a `SistemaEvaluacion`/`PonderacionEvaluacion` (decisión 4 de discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)), no hay regla de negocio que pueda rechazar la edición.

`numero` no aparece en el formulario -- es correlativo automático, sin caso de uso de reordenar (decisión 6 de discussion #140); solo `tipo` (desplegable con las 6 opciones del enum) y `descripcion` son editables.

**Datos en memoria**: los cambios no se persisten hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

**Desarrollo** (Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): igual que [`crearSesion()`](../crearSesion/README.md), la `Sesion` sigue el patrón `vinculada`. `editarSesion()` escribe el cambio al instante; [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) es quien confirma la vinculación o retira la `Sesion` que el profesor haya quitado de la lista de trabajo. La sincronización de sesiones en `guardarBorradorGuia` y su inclusión en el `409` de `enviarGuiaARevision` se añadieron en #206.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : editarSesion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Sesion{numero, tipo, descripcion}`
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/wireframe-formulario.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Crear una `Sesion` de la `PlanificacionDocente` de una `Guia`, con el siguiente número correlativo automático|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Sin `<<choice>>`, a diferencia de [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md)**: no existe ninguna regla de negocio que pueda rechazar el alta -- `Sesion` no se enlaza estructuralmente con `SistemaEvaluacion`/`PonderacionEvaluacion` en esta iteración (decisión 4 de discussion [#140](https://github.com/mmasias/pyCelda/discussions/140), riesgo aceptado a propósito), así que una `Sesion` de tipo `EVALUACION_CONTINUA` no se valida contra las ponderaciones reales de la Guía. Camino verde único.

`numero` no se solicita: lo asigna el sistema como el siguiente correlativo tras la última `Sesion` existente (o `1` si la planificación docente está vacía) -- sin caso de uso de reordenar, el profesor construye la planificación docente agregando en cadena (decisión 6 de discussion #140). Los otros dos puntos donde el sistema fija `numero` sin pedirlo son [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) y [`generarPlanificacionDocenteGenerica()`](../generarPlanificacionDocenteGenerica/README.md) (familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184)): al reemplazar o arrancar la planificación docente en bloque, las `Sesion` nacen renumeradas `1..N` en persistencia -- son filas nuevas, la numeración secuencial desde 1 es su valor de alta, a diferencia de la renumeración solo posicional de [`eliminarSesion()`](../eliminarSesion/README.md). Ambas nacen además `vinculada=True` directo (arranque en bloque, no edición incremental), a diferencia del `vinculada=False` de este caso de uso.

`tipo` es un desplegable con las 6 opciones del enum cerrado (`CLASE_TEORICA`, `CLASE_PRACTICA`, `CLASE_TEORICO_PRACTICA`, `CLASE_LABORATORIO`, `EVALUACION_CONTINUA`, `EVALUACION_PARCIAL`), no texto libre.

**Datos en memoria**: como el resto de la sesión de edición de una `Guia`, la `Sesion` creada no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

**Desarrollo** (Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): mismo patrón CRUD real + inmediato con `vinculada: bool` que `PonderacionEvaluacion` y `ReferenciaBibliografica`. `crearSesion()` escribe la fila al instante con `vinculada=False`; es [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) quien la vincula si sigue en la lista de trabajo enviada, o la borra si el profesor la quitó ([`eliminarSesion()`](../eliminarSesion/README.md)). Hasta #206 el backend no cumplía esto -- `guardarBorradorGuia` no sincronizaba sesiones y `enviarGuiaARevision` no las contaba entre los ítems sin guardar (`409`); el RUP y el frontend ya lo asumían.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : crearSesion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PlanificacionDocente *-- Sesion`, `Sesion{numero, tipo, descripcion}`
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente

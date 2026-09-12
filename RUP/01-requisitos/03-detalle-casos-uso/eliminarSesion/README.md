<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarSesion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarSesion/wireframe-confirmacion.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor`|
|**Objetivo**|Eliminar una `Sesion` de la `PlanificacionDocente`; el listado se renumera visualmente para no dejar huecos|
|**Tipo**|Primario|
|**Nivel**|Usuario|

</div>

**Renumeración visual, sin tocar `numero` persistido** (alineado con lo construido, Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206); la decisión de Manuel sobre "renumerar para no dejar huecos" se materializó en presentación): al eliminar una `Sesion` intermedia, el listado no deja huecos porque la numeración que ve el profesor es **posicional** (el orden de la lista, no `Sesion.numero`). `Sesion.numero` persistido conserva el valor de alta y puede quedar con huecos, sin efecto observable -- el orden se mantiene y `siguiente_numero` es `max + 1`. No hay caso de uso de reordenar (decisión 6 de discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)). El wireframe de confirmación avisa de que las siguientes se renumeran antes de que el profesor confirme.

Contraste con [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md) (issue [#184](https://github.com/mmasias/pyCelda/issues/184)): allí la renumeración `1..N` **sí** toca `Sesion.numero` persistido, porque las filas son nuevas (copiadas de la guía hermana) y su valor de alta es esa secuencia -- no es un reajuste retroactivo de filas ya existentes como aquí.

Solicitada desde el listado ([`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md)), con confirmación explícita antes de eliminar -- mismo patrón de dos ramas (confirmar/cancelar) que el resto de `eliminarX()` del catálogo con confirmación simple, sin `<<choice>>` bloqueante: nada depende estructuralmente de una `Sesion`.

**Datos en memoria**: la eliminación no se persiste hasta [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) o [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- ver [catálogo de actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md).

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : eliminarSesion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PlanificacionDocente *-- Sesion`, sin entidad que dependa de `Sesion`
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente

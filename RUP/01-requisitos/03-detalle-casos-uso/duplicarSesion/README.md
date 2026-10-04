<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/duplicarSesion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/duplicarSesion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > duplicarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/duplicarSesion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/duplicarSesion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Profesor` (heredado por `DirectorPrograma`)|
|**Objetivo**|Duplicar una `Sesion` ya persistida de la `PlanificacionDocente`, insertando la copia justo después de la original|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Copia `tipo` y `descripcion` de la `Sesion` origen, la inserta con `numero` = origen + 1 y renumera +1 las posteriores de la misma `Guia`, todo en una transacción; `vinculada` queda en su valor por defecto. Acotado a "justo después de X" (issue [#364](https://github.com/mmasias/pyCelda/issues/364)): no es reordenamiento general. Solo se ofrece sobre filas ya guardadas (no sobre las pendientes en memoria) y sin confirmación. A diferencia de [`crearSesion()`](../crearSesion/README.md)/[`eliminarSesion()`](../eliminarSesion/README.md), **se persiste de inmediato** (`POST /sesiones/{sesion_id}/duplicar`) y registra un `HistorialCambio` (`campo=planificacion_docente`); la respuesta devuelve la planificación completa ya renumerada.

**Hueco de documentación hallado en la auditoría del issue [#605](https://github.com/mmasias/pyCelda/issues/605)**: endpoint y botón `📑 Duplicar` de `PlanificacionDocente` ya existían sin reflejo en el diagrama de contexto ni en el catálogo. Se documenta lo construido, sin cambiar comportamiento.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : duplicarSesion()`
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) -- catálogo de casos de uso de `Profesor` sobre `PlanificacionDocente`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PlanificacionDocente *-- Sesion`
- [Issue #364](https://github.com/mmasias/pyCelda/issues/364) -- duplicar una sesión
- [Issue #605](https://github.com/mmasias/pyCelda/issues/605) -- auditoría de vigencia de diagramas de contexto y catálogos

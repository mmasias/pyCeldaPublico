<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > rechazarGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Rechazar una `Guia` que está `EnRevision`, con un comentario opcional para el `Profesor`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Segunda decisión de la familia -- ver [`aprobarGuia()`](../aprobarGuia/README.md) para el contexto completo, cerrado en la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

**`comentario` opcional, pedido explícitamente**: a diferencia de `aprobarGuia()`/`escalarGuiaAAprobada()` (sin incidencia, sin campo), `rechazarGuia()` sí narra una incidencia -- el formulario pide `comentario` para que el `DirectorGrado` deje al `Profesor` una pista de qué corregir. Sigue siendo opcional (`HistorialCambio.comentario` no es obligatorio en el modelo de dominio); si se deja vacío, la fila de `HistorialCambio` queda sin texto, sin valor por defecto (a diferencia de `aprobarGuia()`, que sí rellena uno). Decisión cerrada en el punto 1 de la discussion #44.

**Sin pantalla de confirmación** ni sub-estado `ConfirmandoX`: el propio formulario de `comentario` ya actúa como el paso de pausa antes de decidir -- mismo criterio que el resto de la familia (punto 4 de la discussion #44). `rechazarGuia()` se deshace con el reenvío del `Profesor` (`enviarGuiaARevision()`, ya construido), así que la decisión no es irreversible en el sentido de `eliminarX()`.

Sin pantalla de éxito distinta: al no haber rama de fallo, el wireframe muestra solo el formulario -- la llegada a `GUIAS_DEL_GRADO_ABIERTO` ya está ilustrada en [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), mismo criterio que `crearPonderacionEvaluacion()`/`editarAsociacionMetodologiaDocenteMateria()` (formulario sin pantalla de éxito aparte).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : rechazarGuia()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- Diagrama de estados de Guia -- `EnRevision -> Rechazada`
- Modelo del dominio -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`
- [`aprobarGuia()`](../aprobarGuia/README.md) -- contraparte de la misma decisión, sin campo de comentario
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, puntos 1 y 4

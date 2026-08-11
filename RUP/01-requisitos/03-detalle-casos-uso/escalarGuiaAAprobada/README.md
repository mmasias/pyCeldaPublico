<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > escalarGuiaAAprobada()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Aprobar directamente una `Guia` que está `Borrador` o `Rechazada`, sin pasar por `EnRevision`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Tercera decisión de la familia -- ver [`aprobarGuia()`](../aprobarGuia/README.md) para el contexto completo. `GUIA_ABIERTO` es un único estado en el diagrama de contexto independientemente de si `Guia.estado` es `Borrador` o `Rechazada`: la especificación no distingue el origen (ambas transiciones comparten el mismo destino `Aprobada` y la misma mecánica), es el propio dato de la `Guia` el que determina si el botón `[Escalar a aprobada]` tiene sentido ofrecerlo -- mismo criterio de disponibilidad condicional que el resto de decisiones de esta familia.

**Sin campo de formulario**, igual que `aprobarGuia()`: es un "sí" sin incidencia que explicar, el sistema registra `"escalada a aprobada sin incidencia"` en `HistorialCambio.comentario` sin pedir nada al `DirectorGrado`. **Sin pantalla de confirmación**: se deshace igual que `aprobarGuia()`, con `revocarAprobacionGuia()`. Ambos puntos cerrados en la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

Único caso de uso de L9 con dato real, sin hipótesis: `GII__IYA003` está realmente en `Borrador` (estado visible en el catálogo desde L7), así que el wireframe la usa tal cual -- no hace falta forzar un estado hipotético, a diferencia del resto de decisiones de esta familia.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : escalarGuiaAAprobada()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- Diagrama de estados de Guia -- `{Borrador,Rechazada} -> Aprobada`, escalado directo
- Modelo del dominio -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`
- [`aprobarGuia()`](../aprobarGuia/README.md) -- misma mecánica de "sí sin incidencia", origen `EnRevision` en vez de `{Borrador,Rechazada}`
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, puntos 1 y 4

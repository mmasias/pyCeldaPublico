<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > revocarAprobacionGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Revocar la aprobación de una `Guia` `Aprobada`, devolviéndola a `Borrador`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Cuarta decisión de la familia, una de las tres transiciones de reapertura desde `Aprobada` (ver README del modelo de dominio, entrada "Reapertura desde `Aprobada`"). A diferencia de `Admin` (`reabrirGuiaPorIncidencia()`, destino `EnRevision`), el `DirectorGrado` revoca su propia aprobación con destino `Borrador`: revocar es decir "esto no está listo", así que vuelve al mismo punto que si el `Profesor` nunca la hubiera enviado, no a la cola de revisión.

**`comentario` opcional, pedido explícitamente**: narra una incidencia (el director explica por qué se echa atrás), mismo mecanismo que `rechazarGuia()` -- ver punto 1 de la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44). **Sin pantalla de confirmación**: es en sí misma la corrección de una decisión previa (`aprobarGuia()`/`escalarGuiaAAprobada()`), no una acción irreversible que necesite una pausa adicional -- punto 4 de la misma discussion.

Wireframe con `GII__IYA003` mostrada hipotéticamente `Aprobada` -- estado real necesario como precondición de esta decisión, que el catálogo todavía no tiene documentado en ninguna `Guia` real; mismo criterio ilustrativo que el resto del lote.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : revocarAprobacionGuia()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- Diagrama de estados de Guia -- `Aprobada -> Borrador` (`DirectorGrado`)
- Modelo del dominio -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, entrada "Reapertura desde Aprobada"
- [`reabrirGuiaPorIncidencia()`](../reabrirGuiaPorIncidencia/README.md) -- misma familia de reapertura, actor `Admin`, destino `EnRevision`
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, puntos 1 y 4

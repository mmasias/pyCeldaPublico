<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarEstadoGuias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Consultar el listado de `Guia` de un `Grado`, con su estado actual|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Puerta de entrada al ciclo de revisión del grado: primer caso de uso de L9, abre `GUIAS_DEL_GRADO_ABIERTO`, el listado desde el que se navega a las nueve decisiones/acciones restantes (`abrirGuia()` reutilizado, más `notificarGuiasActualizadas()` como self-loop del propio listado). Mismo patrón que `abrirAsignaturasGrado()`: listado plural sin `<<choice>>`, sin equivalente en `Admin` (que llega a este mismo `GUIAS_DEL_GRADO_ABIERTO` por su propio hilo, reabertura por incidencia, no por revisión -- ver [`diagramaContextoAdmin.puml`](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml)).

Columna **Estado**: valor de `Guia.estado` (`Borrador`/`EnRevision`/`Aprobada`/`Rechazada`), determina qué decisión ofrece `abrirGuia()` al abrir cada fila -- `[Aprobar]`/`[Rechazar]` si `EnRevision`, `[Escalar a aprobada]` si `Borrador`/`Rechazada`, `[Revocar aprobación]` si `Aprobada` (ver retoque de [`abrirGuia()`](../abrirGuia/README.md) en este mismo lote).

Una sola fila real en el wireframe (`GII__IYA003`, Programación I) -- única `Guia` confirmada del seed. **Mostrada hipotéticamente en `EnRevision`**: su estado real es `Borrador` (así se ve en el resto del catálogo desde L7); se fuerza aquí de forma ilustrativa, documentada explícitamente, porque el catálogo no tiene todavía una `Guia` real en revisión y el caso de uso pierde sentido si la única fila mostrada nunca ofreciera `[Aprobar]`/`[Rechazar]` -- decisión tomada con el usuario en la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : consultarEstadoGuias()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Guia`
- Diagrama de estados de Guia -- los cuatro estados mostrados en la columna Estado
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, dato hipotético de `EnRevision` para el wireframe

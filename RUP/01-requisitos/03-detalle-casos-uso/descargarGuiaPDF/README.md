<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > descargarGuiaPDF()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/descargarGuiaPDF/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `Profesor` (heredado por `DirectorGrado`)|
|**Objetivo**|Descargar el PDF ya generado de una `Guia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Compartido entre `Admin` y `Profesor` **sin relación de herencia entre ambos** -- un solo caso de uso, una sola especificación, catalogado de forma independiente en `actoresCasosUsoAdminOperativa.puml` y en `actoresCasosUsoProfesor.puml`, mismo criterio que `abrirGrados()`/`abrirAsignaturaGrado()` reutilizados entre `Admin`/`DirectorGrado`. Self-loop de `GUIA_ABIERTO` en los tres diagramas de contexto (`Profesor`, `DirectorGrado` heredado, `Admin`).

**`<<choice>>` bloqueante en la especificación, pero sin pantalla de bloqueo en el wireframe**: si `fechaGeneracionPDF` está vacía no hay PDF que mostrar, pero el botón `[Descargar PDF]` ya se ofrece condicionalmente en `GUIA_ABIERTO` (ver retoque de [`abrirGuia()`](../abrirGuia/README.md)) -- no aparece cuando el dato está vacío, así que la rama roja nunca se dispara desde esta interfaz. Se mantiene en la especificación como salvaguarda estructural del caso de uso (reutilizable desde otro punto no modelado todavía), no como un flujo real de este wireframe -- decisión cerrada en el punto 2 de la discussion [#44](https://github.com/mmasias/pyCelda/discussions/44).

Wireframe con `GII__IYA003` mostrada hipotéticamente con PDF ya generado (`fechaGeneracionPDF` con valor) -- su estado real (`Borrador`, sin PDF) es justo el caso que el botón condicional excluye; mismo criterio ilustrativo que el resto del lote.

## Referencias

- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : descargarGuiaPDF()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- misma transición, sin herencia
- [actoresCasosUsoProfesor.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoProfesor.puml) / [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catalogado en ambos, sin herencia
- Modelo del dominio -- `fechaGeneracionPDF`, distinta de `fechaUltimaModificacion`/`fechaCreacion`
- [`generarGuiasPDF()`](../generarGuiasPDF/README.md) -- caso de uso que produce el dato que este consume
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de L9, punto 2

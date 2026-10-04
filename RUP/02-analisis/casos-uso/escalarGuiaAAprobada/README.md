<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > escalarGuiaAAprobada()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/escalarGuiaAAprobada/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`escalarGuiaAAprobada()`](/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/README.md): un solo paso, sin `<<choice>>`, sin formulario -- el `DirectorPrograma` solicita escalar y el sistema transiciona `Guia.estado` de `Borrador` o `Rechazada` a `Aprobada`, registrando el `HistorialCambio` con el comentario fijo `"escalada a aprobada sin incidencia"`. Misma familia que [`aprobarGuia()`](../aprobarGuia/README.md): "sí" sin matiz, comentario fijo por el propio caso de uso -- a diferencia de aquel, el estado de origen no es único (`{Borrador, Rechazada}`), así que el `valorAnterior` registrado varía según de cuál venga.

**Retoque posterior (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224), cierre de Frente B)**: mismo retoque que [`aprobarGuia()`](../aprobarGuia/README.md) -- `escalarAAprobada()` regenera `fechaGeneracionPDF` (`regenerarPDF()`) como parte del propio cambio de estado, encapsulado en el método (Fat Model), sin colaboración nueva en el diagrama.

**Retoque posterior (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: también como `aprobarGuia()` -- dentro del mismo `escalarAAprobada()` la `Guia` re-deriva `Guia -- Profesor` de `AsignaturaPrograma -- Profesor` (Fat Model, sin flecha nueva). Un escalado directo es un punto de sincronización de la copia igual que una aprobación desde `EnRevision`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/escalarGuiaAAprobada/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EscalarGuiaAAprobadaView`

**Responsabilidades:**
- recoge la solicitud de escalado de la `Guia` abierta (un único paso: sin formulario ni confirmación).
- presenta la pantalla de resultado: estado anterior, estado actual (`Aprobada`) y el comentario fijo registrado.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `DirectorPrograma` solicita escalar la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIAS_DEL_PROGRAMA_ABIERTO`.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- coordina la decisión de revisión en tres piezas: pide a la `Guia` que aplique su transición de estado, registra el `HistorialCambio` con el comentario fijo `"escalada a aprobada sin incidencia"` y el `estadoAnterior` real (`Borrador` o `Rechazada`), y persiste el agregado.
- no pide ningún dato al actor: mismo criterio que `aprobarGuia()`.
- no modela rama de fallo: la acción solo es alcanzable sobre una `Guia` `Borrador` o `Rechazada` -- el botón que la invoca ya se ofrece condicionalmente según `Guia.estado`.

**Colaboraciones:**
- **Entrada:** `EscalarGuiaAAprobadaView`.
- **Salida:** `Guia`, `HistorialCambio`, `GuiaRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- aplica su propia transición de estado `{Borrador, Rechazada} -> Aprobada` (`escalarAAprobada()`), según su máquina de estados.
- como parte del mismo `escalarAAprobada()`, regenera `fechaGeneracionPDF` (`regenerarPDF()`) -- retoque posterior, discussion #224.
- como parte del mismo `escalarAAprobada()`, re-deriva `Guia -- Profesor` de la plantilla (issue #254) -- Fat Model, sin colaboración nueva.
- es el agregado dueño de su historial (`Guia *- HistorialCambio`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** compone `HistorialCambio`; persistida por `GuiaRepository`.

### `HistorialCambio`

**Responsabilidades:**
- registra el cambio con `campo = "estado"`, `valorAnterior` (el estado real de origen, `Borrador` o `Rechazada`), `valorNuevo = "Aprobada"` y `comentario = "escalada a aprobada sin incidencia"`; fija su `fecha`.

**Colaboraciones:**
- **Entrada:** `GuiaController` (registro); `Guia` (composición).

### `GuiaRepository`

**Responsabilidades:**
- persiste de verdad el agregado (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/escalarGuiaAAprobada/wireframes.puml) -- fuente de verdad del paso único y del comentario fijo.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_PROGRAMA_ABIERTO : escalarGuiaAAprobada()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `{Borrador, Rechazada} -> Aprobada` (escalado directo) que la `Guia` aplica en `escalarAAprobada()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, `Guia *- HistorialCambio`.
- [`aprobarGuia()`](../aprobarGuia/README.md) -- misma familia, mismo criterio de comentario fijo sin pedir nada al actor, mismo retoque de `regenerarPDF()`.
- [`rechazarGuia()`](../rechazarGuia/README.md) / [`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md) -- resto de la familia de decisiones sobre `Guia`; ninguna de las dos regenera PDF.
- [`editarSemestreGuia()`](../editarSemestreGuia/README.md) -- disparador original de `regenerarPDF()`, ya no en exclusiva.
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- consumidor de `fechaGeneracionPDF`.
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- cierre de Frente B.
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- `escalarAAprobada()` re-deriva `Guia -- Profesor`.

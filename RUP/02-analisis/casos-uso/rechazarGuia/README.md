<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > rechazarGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/rechazarGuia/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/rechazarGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`rechazarGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/README.md): un solo paso, sin `<<choice>>` -- el `DirectorGrado` introduce un comentario opcional y solicita rechazar; el sistema transiciona `Guia.estado` de `EnRevision` a `Rechazada` y registra el `HistorialCambio` con ese comentario. Misma familia que [`aprobarGuia()`](../aprobarGuia/README.md) (decisión de revisión inmediata, con persistencia real), pero con `comentario` pedido al actor en vez de fijo -- es una incidencia, no un "sí" sin matiz.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/rechazarGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `RechazarGuiaView`

**Responsabilidades:**
- presenta el `estado` actual de la `Guia` y un campo de `comentario` opcional.
- permite solicitar rechazar.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `DirectorGrado` solicita rechazar la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIAS_DEL_GRADO_ABIERTO`.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- coordina la decisión de revisión en tres piezas: pide a la `Guia` que aplique su transición de estado, registra el `HistorialCambio` con el `comentario` recibido del actor (puede ir vacío) y persiste el agregado.
- no modela rama de fallo: la especificación no tiene `<<choice>>` -- la acción solo es alcanzable sobre una `Guia` `EnRevision`.

**Colaboraciones:**
- **Entrada:** `RechazarGuiaView`.
- **Salida:** `Guia`, `HistorialCambio`, `GuiaRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- aplica su propia transición de estado `EnRevision -> Rechazada` (`rechazar()`), según su máquina de estados.
- es el agregado dueño de su historial (`Guia *- HistorialCambio`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** compone `HistorialCambio`; persistida por `GuiaRepository`.

### `HistorialCambio`

**Responsabilidades:**
- registra el cambio con `campo = "estado"`, `valorAnterior = "EnRevision"`, `valorNuevo = "Rechazada"` y el `comentario` introducido por el `DirectorGrado` (opcional); fija su `fecha`.

**Colaboraciones:**
- **Entrada:** `GuiaController` (registro); `Guia` (composición).

### `GuiaRepository`

**Responsabilidades:**
- persiste de verdad el agregado (`actualizar(guia)`): el rechazo es una decisión de revisión inmediata.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/rechazarGuia/wireframes.puml) -- fuente de verdad del comentario opcional.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : rechazarGuia()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `EnRevision -> Rechazada` que la `Guia` aplica en `rechazar()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, `Guia *- HistorialCambio`.
- [`aprobarGuia()`](../aprobarGuia/README.md) -- misma familia de decisiones de revisión, contraste: comentario fijo, sin pedir nada al actor.
- [`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md) / [`revocarAprobacionGuia()`](../revocarAprobacionGuia/README.md) -- resto de la familia de decisiones sobre `Guia`.

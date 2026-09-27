<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > revocarAprobacionGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/revocarAprobacionGuia/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/revocarAprobacionGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`revocarAprobacionGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/README.md): un solo paso, sin `<<choice>>` -- el `DirectorGrado` introduce un comentario opcional y solicita revocar; el sistema transiciona `Guia.estado` de `Aprobada` a `Borrador` y registra el `HistorialCambio` con ese comentario. Misma forma que [`rechazarGuia()`](../rechazarGuia/README.md): comentario opcional pedido al actor, narra una incidencia sobre una `Guia` ya aprobada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/revocarAprobacionGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `RevocarAprobacionGuiaView`

**Responsabilidades:**
- presenta el `estado` actual de la `Guia` (`Aprobada`) y un campo de `comentario` opcional.
- permite solicitar revocar.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `DirectorGrado` solicita revocar la aprobación de la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIAS_DEL_GRADO_ABIERTO`.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- coordina la decisión de revisión en tres piezas: pide a la `Guia` que aplique su transición de estado, registra el `HistorialCambio` con el `comentario` recibido del actor (puede ir vacío) y persiste el agregado.
- no modela rama de fallo: la acción solo es alcanzable sobre una `Guia` `Aprobada`.

**Colaboraciones:**
- **Entrada:** `RevocarAprobacionGuiaView`.
- **Salida:** `Guia`, `HistorialCambio`, `GuiaRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- aplica su propia transición de estado `Aprobada -> Borrador` (`revocarAprobacion()`), según su máquina de estados.
- es el agregado dueño de su historial (`Guia *- HistorialCambio`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** compone `HistorialCambio`; persistida por `GuiaRepository`.

### `HistorialCambio`

**Responsabilidades:**
- registra el cambio con `campo = "estado"`, `valorAnterior = "Aprobada"`, `valorNuevo = "Borrador"` y el `comentario` introducido por el `DirectorGrado` (opcional); fija su `fecha`.

**Colaboraciones:**
- **Entrada:** `GuiaController` (registro); `Guia` (composición).

### `GuiaRepository`

**Responsabilidades:**
- persiste de verdad el agregado (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/revocarAprobacionGuia/wireframes.puml) -- fuente de verdad del comentario opcional.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : revocarAprobacionGuia()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `Aprobada -> Borrador` (revocación) que la `Guia` aplica en `revocarAprobacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, `Guia *- HistorialCambio`.
- [`rechazarGuia()`](../rechazarGuia/README.md) -- misma forma: comentario opcional narrando una incidencia.
- [`aprobarGuia()`](../aprobarGuia/README.md) / [`escalarGuiaAAprobada()`](../escalarGuiaAAprobada/README.md) -- resto de la familia de decisiones sobre `Guia`.

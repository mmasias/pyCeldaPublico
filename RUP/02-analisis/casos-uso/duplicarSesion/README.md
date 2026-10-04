<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > duplicarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/duplicarSesion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`duplicarSesion()`](/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/README.md): CRUD real e inmediato contra `SesionRepository`, sin `<<choice>>` -- no hay regla de negocio que pueda rechazar la duplicación. Misma entidad que [`crearSesion()`](../crearSesion/README.md), con tres diferencias: (1) no hay formulario -- se actúa sobre una `Sesion` ya persistida con una sola acción (botón `📑 Duplicar` en su fila), (2) el `numero` de la copia no es el siguiente correlativo sino **origen + 1**, con renumeración +1 de las posteriores de la misma `Guia` (acotado a "justo después de X", no es reordenamiento general; issue [#364](https://github.com/mmasias/pyCelda/issues/364)), y (3) deja constancia en `HistorialCambio` (`campo=planificacion_docente`, issue [#420](https://github.com/mmasias/pyCelda/issues/420)). La respuesta devuelve la planificación docente completa ya renumerada, no solo la `Sesion` nueva.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/duplicarSesion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DuplicarSesionView`

**Responsabilidades:**
- ofrece la acción de duplicar solo sobre las filas ya guardadas del listado (no sobre las pendientes en memoria), sin confirmación.
- al volver, el listado muestra la copia justo después de la original y las posteriores ya renumeradas.

**Colaboraciones:**
- **Entrada:** `:PLANIFICACION_DOCENTE_ABIERTO` -- el `Profesor` solicita duplicar una sesión desde el listado de la Planificación docente.
- **Control:** `PlanificacionDocenteController`.
- **Salida:** `:PLANIFICACION_DOCENTE_ABIERTO` -- copia insertada tras la original, sesiones posteriores renumeradas.

## Clases de controlador

### `PlanificacionDocenteController`

**Responsabilidades:**
- duplica la `Sesion` real e inmediatamente en `SesionRepository` (`duplicar(sesionId)`) -- ninguna llamada a `Guia` salvo para autorizar y resolver a qué `Guia` pertenece.
- registra el cambio en `HistorialCambio` (`planificacion_docente`: "n sesiones" -> "n+1 sesiones").
- devuelve la planificación docente completa ya renumerada.

**Colaboraciones:**
- **Entrada:** `DuplicarSesionView`.
- **Salida:** `SesionRepository`, `HistorialCambio`.

## Clases de modelo

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo`, `descripcion` y `guiaId` -- la copia hereda `tipo` y `descripcion` de la original, se inserta en `numero` = origen + 1 y nace pendiente-sin-vincular, como cualquier `Sesion` recién creada.

**Colaboraciones:**
- **Entrada:** creada y renumerada por `SesionRepository`.

### `SesionRepository`

**Responsabilidades:**
- inserta la copia y renumera +1 las posteriores de la misma `Guia` (`duplicar(sesionId)`) -- persistencia real e inmediata, todo en una única transacción.

**Colaboraciones:**
- **Entrada:** `PlanificacionDocenteController`.
- **Salida:** gestiona `Sesion`.

### `HistorialCambio`

**Responsabilidades:**
- recoge la fila de auditoría de la duplicación (`campo=planificacion_docente`, recuento antes/después, comentario con la sesión de origen).

**Colaboraciones:**
- **Entrada:** `PlanificacionDocenteController`.

**Actor `DirectorPrograma`** (issue [#612](https://github.com/mmasias/pyCelda/issues/612)): hereda el caso de uso del `Profesor` como corrección excepcional sobre la `Guia` de su `Programa`; la colaboración es la misma, con la transición de estado de la `Guia` previa a la escritura.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/duplicarSesion/wireframes.puml) -- fuente de verdad de la acción.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : duplicarSesion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PlanificacionDocente *-- Sesion`.
- [`crearSesion()`](../crearSesion/README.md) -- plantilla estructural (misma entidad); contraste: allí el `numero` es el siguiente correlativo y no hay renumeración.
- [`editarSesion()`](../editarSesion/README.md) / [`eliminarSesion()`](../eliminarSesion/README.md) -- mismos participantes sobre la `Sesion`.
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- el listado desde el que se invoca y al que se vuelve.
- [Issue #364](https://github.com/mmasias/pyCelda/issues/364) -- duplicar una sesión.

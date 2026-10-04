<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarSistemaEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/README.md): `<<choice>>` bloqueante -- borrado físico de la composición de la `Materia`, bloqueado si alguna `PonderacionEvaluacion` lo usa (`PonderacionEvaluacion --> SistemaEvaluacion`, desde la `Guia`). `SistemaEvaluacion` no tiene `estado` propio -- vive y muere con la `Materia` que lo contiene, así que su borrado es siempre físico, mismo patrón que `eliminarMetodologiaDocente()`/`eliminarResultadoAprendizaje()`. Diferencia con ambos: la comprobación del bloqueo es un **conteo**, no una lista de nombres -- una `PonderacionEvaluacion` no tiene un nombre distintivo tipo `Materia.nombre`; puede haber muchas repartidas en varias `Guia`, y listarlas alargaría el mensaje sin aportar claridad. `contarPonderacionesAsociadas()` devuelve el número; cero significa que puede eliminarse.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarSistemaEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarSistemaEvaluacionView`

**Responsabilidades:**
- en la rama verde, presenta la información del `SistemaEvaluacion` (`tipo`, `descripcion`, rango de ponderación) y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo nombrando las `AsignaturaPrograma` donde el `SistemaEvaluacion` está en uso (issue #581).

**Colaboraciones:**
- **Entrada:** `:SISTEMAS_EVALUACION_ABIERTO` -- el `Admin` solicita eliminar un `SistemaEvaluacion`.
- **Control:** `SistemaEvaluacionController`.
- **Salida:** `:SISTEMAS_EVALUACION_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `SistemaEvaluacionController`

**Responsabilidades:**
- aplica el `<<choice>>`: pregunta cuántas `PonderacionEvaluacion` usan el `SistemaEvaluacion` (`puedeEliminar(sistemaEvaluacionId)`).
- si no está bloqueado y el `Admin` confirma, elimina real e inmediato (`eliminar(sistemaEvaluacionId)`) -- borrado físico, sin `estado` propio que mutar.

**Colaboraciones:**
- **Entrada:** `EliminarSistemaEvaluacionView`.
- **Salida:** `SistemaEvaluacionRepository`.

## Clases de modelo

### `SistemaEvaluacion`

**Responsabilidades:**
- porta `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima` -- la información presentada antes de confirmar.

**Colaboraciones:**
- **Entrada:** recuperada por `SistemaEvaluacionRepository`.
- **Salida:** eliminada físicamente por `SistemaEvaluacionRepository`.

### `SistemaEvaluacionRepository`

**Responsabilidades:**
- cuenta las `PonderacionEvaluacion` que usan el `SistemaEvaluacion` (`contarPonderacionesAsociadas(sistemaEvaluacionId) : int`) -- cero significa que puede eliminarse; el número alimenta el mensaje de la rama roja. Decisión cerrada: conteo simple, no listado de descripciones individuales.
- elimina el `SistemaEvaluacion` (`eliminar(sistemaEvaluacionId)`) -- borrado físico.

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`.
- **Salida:** gestiona `SistemaEvaluacion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante por `PonderacionEvaluacion` asociadas.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMAS_EVALUACION_ABIERTO --> SISTEMAS_EVALUACION_ABIERTO : eliminarSistemaEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PonderacionEvaluacion -> SistemaEvaluacion` (origen de la regla de bloqueo).
- [`eliminarMetodologiaDocente()`](../eliminarMetodologiaDocente/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico; allí el bloqueo lista nombres de `Materia`, aquí lista nombres de `AsignaturaPrograma` (issue #581).
- [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- contraste: borrado lógico sin `<<choice>>`.

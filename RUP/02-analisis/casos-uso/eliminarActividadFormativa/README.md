<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`eliminarActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): borrado físico del catálogo del `Programa`, con `<<choice>>` bloqueante tras la confirmación. "En uso" = horas > 0 en alguna `Materia` o en alguna `AsignaturaPrograma`; las filas a 0 son autopoblado y no cuentan. El chequeo cubre las **dos** clases de asociación (`ActividadFormativaMateria` y `ActividadFormativaAsignaturaPrograma`): nada garantiza que unas horas en una asignatura impliquen horas en su materia (la regla `AfM = Σ AfAdM` es blanda). Al borrar se retiran también las filas a 0.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarActividadFormativaView`

**Responsabilidades:**
- presenta `codigo` y `nombre` de la `ActividadFormativa` y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo con los nombres de las `Materia` en las que está en uso.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDADES_FORMATIVAS_ABIERTO`.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDADES_FORMATIVAS_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- carga la `ActividadFormativa` para la confirmación.
- al confirmar, aplica el `<<choice>>`: si `nombresMateriasAsociadas()` no está vacía, rechaza con esos nombres; si lo está, elimina real e inmediato.

**Colaboraciones:**
- **Entrada:** `EliminarActividadFormativaView`.
- **Salida:** `ActividadFormativaRepository`.

## Clases de modelo

### `ActividadFormativa`

**Responsabilidades:**
- porta `codigo` y `nombre` -- la información presentada antes de confirmar.

**Colaboraciones:**
- **Entrada:** recuperada por `ActividadFormativaRepository`.
- **Salida:** eliminada físicamente por `ActividadFormativaRepository`.

### `ActividadFormativaRepository`

**Responsabilidades:**
- responde con los nombres de las `Materia` donde la actividad está en uso (`nombresMateriasAsociadas(actividadFormativaId)`): horas > 0 en la propia `Materia` o en alguna de sus `AsignaturaPrograma`. Lista vacía significa que puede eliminarse.
- elimina la `ActividadFormativa` y sus filas a 0 de autopoblado (`eliminar(actividadFormativaId)`).

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa` y sus dos clases de asociación.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/wireframes.puml) -- fuente de verdad.
- [`eliminarCompetencia()`](../eliminarCompetencia/README.md) -- contraste: bloqueo con consulta previa de asignaciones.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarActividadFormativa()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo, bloqueado si la `ActividadFormativa` está *en uso* (horas > 0 en alguna `Materia` o en alguna `AsignaturaPrograma`). Las filas a 0 son autopoblado puro (toda `Materia` las tiene para todo el catálogo de su `Universidad`) y no cuentan como asignación: si contaran, ninguna actividad sería eliminable. A diferencia de `eliminarMetodologiaDocente()`, el chequeo cubre **dos** tablas de asociación (`ActividadFormativaMateria` y `ActividadFormativaAsignaturaPrograma`) porque, a diferencia de las metodologías, no existe un guard que garantice la inclusión de una en la otra. El mensaje de bloqueo nombra las `Materia` afectadas. Al borrar, se retiran también las filas a 0 de autopoblado.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarActividadFormativa/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarActividadFormativaView`

**Responsabilidades:**
- en la rama verde, presenta la información de la `ActividadFormativa` y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo por uso, con los nombres de las `Materia` afectadas.

**Colaboraciones:**
- **Entrada:** `:ACTIVIDADES_FORMATIVAS_ABIERTO` -- el `Admin` solicita eliminar una `ActividadFormativa`.
- **Control:** `ActividadFormativaController`.
- **Salida:** `:ACTIVIDADES_FORMATIVAS_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ActividadFormativaController`

**Responsabilidades:**
- aplica el `<<choice>>`: pregunta si la `ActividadFormativa` está en uso (`puedeEliminar(actividadFormativaId)`).
- si no está bloqueada y el `Admin` confirma, elimina real e inmediato (`eliminar(actividadFormativaId)`) -- borrado físico, sin `estado` propio que mutar.

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
- responde con los nombres de las `Materia` donde la actividad está en uso (`nombresMateriasAsociadas(actividadFormativaId)`) -- lista vacía significa que puede eliminarse; los nombres alimentan el mensaje de la rama roja.
- elimina la `ActividadFormativa` (`eliminar(actividadFormativaId)`) y sus filas a 0 de autopoblado.

**Colaboraciones:**
- **Entrada:** `ActividadFormativaController`.
- **Salida:** gestiona `ActividadFormativa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/wireframes.puml) -- fuente de verdad de el `<<choice>>` bloqueante por uso en Materias..
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDADES_FORMATIVAS_ABIERTO --> ACTIVIDADES_FORMATIVAS_ABIERTO : eliminarActividadFormativa()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`, catálogo de `Universidad` (`Universidad *-- ActividadFormativa`).
- [`eliminarMetodologiaDocente()`](../eliminarMetodologiaDocente/README.md) -- clúster plantilla; allí el chequeo es de una sola tabla.
- [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico y cascada de dos niveles.
- [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- contraste: borrado lógico sin `<<choice>>`.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo institucional, bloqueado si la `MetodologiaDocente` está asociada a alguna `Materia` (tabla `metodologias_materia`). A diferencia de `eliminarAsignatura()` (borrado lógico sin bloqueo, `estado` Vigente/Extinguido), aquí sí hay rama roja: el mensaje de bloqueo nombra las `Materia` asociadas. La comprobación cubre solo la asociación con `Materia`, no la de `AsignaturaGrado`: el guard de `desasociarMetodologiaDocenteMateria()` (409 si está en uso en alguna `AsignaturaGrado` de esa `Materia`) garantiza que una `MetodologiaDocente` nunca puede estar asociada a una `AsignaturaGrado` sin estar también asociada a la `Materia` padre -- si `metodologias_materia` no tiene ninguna fila, `asignaturas_grado_metodologias_docentes` no puede tenerla tampoco. Mismo patrón que [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md), pero con un solo nivel de la cascada que comprobar.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarMetodologiaDocenteView`

**Responsabilidades:**
- en la rama verde, presenta la información de la `MetodologiaDocente` y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo por uso en `Materia`, con los nombres de las materias asociadas.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_ABIERTO` -- el `Admin` solicita eliminar una `MetodologiaDocente`.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- aplica el `<<choice>>`: pregunta si la `MetodologiaDocente` está asociada a alguna `Materia` (`puedeEliminar(metodologiaDocenteId)`).
- si no está bloqueada y el `Admin` confirma, elimina real e inmediato (`eliminar(metodologiaDocenteId)`) -- borrado físico, sin `estado` propio que mutar.

**Colaboraciones:**
- **Entrada:** `EliminarMetodologiaDocenteView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion` -- la información presentada antes de confirmar.

**Colaboraciones:**
- **Entrada:** recuperada por `MetodologiaDocenteRepository`.
- **Salida:** eliminada físicamente por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- responde con los nombres de las `Materia` asociadas (`nombresMateriasAsociadas(metodologiaDocenteId)`) -- lista vacía significa que puede eliminarse; los nombres alimentan el mensaje de la rama roja. Suficiente por sí sola: el guard de `desasociarMetodologiaDocenteMateria()` impide que exista asociación a `AsignaturaGrado` sin la `Materia` padre.
- elimina la `MetodologiaDocente` (`eliminar(metodologiaDocenteId)`) -- borrado físico.

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.
- **Salida:** gestiona `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante por uso en Materias.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_ABIERTO --> METODOLOGIAS_DOCENTES_ABIERTO : eliminarMetodologiaDocente()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- MetodologiaDocente`, `AsignaturaGrado o-- MetodologiaDocente` (cascada en dos pasos cuya primera tabla basta como chequeo).
- [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico; allí la comprobación cubre los dos niveles de la cascada.
- [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- contraste: borrado lógico sin `<<choice>>`.

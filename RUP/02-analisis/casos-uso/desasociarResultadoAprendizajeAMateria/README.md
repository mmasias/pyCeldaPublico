<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarResultadoAprendizajeAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/README.md): `<<choice>>` bloqueante -- rompe la asociación con la `Materia` siempre que ninguna `AsignaturaPrograma` de esa `Materia` ya tenga asignado el mismo `ResultadoAprendizaje` (integridad de la cascada: los RA de una `AsignaturaPrograma` deben ser subconjunto de los de su `Materia`).

**Retocado (issue #179, 2026-09-05)**: `tieneResultadoAprendizajeEnUso(resultadoAprendizajeId) : boolean` pasa a `asignaturasProgramaConResultadoAprendizaje(resultadoAprendizajeId) : List<String>` -- mismo hueco que tenía `eliminarResultadoAprendizaje()` antes de su propio retoque (PR #178), auditado y replicado también aquí junto con [`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarResultadoAprendizajeAMateriaView`

**Responsabilidades:**
- en la rama verde, presenta la asociación y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo con las `AsignaturaPrograma` concretas en uso.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorPrograma` solicita desasociar un `ResultadoAprendizaje`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO` en los tres casos.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- aplica el `<<choice>>`: recupera las `AsignaturaPrograma` que usan el `ResultadoAprendizaje` (`asignaturasProgramaConResultadoAprendizaje(materiaId, resultadoAprendizajeId)`) -- lista vacía = no bloqueado.
- si no está bloqueado y el `DirectorPrograma` confirma, desasocia real e inmediato (`desasociarResultadoAprendizaje(materiaId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarResultadoAprendizajeAMateriaView`.
- **Salida:** `Materia`, `MateriaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- lista los nombres de sus `AsignaturaPrograma` que usan un `ResultadoAprendizaje` dado (`asignaturasProgramaConResultadoAprendizaje(resultadoAprendizajeId)`) -- origen de la regla de bloqueo, `AsignaturaPrograma o- ResultadoAprendizaje`.

**Colaboraciones:**
- **Entrada:** `MateriaController`.

### `MateriaRepository`

**Responsabilidades:**
- elimina real e inmediata la asociación (`desasociarResultadoAprendizaje(materiaId, resultadoAprendizajeId)`) -- no es un borrado del `ResultadoAprendizaje`, que sigue en el catálogo del `Programa`.

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAMateria/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarResultadoAprendizajeAMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o- ResultadoAprendizaje` (origen de la regla de bloqueo).
- [`asociarResultadoAprendizajeAMateria()`](../asociarResultadoAprendizajeAMateria/README.md) -- caso de uso complementario (alta de la asociación).
- [`desasociarResultadoAprendizajeAsignaturaPrograma()`](../desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- segundo escalón de la misma cascada, sin bloqueo por ser el último nivel.
- [`eliminarResultadoAprendizaje()` en Análisis](../eliminarResultadoAprendizaje/README.md) -- precedente del patrón booleano->lista (PR #178), auditado y replicado aquí (issue #179).

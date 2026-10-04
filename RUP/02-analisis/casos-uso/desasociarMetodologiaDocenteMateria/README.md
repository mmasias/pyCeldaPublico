<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarMetodologiaDocenteMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/README.md): `<<choice>>` bloqueante -- rompe el vínculo `MetodologiaMateria` siempre que ninguna `AsignaturaPrograma` de la `Materia` ya use esa `MetodologiaDocente` (primer escalón de la cascada de dos pasos hacia `AsignaturaPrograma`).

**Retocado (issue #179, 2026-09-05)**: `tieneMetodologiaDocenteEnUso(metodologiaDocenteId) : boolean` pasa a `asignaturasProgramaConMetodologiaDocente(metodologiaDocenteId) : List<String>` -- mismo hueco que tenía `eliminarResultadoAprendizaje()` antes de su propio retoque (PR #178): el booleano bastaba para bloquear, pero descartaba el detalle que la `View` necesita para nombrar las `AsignaturaPrograma` concretas en el mensaje de bloqueo.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarMetodologiaDocenteMateriaView`

**Responsabilidades:**
- en la rama verde, presenta la asociación y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo con las `AsignaturaPrograma` concretas en uso.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `DirectorPrograma` solicita desasociar una `MetodologiaDocente`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO` en los tres casos -- self-loop, con "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- aplica el `<<choice>>`: recupera las `AsignaturaPrograma` que usan la `MetodologiaDocente` (`asignaturasProgramaConMetodologiaDocente(materiaId, metodologiaDocenteId)`) -- lista vacía = no bloqueada.
- si no está bloqueada y el `DirectorPrograma` confirma, elimina real e inmediata la asociación (`desasociarMetodologiaDocente(materiaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarMetodologiaDocenteMateriaView`.
- **Salida:** `Materia`, `MetodologiaMateriaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- lista los nombres de sus `AsignaturaPrograma` que usan una `MetodologiaDocente` dada (`asignaturasProgramaConMetodologiaDocente(metodologiaDocenteId)`) -- origen de la regla de bloqueo, `AsignaturaPrograma o-- MetodologiaDocente`.

**Colaboraciones:**
- **Entrada:** `MateriaController`.

### `MetodologiaMateriaRepository`

**Responsabilidades:**
- elimina real e inmediata la asociación (`eliminar(materiaId, metodologiaDocenteId)`) -- no es un borrado de `MetodologiaDocente`, que sigue en el catálogo institucional.

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona la asociación entre `Materia` y `MetodologiaDocente`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarMetodologiaDocenteMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-- MetodologiaDocente` (origen de la regla de bloqueo, cascada en dos pasos).
- [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md) -- caso de uso complementario (alta de la asociación).
- [`desasociarMetodologiaDocenteAsignaturaPrograma()`](../desasociarMetodologiaDocenteAsignaturaPrograma/README.md) -- segundo escalón de la misma cascada, sin bloqueo por ser el último nivel.
- [`eliminarResultadoAprendizaje()` en Análisis](../eliminarResultadoAprendizaje/README.md) -- precedente del patrón booleano->lista (PR #178), auditado y replicado aquí (issue #179).

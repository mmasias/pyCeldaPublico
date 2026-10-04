<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarMetodologiaDocenteAAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/README.md): sin `<<choice>>` -- segundo escalón de la cascada `MetodologiaDocente` en dos pasos. Asocia una `MetodologiaDocente` ya asociada a la `Materia` a una `AsignaturaPrograma` concreta de esa `Materia`, sin clase de asociación (agregación simple).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarMetodologiaDocenteAAsignaturaProgramaView`

**Responsabilidades:**
- presenta la selección de `MetodologiaDocente` ya asociadas a la `Materia` y no asociadas aún a esta `AsignaturaPrograma`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita asociar una `MetodologiaDocente`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- lista las `MetodologiaDocente` que cumplen las dos condiciones -- ya asociadas a la `Materia`, no asociadas aún a esta `AsignaturaPrograma` (`cargarMetodologiasDocentesDisponibles(asignaturaProgramaId)`).
- asocia real e inmediato (`asociarMetodologiaDocente(asignaturaProgramaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `AsociarMetodologiaDocenteAAsignaturaProgramaView`.
- **Salida:** `MetodologiaDocenteRepository`, `AsignaturaProgramaRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- el subconjunto ya asociado a la `Materia`, del que se elige.

**Colaboraciones:**
- **Entrada:** listada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- lista las `MetodologiaDocente` ya asociadas a la `Materia` y no aún a esta `AsignaturaPrograma` (`listarDisponiblesParaAsignaturaPrograma(asignaturaProgramaId)`) -- aplica la regla de consistencia del modelo de dominio.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `MetodologiaDocente`.

### `AsignaturaPrograma`

**Responsabilidades:**
- gana una `MetodologiaDocente` en su colección asociada.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `AsignaturaProgramaRepository`.
- **Salida:** compone `MetodologiaDocente` asociadas.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- persiste la nueva asociación (`asociarMetodologiaDocente(asignaturaProgramaId, metodologiaDocenteId)`) -- agregación simple, sin clase de asociación que crear (a diferencia de `MetodologiaMateria`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaPrograma/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asociarMetodologiaDocenteAAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-r- MetodologiaDocente`; regla de consistencia, subconjunto de la `Materia`.
- [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md) -- primer escalón de la misma cascada.
- [`desasociarMetodologiaDocenteAsignaturaPrograma()`](../desasociarMetodologiaDocenteAsignaturaPrograma/README.md) -- caso de uso complementario (baja de la asociación).

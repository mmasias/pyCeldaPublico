<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarResultadoAprendizajeAAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md): sin `<<choice>>` -- segundo escalón de la cascada `ResultadoAprendizaje`. Asocia un `ResultadoAprendizaje` ya asignado a la `Materia` a una `AsignaturaPrograma` concreta de esa `Materia`, mismo patrón que [`asociarMetodologiaDocenteAAsignaturaPrograma()`](../asociarMetodologiaDocenteAAsignaturaPrograma/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarResultadoAprendizajeAAsignaturaProgramaView`

**Responsabilidades:**
- presenta la selección de `ResultadoAprendizaje` ya asignados a la `Materia` y no asignados aún a esta `AsignaturaPrograma`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita asociar un `ResultadoAprendizaje`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` que cumplen las dos condiciones -- ya asignados a la `Materia`, no asignados aún a esta `AsignaturaPrograma` (`cargarResultadosAprendizajeDisponibles(asignaturaProgramaId)`).
- asocia real e inmediato (`asociarResultadoAprendizaje(asignaturaProgramaId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `AsociarResultadoAprendizajeAAsignaturaProgramaView`.
- **Salida:** `ResultadoAprendizajeRepository`, `AsignaturaProgramaRepository`.

## Clases de modelo

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo` -- el subconjunto ya asignado a la `Materia`, del que se elige.

**Colaboraciones:**
- **Entrada:** listado por `ResultadoAprendizajeRepository`.

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` ya asignados a la `Materia` y no aún a esta `AsignaturaPrograma` (`listarDisponiblesParaAsignaturaPrograma(asignaturaProgramaId)`) -- aplica la regla de consistencia del modelo de dominio.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

### `AsignaturaPrograma`

**Responsabilidades:**
- gana un `ResultadoAprendizaje` en su colección asociada.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `AsignaturaProgramaRepository`.
- **Salida:** compone `ResultadoAprendizaje` asociados.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- persiste la nueva asociación (`asociarResultadoAprendizaje(asignaturaProgramaId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asociarResultadoAprendizajeAAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o- ResultadoAprendizaje`; regla de consistencia, subconjunto de la `Materia`.
- [`asociarResultadoAprendizajeAMateria()`](../asociarResultadoAprendizajeAMateria/README.md) -- primer escalón de la misma cascada.
- [`desasociarResultadoAprendizajeAsignaturaPrograma()`](../desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- caso de uso complementario (baja de la asociación).

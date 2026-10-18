<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarCompetencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarCompetencia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarCompetencia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`eliminarCompetencia()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarCompetencia/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): el `<<choice>>` de bloqueo se apoya en las asignaciones de la competencia (las mismas que pinta la ficha), y el controlador lo vuelve a comprobar al borrar.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarCompetencia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarCompetenciaView`

**Responsabilidades:**
- presenta la competencia y, según las asignaciones, el bloqueo con las materias y asignaturas que la usan o la confirmación.

**Colaboraciones:**
- **Entrada:** `:COMPETENCIAS_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `:COMPETENCIAS_ABIERTO` (tres ramas).

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- carga las asignaciones.
- rechaza el borrado si la competencia está asignada (409 con los nombres); si no, la borra.

**Colaboraciones:**
- **Entrada:** `EliminarCompetenciaView`.
- **Salida:** `CompetenciaRepository`.

## Clases de modelo

### `Competencia`

**Responsabilidades:**
- porta `codigo`, `tipo` (Básica, General, Transversal, Específica), `descripcion`.

**Colaboraciones:**
- **Entrada:** gestionada por `CompetenciaRepository`.

### `CompetenciaRepository`

**Responsabilidades:**
- gestiona `Competencia` y sus dos tablas de asociación (`materias_competencias`, `asignaturas_programa_competencias`).

**Colaboraciones:**
- **Entrada:** `CompetenciaController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarCompetencia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarCompetencia/wireframes.puml) -- fuente de verdad
- [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md) -- patrón de origen

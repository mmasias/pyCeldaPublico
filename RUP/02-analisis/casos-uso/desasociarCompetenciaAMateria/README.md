<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarCompetenciaAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarCompetenciaAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`desasociarCompetenciaAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): el `<<choice>>` lo responde la propia `Materia` (Fat Model), que recorre sus `AsignaturaPrograma` y devuelve los nombres de las que usan la competencia -- mismo mecanismo que `desasociarResultadoAprendizajeAMateria()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarCompetenciaAMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarCompetenciaAMateriaView`

**Responsabilidades:**
- presenta el bloqueo con los nombres de las asignaturas en uso, o la confirmación.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `:MATERIA_ABIERTO` (tres ramas).

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- pregunta a la `Materia` qué asignaturas usan la competencia.
- rechaza la desasociación si alguna la usa (409); si no, desasocia.

**Colaboraciones:**
- **Entrada:** `DesasociarCompetenciaAMateriaView`.
- **Salida:** `Materia`, `CompetenciaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- `asignaturasProgramaConCompetencia(competenciaId)`: nombres de sus `AsignaturaPrograma` que tienen la competencia.

**Colaboraciones:**
- **Entrada:** `CompetenciaController`.

### `CompetenciaRepository`

**Responsabilidades:**
- gestiona `Competencia` y sus dos tablas de asociación (`materias_competencias`, `asignaturas_programa_competencias`).

**Colaboraciones:**
- **Entrada:** `CompetenciaController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/wireframes.puml) -- fuente de verdad
- [`desasociarResultadoAprendizajeAMateria()`](../desasociarResultadoAprendizajeAMateria/README.md) -- patrón de origen

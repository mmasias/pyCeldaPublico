<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarCompetenciaAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`desasociarCompetenciaAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): confirmación sin `<<choice>>` ni advertencia de último elemento; la vista toma la competencia de la ficha ya cargada de la asignatura.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarCompetenciaAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarCompetenciaAsignaturaProgramaView`

**Responsabilidades:**
- presenta la competencia y la asignatura y permite confirmar o cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO`.

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- autoriza la asignatura por su `Programa` y desasocia.

**Colaboraciones:**
- **Entrada:** `DesasociarCompetenciaAsignaturaProgramaView`.
- **Salida:** `CompetenciaRepository`.

## Clases de modelo

### `CompetenciaRepository`

**Responsabilidades:**
- gestiona `Competencia` y sus dos tablas de asociación (`materias_competencias`, `asignaturas_programa_competencias`).

**Colaboraciones:**
- **Entrada:** `CompetenciaController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/wireframes.puml) -- fuente de verdad

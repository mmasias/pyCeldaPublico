<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCompetencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirCompetencia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirCompetencia()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencia/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): detalle de solo lectura de una `Competencia` con su distribución (materias y asignaturas que la tienen asignada).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirCompetencia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirCompetenciaView`

**Responsabilidades:**
- presenta tipo, descripción y la Distribución en dos columnas, con enlace a cada materia y asignatura.
- ofrece la entrada a editar.

**Colaboraciones:**
- **Entrada:** `:COMPETENCIAS_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `:COMPETENCIA_ABIERTO`.

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- autoriza la competencia por su `Programa`.
- carga la competencia y sus asignaciones.

**Colaboraciones:**
- **Entrada:** `AbrirCompetenciaView`.
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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencia/wireframes.puml) -- fuente de verdad

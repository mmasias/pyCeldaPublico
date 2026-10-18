<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCompetencias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencias/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirCompetencias/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirCompetencias()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencias/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): listado de solo lectura del catálogo de `Competencia` del `Programa`, con el número de `AsignaturaPrograma` que tienen asignada cada una. Mismo patrón que `abrirResultadosAprendizaje()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirCompetencias/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirCompetenciasView`

**Responsabilidades:**
- presenta el catálogo (descripción, tipo, código, nº de asignaturas) con entrada a abrir, crear y eliminar.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` (`Admin` o `DirectorPrograma`).
- **Control:** `CompetenciaController`.
- **Salida:** `:COMPETENCIAS_ABIERTO`.

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- autoriza el `Programa` (Admin cualquiera; director, solo los que dirige).
- compone el listado con el conteo de asignaturas por competencia.

**Colaboraciones:**
- **Entrada:** `AbrirCompetenciasView`.
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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencias/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirCompetencias/wireframes.puml) -- fuente de verdad
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Competencia`

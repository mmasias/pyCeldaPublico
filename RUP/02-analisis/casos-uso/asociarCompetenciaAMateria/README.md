<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarCompetenciaAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarCompetenciaAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`asociarCompetenciaAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAMateria/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): primer escalón de la cascada. Disponibles = competencias del `Programa` de la materia aún no asociadas a ella. Al asociar, el controlador comprueba que la competencia es del mismo `Programa` (el id viene del cuerpo) y que no está ya asociada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarCompetenciaAMateria/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarCompetenciaAMateriaView`

**Responsabilidades:**
- presenta la selección de competencias disponibles (`código -- extracto`) y el texto completo de la elegida.
- ofrece asociar.

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- autoriza la materia por su `Programa`.
- rechaza una competencia de otro `Programa` (no encontrada) o ya asociada (conflicto).
- asocia.

**Colaboraciones:**
- **Entrada:** `AsociarCompetenciaAMateriaView`.
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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAMateria/wireframes.puml) -- fuente de verdad
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- regla de subconjunto de `Competencia`

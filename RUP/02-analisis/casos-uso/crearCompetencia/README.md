<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearCompetencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearCompetencia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearCompetencia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`crearCompetencia()`](/RUP/01-requisitos/03-detalle-casos-uso/crearCompetencia/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): formulario de `codigo`, `tipo` (selección cerrada) y `descripcion`, sin patrón C→U, como en el RA. El `<<choice>>` de código repetido lo resuelve el controlador contra el repositorio antes de escribir: si el código ya lo usa otra competencia del `Programa`, el formulario sigue con lo escrito y el mensaje.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearCompetencia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearCompetenciaView`

**Responsabilidades:**
- presenta el formulario: `codigo`, `tipo` (desplegable con los cuatro valores), `descripcion`, los tres obligatorios.
- presenta el mensaje de código repetido sin perder lo escrito.

**Colaboraciones:**
- **Entrada:** `:COMPETENCIAS_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `<<include>>` hacia [`editarCompetencia()`](../editarCompetencia/README.md), `:COMPETENCIA_ABIERTO`.

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- valida que el `codigo` no lo use otra competencia del `Programa`.
- crea la `Competencia`, real e inmediata.

**Colaboraciones:**
- **Entrada:** `CrearCompetenciaView`.
- **Salida:** `CompetenciaRepository`.

## Clases de modelo

### `Competencia`

**Responsabilidades:**
- porta `codigo`, `tipo`, `descripcion`.

**Colaboraciones:**
- **Entrada:** `CompetenciaRepository`.

### `CompetenciaRepository`

**Responsabilidades:**
- gestiona `Competencia` y sus dos tablas de asociación (`materias_competencias`, `asignaturas_programa_competencias`).

**Colaboraciones:**
- **Entrada:** `CompetenciaController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearCompetencia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearCompetencia/wireframes.puml) -- fuente de verdad
- [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md) / [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md) -- patrón de origen

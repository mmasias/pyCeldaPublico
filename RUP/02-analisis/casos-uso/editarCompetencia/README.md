<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarCompetencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarCompetencia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`editarCompetencia()`](/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/README.md) (issue [#761](https://github.com/mmasias/pyCelda/issues/761)): formulario de `codigo`, `tipo` (selección cerrada) y `descripcion`, sin patrón C→U, como en el RA. El `<<choice>>` de código repetido lo resuelve el controlador contra el repositorio antes de escribir: si el código ya lo usa otra competencia del `Programa`, el formulario sigue con lo escrito y el mensaje.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarCompetencia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarCompetenciaView`

**Responsabilidades:**
- presenta el formulario: `codigo`, `tipo` (desplegable con los cuatro valores), `descripcion`, los tres obligatorios.
- presenta el mensaje de código repetido sin perder lo escrito.

**Colaboraciones:**
- **Entrada:** `:COMPETENCIA_ABIERTO`.
- **Control:** `CompetenciaController`.
- **Salida:** `:COMPETENCIA_ABIERTO`.

## Clases de controlador

### `CompetenciaController`

**Responsabilidades:**
- valida que el `codigo` no lo use otra competencia del `Programa`.
- aplica los cambios con `Competencia.actualizar()`.

**Colaboraciones:**
- **Entrada:** `EditarCompetenciaView`.
- **Salida:** `CompetenciaRepository`, `Competencia`.

## Clases de modelo

### `Competencia`

**Responsabilidades:**
- porta `codigo`, `tipo`, `descripcion`. `actualizar()` cambia los tres a la vez.

**Colaboraciones:**
- **Entrada:** `CompetenciaRepository`, `CompetenciaController`.

### `CompetenciaRepository`

**Responsabilidades:**
- gestiona `Competencia` y sus dos tablas de asociación (`materias_competencias`, `asignaturas_programa_competencias`).

**Colaboraciones:**
- **Entrada:** `CompetenciaController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/wireframes.puml) -- fuente de verdad
- [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md) / [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md) -- patrón de origen

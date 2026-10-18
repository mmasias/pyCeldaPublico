<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`crearMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): formulario de `codigo` y `descripcion`, sin patrón C→U, como en `Competencia` pero sin `tipo`. El `<<choice>>` de código repetido lo resuelve el controlador contra el repositorio antes de escribir: si el código ya lo usa otra metodología del `Programa`, el formulario sigue con lo escrito y el mensaje. Hasta #772 el alta pedía además la `Universidad` del catálogo institucional y no comprobaba el código repetido.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearMetodologiaDocenteView`

**Responsabilidades:**
- presenta el formulario: `codigo` y `descripcion` (multilínea), los dos obligatorios.
- presenta el mensaje de código repetido sin perder lo escrito.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_ABIERTO`.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `<<include>>` hacia [`editarMetodologiaDocente()`](../editarMetodologiaDocente/README.md), `:METODOLOGIA_DOCENTE_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- valida que el `codigo` no lo use otra metodología del `Programa`, sin distinguir mayúsculas.
- crea la `MetodologiaDocente`, real e inmediata.

**Colaboraciones:**
- **Entrada:** `CrearMetodologiaDocenteView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion`, los literales de la memoria del `Programa`.

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- gestiona `MetodologiaDocente` y consulta sus dos tablas de asociación (`metodologias_materia`, `asignaturas_programa_metodologias_docentes`).

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/wireframes.puml) -- fuente de verdad
- [`crearCompetencia()`](../crearCompetencia/README.md) -- patrón de origen

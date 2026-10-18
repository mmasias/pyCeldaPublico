<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): detalle de solo lectura de una `MetodologiaDocente` con su distribución (materias y asignaturas que la tienen asignada). Mismo patrón que [`abrirCompetencia()`](../abrirCompetencia/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirMetodologiaDocenteView`

**Responsabilidades:**
- presenta la descripción y la Distribución en dos columnas, con enlace a cada materia y asignatura.
- ofrece la entrada a editar.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_ABIERTO`.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIA_DOCENTE_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- autoriza la metodología por su `Programa`.
- carga la metodología y sus asignaciones.

**Colaboraciones:**
- **Entrada:** `AbrirMetodologiaDocenteView`.
- **Salida:** `MetodologiaDocenteRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo` y `descripcion`, los literales de la memoria del `Programa`.

**Colaboraciones:**
- **Entrada:** gestionada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- gestiona `MetodologiaDocente` y consulta sus dos tablas de asociación (`metodologias_materia`, `asignaturas_programa_metodologias_docentes`).

**Colaboraciones:**
- **Entrada:** `MetodologiaDocenteController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/wireframes.puml) -- fuente de verdad

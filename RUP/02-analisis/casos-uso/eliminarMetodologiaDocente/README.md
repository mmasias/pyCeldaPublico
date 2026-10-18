<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`eliminarMetodologiaDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): el `<<choice>>` de bloqueo se apoya en las asignaciones de la metodología (las mismas que pinta la ficha), y el controlador lo vuelve a comprobar al borrar. Hasta #772 solo bloqueaban las `Materia`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarMetodologiaDocenteView`

**Responsabilidades:**
- presenta la metodología y, según las asignaciones, el bloqueo con las materias y asignaturas que la usan o la confirmación.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_ABIERTO`.
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_ABIERTO` (tres ramas).

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- carga las asignaciones.
- rechaza el borrado si la metodología está asignada a alguna `Materia` o `AsignaturaPrograma` (409 con los nombres); si no, la borra.

**Colaboraciones:**
- **Entrada:** `EliminarMetodologiaDocenteView`.
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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/wireframes.puml) -- fuente de verdad
- [`eliminarCompetencia()`](../eliminarCompetencia/README.md) -- patrón de origen

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentes()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirMetodologiasDocentes()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): listado de solo lectura del catálogo de `MetodologiaDocente` del `Programa`, con el número de `AsignaturaPrograma` que tienen asignada cada una. Mismo patrón que [`abrirCompetencias()`](../abrirCompetencias/README.md). Hasta #772 el listado colgaba de `SISTEMA_DISPONIBLE` y filtraba el catálogo institucional por `Universidad`; el subconjunto habilitado en el `Programa` era otro caso de uso (`abrirMetodologiasDocentesPrograma()`), absorbido por este.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirMetodologiasDocentesView`

**Responsabilidades:**
- presenta el catálogo (descripción, código, nº de asignaturas) con entrada a abrir, crear y eliminar.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` (`Admin` o `DirectorPrograma`).
- **Control:** `MetodologiaDocenteController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_ABIERTO`.

## Clases de controlador

### `MetodologiaDocenteController`

**Responsabilidades:**
- autoriza el `Programa` (Admin cualquiera; director, solo los que dirige).
- compone el listado con el conteo de asignaturas por metodología.

**Colaboraciones:**
- **Entrada:** `AbrirMetodologiasDocentesView`.
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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/wireframes.puml) -- fuente de verdad
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- MetodologiaDocente`
- [`abrirCompetencias()`](../abrirCompetencias/README.md) -- patrón de origen

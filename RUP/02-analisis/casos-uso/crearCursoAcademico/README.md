<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearCursoAcademico()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearCursoAcademico/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearCursoAcademico/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/crearCursoAcademico/README.md): CRUD real e inmediato contra `CursoAcademicoRepository`, el patrón C→U más simple del catálogo -- un único paso, sin `<<choice>>`, sin catálogo del que heredar y sin relación de composición con otra entidad todavía (`CursoAcademico` nace autónomo; la primera mitad de [#222](https://github.com/mmasias/pyCelda/issues/222), ver [discussion #430](https://github.com/mmasias/pyCelda/discussions/430)). Los dos campos obligatorios (`inicio`, `fin`) se piden al crear; `estado` nace `Inactivo` sin pedirlo -- dar de alta no activa, son dos eventos distintos (`crearCursoAcademico()` / `activarCursoAcademico()`, ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)). `semestreActivo` tampoco se fija aquí: es el resultado de `activarSemestre()`, fuera de alcance de esta rebanada.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearCursoAcademico/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearCursoAcademicoView`

**Responsabilidades:**
- presenta el formulario de creación: `inicio`, `fin` -- ambos obligatorios.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:CURSOS_ACADEMICOS_ABIERTO` -- el `Admin` solicita crear un `CursoAcademico`.
- **Control:** `CursoAcademicoController`.
- **Salida:** `:Collaboration EditarCursoAcademico` vía `<<include>> editarCursoAcademico()`.

## Clases de controlador

### `CursoAcademicoController`

**Responsabilidades:**
- valida que `inicio`/`fin` estén presentes (`validarDatosObligatorios(inicio, fin)`).
- crea el `CursoAcademico`, directamente en `CursoAcademicoRepository`, real e inmediato (`crearCursoAcademico(inicio, fin)`).

**Colaboraciones:**
- **Entrada:** `CrearCursoAcademicoView`.
- **Salida:** `CursoAcademicoRepository`.

## Clases de modelo

### `CursoAcademico`

**Responsabilidades:**
- porta `inicio`, `fin`, `estado` (nace `Inactivo`) y `semestreActivo` (nace sin fijar, `null`) desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creada por `CursoAcademicoRepository`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- crea el `CursoAcademico` (`crear(inicio, fin)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** gestiona `CursoAcademico`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearCursoAcademico/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearCursoAcademico/wireframes.puml) -- fuente de verdad del formulario, patrón C→U: solo `inicio`/`fin` al crear.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSOS_ACADEMICOS_ABIERTO --> CURSO_ACADEMICO_ABIERTO : crearCursoAcademico()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `CursoAcademico { inicio, fin, estado, semestreActivo }`; dar de alta y activar son dos eventos distintos.
- [`editarCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/README.md) -- `<<include>>` de salida; ficha de Requisitos cerrada, sin Análisis/Diseño propios todavía (fuera de alcance de esta rebanada).
- [`crearFacultad()` en Análisis](/RUP/02-analisis/casos-uso/crearFacultad/README.md) -- mismo patrón de creación de una sola entidad autónoma, usado como plantilla de este documento.

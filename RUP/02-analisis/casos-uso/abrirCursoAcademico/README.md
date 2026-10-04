<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCursoAcademico()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursoAcademico/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirCursoAcademico/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursoAcademico/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta los datos de un `CursoAcademico` (`inicio`, `fin`, `estado`, `semestreActivo`) y ofrece editarlo, fijar el semestre activo o volver al listado -- es el estado desde el que se alcanzan [`editarCursoAcademico()`](../editarCursoAcademico/README.md) y [`activarSemestre()`](../activarSemestre/README.md). Mismo molde que [`abrirFacultad()`](../abrirFacultad/README.md) (detalle de un elemento de una colección anidada bajo la `Universidad`), con una diferencia deliberada: `[Editar]` está **siempre** presente, sin filtro previo -- el bloqueo por `Guia` asociadas lo resuelve el `<<choice>>` de `editarCursoAcademico()` al solicitarlo, no esta pantalla.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirCursoAcademico/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirCursoAcademicoView`

**Responsabilidades:**
- presenta los datos del `CursoAcademico`: `inicio`, `fin`, `estado` y `semestreActivo` (`--` si no hay semestre fijado).
- ofrece la navegación a editar, a fijar el semestre activo y a volver al listado (`[Editar]`/`[Activar semestre]`/`[Volver a los Cursos académicos]`), sin deshabilitar ninguna por el estado del curso.

**Colaboraciones:**
- **Entrada:** `:CURSOS_ACADEMICOS_ABIERTO` -- el `Admin` solicita abrir un `CursoAcademico` del listado; también alcanzado desde `:CURSO_ACADEMICO_ABIERTO` al volver de `editarCursoAcademico()`/`activarSemestre()`.
- **Control:** `CursoAcademicoController`.
- **Salida:** `:CURSO_ACADEMICO_ABIERTO`.

## Clases de controlador

### `CursoAcademicoController`

**Responsabilidades:**
- recupera el `CursoAcademico` (`cargarCursoAcademico(cursoAcademicoId)`) -- el mismo método que reutilizan `editarCursoAcademico()` y `activarSemestre()` para cargar su formulario.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirCursoAcademicoView`.
- **Salida:** `CursoAcademicoRepository`.

## Clases de modelo

### `CursoAcademico`

**Responsabilidades:**
- porta `inicio`, `fin`, `estado` y `semestreActivo` -- los datos mostrados.

**Colaboraciones:**
- **Entrada:** recuperada por `CursoAcademicoRepository`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- recupera el `CursoAcademico` por identificador (`obtener(cursoAcademicoId)`).

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** gestiona `CursoAcademico`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursoAcademico/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursoAcademico/wireframes.puml) -- fuente de verdad del contenido presentado y de los dos botones de acción.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSOS_ACADEMICOS_ABIERTO --> CURSO_ACADEMICO_ABIERTO : abrirCursoAcademico()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `CursoAcademico { inicio, fin, estado, semestreActivo }`.
- [`abrirFacultad()`](../abrirFacultad/README.md) -- plantilla del detalle de un elemento anidado bajo la `Universidad`.
- [`abrirCursosAcademicos()`](../abrirCursosAcademicos/README.md) -- listado desde el que se alcanza este caso de uso.
- [`editarCursoAcademico()`](../editarCursoAcademico/README.md) / [`activarSemestre()`](../activarSemestre/README.md) -- destinos de `[Editar]` y `[Activar semestre]`.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCursosAcademicos()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirCursosAcademicos()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md): un solo paso, sin `<<choice>>` de bloqueo, de solo lectura. Presenta el listado de `CursoAcademico` de una `Universidad` concreta -- cada institución tiene su propio plan de cursos (issue [#471](https://github.com/mmasias/pyCelda/issues/471)), así que el filtro por `Universidad` vive en la consulta, no en la sesión. Mismo molde que [`abrirFacultades()`](../abrirFacultades/README.md) (listado de una colección que cuelga de la `Universidad`), con una diferencia real: cada fila lleva dos datos **derivados** que decide el controlador, no la fila persistida -- si se ofrece `[Activar]` (la elegibilidad de [`activarCursoAcademico()`](../activarCursoAcademico/README.md), evaluada aquí para no presentar botones siempre bloqueados: mismo criterio de "validar antes de presentar" que `eliminarFacultad()`) y si el curso ya tiene alguna `Guia` asociada (dato que consume [`editarCursoAcademico()`](../editarCursoAcademico/README.md) para abrir en modo formulario o bloqueado sin tentar el `PUT`). Es el estado de partida de [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md), `crearCursoAcademico()` y `activarCursoAcademico()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirCursosAcademicos/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirCursosAcademicosView`

**Responsabilidades:**
- presenta el listado de `CursoAcademico` de la `Universidad`: curso (`inicio`-`fin`), `estado` y `semestreActivo` de cada fila.
- ofrece por fila `[Abrir]` (siempre -- consultar el detalle no está sujeto a ningún `<<choice>>`) y `[Activar]` solo en las filas elegibles; ofrece además `[+ Crear Curso Académico]` y la vuelta al panel de administración.
- el selector de `Universidad` (primera preseleccionada) es de la propia pantalla y se alimenta de [`abrirUniversidades()`](../abrirUniversidades/README.md); no es una colaboración de este caso de uso.

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita abrir los Cursos académicos; también `:CURSO_ACADEMICO_ABIERTO` (vuelta desde el detalle de un curso).
- **Control:** `CursoAcademicoController`.
- **Salida:** `:CURSOS_ACADEMICOS_ABIERTO`.

## Clases de controlador

### `CursoAcademicoController`

**Responsabilidades:**
- lista los `CursoAcademico` de una `Universidad` (`listarCursosAcademicosDeLaUniversidad(universidadId)`).
- por cada fila, resuelve los dos datos derivados: si es elegible para activar (`esElegibleParaActivar(cursoAcademicoId)`) y si tiene alguna `Guia` asociada (`tieneGuiaAsociada()`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirCursosAcademicosView`.
- **Salida:** `CursoAcademicoRepository`, `CursoAcademico`.

## Clases de modelo

### `CursoAcademico`

**Responsabilidades:**
- porta `inicio`, `fin`, `estado` y `semestreActivo` -- los datos mostrados en cada fila.
- responde si tiene alguna `Guia` asociada (`tieneGuiaAsociada()`) -- la misma consulta que el `<<choice>>` bloqueante de `editarCursoAcademico()`.

**Colaboraciones:**
- **Entrada:** listada por `CursoAcademicoRepository`; consultada por `CursoAcademicoController`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- lista los `CursoAcademico` de una `Universidad` (`listarDeLaUniversidad(universidadId)`), en orden de alta (`id` ascendente) -- el mismo orden que la regla "último/penúltimo" de `activarCursoAcademico()`.
- responde si un curso es elegible para activar (`esElegibleParaActivar(cursoAcademicoId)`): regla del `<<choice>>` de `activarCursoAcademico()` (último en estado `Inactivo`, o penúltimo si el último no tiene actividad registrada), reutilizada sin reescribirla.

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** gestiona `CursoAcademico`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/wireframes.puml) -- fuente de verdad del listado, incluido el criterio de cuándo aparece `[Activar]`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> CURSOS_ACADEMICOS_ABIERTO : abrirCursosAcademicos()`, `CURSO_ACADEMICO_ABIERTO --> CURSOS_ACADEMICOS_ABIERTO : abrirCursosAcademicos()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad -- CursoAcademico`; regla de `estado`/elegibilidad de activación.
- [`abrirFacultades()`](../abrirFacultades/README.md) -- plantilla del listado de una colección anidada bajo la `Universidad`.
- [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md) / [`activarCursoAcademico()`](../activarCursoAcademico/README.md) / [`crearCursoAcademico()`](../crearCursoAcademico/README.md) -- casos de uso alcanzados desde el listado.

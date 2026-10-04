<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > activarSemestre()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/activarSemestre/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`activarSemestre()`](/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/README.md): edición simple de un único atributo (`CursoAcademico.semestreActivo`, 1 o 2), CRUD real e inmediato contra `CursoAcademicoRepository`. **Sin `<<choice>>`** -- aplica sobre cualquier `CursoAcademico`, `Activo` o `Inactivo`, sin ninguna precondición que bloquee; no hay evento simétrico de "desactivar semestre", el valor nuevo sustituye al anterior en la misma fila. Por eso el molde es el de [`editarPrograma()`](../editarPrograma/README.md)/[`editarUniversidad()`](../editarUniversidad/README.md) (edición sin `<<choice>>` de negocio), no el de [`activarCursoAcademico()`](../activarCursoAcademico/README.md), pese al verbo compartido: aquel es una acción de conjunto sobre el listado con elegibilidad y efecto colateral masivo; este es un formulario de un campo sobre un curso ya abierto (Requisitos lo fija explícitamente como "mismo molde que `editarUniversidad()`"). El semestre nunca se infiere de la fecha de hoy: es un evento explícito del `Admin`, mismo criterio que `CursoAcademico.estado`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/activarSemestre/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ActivarSemestreView`

**Responsabilidades:**
- presenta el `semestreActivo` actual del `CursoAcademico` (`--` si aún no hay ninguno) y el formulario con dos opciones excluyentes, 1 y 2; siempre hay una preseleccionada (el actual si es 2, 1 en cualquier otro caso) -- no existe el estado "sin seleccionar".
- permite solicitar guardar o cancelar.

**Colaboraciones:**
- **Entrada:** `:CURSO_ACADEMICO_ABIERTO` -- el `Admin` solicita fijar el semestre activo del `CursoAcademico` abierto (botón `[Activar semestre]` de [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md)).
- **Control:** `CursoAcademicoController`.
- **Salida:** `:CURSO_ACADEMICO_ABIERTO`.

## Clases de controlador

### `CursoAcademicoController`

**Responsabilidades:**
- recupera el `CursoAcademico` a editar (`cargarCursoAcademico(cursoAcademicoId)`, mismo método introducido por [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md)).
- guarda el semestre (`guardarSemestre(cursoAcademicoId, semestre)`): sin `<<choice>>` de negocio que aplicar -- pide directamente al `CursoAcademico` que fije el valor y persiste.

**Colaboraciones:**
- **Entrada:** `ActivarSemestreView`.
- **Salida:** `CursoAcademico`, `CursoAcademicoRepository`.

## Clases de modelo

### `CursoAcademico`

**Responsabilidades:**
- porta `semestreActivo`.
- se actualiza a sí mismo (`activarSemestre(semestre)`) -- mismo patrón que `Universidad.actualizar(nombre)`.

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** persistido por `CursoAcademicoRepository`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- recupera el `CursoAcademico` por identificador (`obtener(cursoAcademicoId)`).
- persiste la actualización (`actualizar(cursoAcademico)`) -- método compartido con [`editarCursoAcademico()`](../editarCursoAcademico/README.md).

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** gestiona `CursoAcademico`.

## Fuera de alcance de esta rebanada

El **efecto** de `semestreActivo` -- "las notificaciones dirigidas al profesor se filtran por `Guia.semestre == CursoAcademico.semestreActivo`" ([modelo del dominio](/RUP/00-modelo-del-dominio/README.md)) -- no es parte de este caso de uso: aquí solo se fija el valor; no es una relación estructural, es una condición de filtrado en el envío.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/wireframes.puml) -- fuente de verdad del formulario (dos radio buttons, sin rama de rechazo).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSO_ACADEMICO_ABIERTO --> CURSO_ACADEMICO_ABIERTO : activarSemestre()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `CursoAcademico.semestreActivo`.
- [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md) -- mismo `CursoAcademicoController.cargarCursoAcademico(cursoAcademicoId)`, reutilizado; origen del botón.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio.
- [`editarPrograma()`](../editarPrograma/README.md) -- plantilla de formato de la ficha.
- [`editarCursoAcademico()`](../editarCursoAcademico/README.md) -- hermano que comparte `obtener()`/`actualizar()`, pero sí con `<<choice>>` bloqueante.

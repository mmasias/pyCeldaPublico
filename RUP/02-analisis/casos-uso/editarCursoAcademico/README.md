<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarCursoAcademico()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarCursoAcademico/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/README.md): corregir `inicio`/`fin` de un `CursoAcademico`, con un `<<choice>>` **bloqueante** -- si el curso ya tiene alguna `Guia` asociada no se puede editar (discussion [#15](https://github.com/mmasias/pyCelda/discussions/15)). Es la primera vez que el patrón bloqueante, hasta ahora exclusivo de `eliminarX()` ([`eliminarFacultad()`](../eliminarFacultad/README.md)), se aplica a **editar**: mismo criterio relacional que bloquea `eliminarProfesor()`/`eliminarFacultad()`, aquí sobre una edición. No existe `eliminarCursoAcademico()` en el catálogo -- corregir un error de fecha es editar, no borrar y recrear. A diferencia de [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md), donde el `<<choice>>` solo bifurca la presentación de un campo de ocho, aquí bloquea el caso de uso **entero** (ambos campos editables quedan fijos, el formulario no se ofrece). El molde de formato es el de [`editarPrograma()`](../editarPrograma/README.md); el de la rama de bloqueo, el de `eliminarFacultad()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarCursoAcademico/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarCursoAcademicoView`

**Responsabilidades:**
- en la rama verde (sin `Guia` asociadas), presenta el formulario con `inicio` y `fin` editables y permite solicitar guardar o cancelar.
- en la rama roja (con `Guia` asociadas), presenta el mensaje de bloqueo -- "NO SE PUEDE EDITAR", con el motivo -- sin formulario.

**Colaboraciones:**
- **Entrada:** `:CURSO_ACADEMICO_ABIERTO` -- el `Admin` solicita editar el `CursoAcademico` abierto (botón `[Editar]` de [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md), siempre presente).
- **Control:** `CursoAcademicoController`.
- **Salida:** `:CURSO_ACADEMICO_ABIERTO` en ambos casos -- "datos actualizados" (verde) o "bloqueado, sin cambios" (rojo).

## Clases de controlador

### `CursoAcademicoController`

**Responsabilidades:**
- recupera el `CursoAcademico` a editar (`cargarCursoAcademico(cursoAcademicoId)`, mismo método introducido por [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md)).
- aplica el `<<choice>>`: pregunta si tiene `Guia` asociadas (`puedeEditar(cursoAcademicoId)`) **antes** de ofrecer el formulario y de tocar el modelo -- no hay escritura parcial.
- si no está bloqueado, guarda los cambios (`guardarCambios(cursoAcademicoId, inicio, fin)`): pide al `CursoAcademico` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarCursoAcademicoView`.
- **Salida:** `CursoAcademico`, `CursoAcademicoRepository`.

## Clases de modelo

### `CursoAcademico`

**Responsabilidades:**
- porta `inicio` y `fin`; ambos editables mientras no haya `Guia` asociadas. `estado` y `semestreActivo` quedan fuera del formulario (los gestionan [`activarCursoAcademico()`](../activarCursoAcademico/README.md) y [`activarSemestre()`](../activarSemestre/README.md)).
- responde si tiene alguna `Guia` asociada (`tieneGuiaAsociada()`) -- origen de la regla de bloqueo; la consulta recorre su propia relación con `Guia`, sin repositorio propio para esa comprobación.
- se actualiza a sí mismo (`actualizar(inicio, fin)`).

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** persistido por `CursoAcademicoRepository`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- recupera el `CursoAcademico` por identificador (`obtener(cursoAcademicoId)`).
- persiste la actualización (`actualizar(cursoAcademico)`) -- método compartido con [`activarSemestre()`](../activarSemestre/README.md).

**Colaboraciones:**
- **Entrada:** `CursoAcademicoController`.
- **Salida:** gestiona `CursoAcademico`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante y de las dos variantes de pantalla (editable / bloqueada).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSO_ACADEMICO_ABIERTO --> CURSO_ACADEMICO_ABIERTO : editarCursoAcademico()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `CursoAcademico.estado`: corregir `inicio`/`fin` es `editarCursoAcademico()`, bloqueado si el curso tiene alguna `Guia` asociada.
- [`editarPrograma()`](../editarPrograma/README.md) -- plantilla de formato (edición simple de un recurso con carga previa).
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- plantilla del `<<choice>>` bloqueante, aquí aplicado a editar.
- [`editarAsignaturaPrograma()`](../editarAsignaturaPrograma/README.md) -- contraste: `<<choice>>` que bifurca un campo, no el caso de uso entero.
- [`abrirCursoAcademico()`](../abrirCursoAcademico/README.md) -- origen del botón y mismo `cargarCursoAcademico(cursoAcademicoId)`.

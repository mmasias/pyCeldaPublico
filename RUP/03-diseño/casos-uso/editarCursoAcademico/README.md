<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarCursoAcademico() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarCursoAcademico/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarCursoAcademico()`](/RUP/02-analisis/casos-uso/editarCursoAcademico/README.md): `PUT /api/v1/admin/cursos-academicos/{curso_academico_id}` con `<<choice>>` bloqueante resuelto en el Router por un método de consulta del Modelo (`CursoAcademico.tiene_guia_asociada()`), que el Router traduce a HTTP `400` -- **sin excepciones de dominio**, mismo criterio que [`activarCursoAcademico()`](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md) y [`eliminarFacultad()`](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md). Primera aplicación del patrón bloqueante a una edición (discussion [#15](https://github.com/mmasias/pyCelda/discussions/15)). El bloqueo se comprueba antes de mutar el modelo: no hay escritura parcial.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarCursoAcademico/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarCursoAcademicoView` (`EditarCursoAcademicoAdmin.tsx`, `/admin/cursos-academicos/:id/editar`) -- carga el curso con `buscarCursoAcademicoAdminPorId(id)` (listado de gestión de [`abrirCursosAcademicos()`](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md), buscado en el cliente) y **resuelve el `<<choice>>` al cargar** con `tiene_guia_asociada` de esa respuesta: con `Guia` asociadas, presenta la variante bloqueada sin formulario y sin tentar el `PUT`; si no, presenta `<input type="date">` para `inicio`/`fin` y envía con `PUT`. Tras guardar, navega al detalle del curso.
- **API**: `routers/curso_academico.py::editar_curso_academico(curso_academico_id, datos)` -- función suelta; verifica existencia (`404`), aplica el bloqueo (`400`) y solo entonces actualiza.
- **Modelo**: `CursoAcademico.tiene_guia_asociada()` (consulta de la relación ORM `guias`) y `CursoAcademico.actualizar(inicio, fin)`.
- **Repositorio**: `CursoAcademicoRepository.obtener(curso_academico_id)` (reutilizado); `.actualizar(curso)` -- `commit()` + `refresh()`, compartido con `activarSemestre()`.
- **Schema**: `CursoAcademicoUpdate` (`inicio: date`, `fin: date`), fichero propio aunque comparta forma con `CursoAcademicoCreate` -- el proyecto usa siempre `XCreate`/`XUpdate` separados.

## Decisiones de diseño

- **`<<choice>>` bloqueante, sin excepción de dominio**: `tiene_guia_asociada()` devuelve `bool`; el Router decide `404` (no existe) / `400` (con `Guia` asociadas) / actualiza. El código de estado del bloqueo es `400`, no `409` como en `activarCursoAcademico()`: es lo que implementa el Router, y la Vista lo trata como "bloqueo" al recibirlo (ver abajo).
- **Doble comprobación del bloqueo, a propósito**: la Vista lo resuelve al cargar (para no ofrecer un formulario que se sabe condenado) **y** el Router lo vuelve a comprobar en el `PUT` -- una `Guia` puede nacer entre la carga y el envío (p.ej. un `activarCursoAcademico()` concurrente). Si el `PUT` devuelve `400`, la Vista cambia a la variante bloqueada con el motivo del servidor (`detail`). La protección real vive en el servidor, no en la Vista.
- **Se bloquea el caso de uso entero, no un campo**: contraste con `editarAsignaturaPrograma()`, cuyo `<<choice>>` solo afecta a `semestreDefault`. Aquí `inicio` y `fin` son los únicos campos editables y ambos quedan fijos una vez el curso tiene actividad.
- **Sin validación cruzada `inicio` < `fin`**: `CursoAcademicoUpdate` solo valida forma (dos fechas obligatorias); el Router no comprueba el orden entre ellas, igual que el alta (`CursoAcademicoCreate`).
- **`estado`/`semestre_activo` no viajan en el esquema**: la edición no puede mutarlos; los gestionan `activarCursoAcademico()` y `activarSemestre()`.
- **Sin `GET` previo propio**: la carga reutiliza el listado de gestión, que ya trae `tiene_guia_asociada` calculado por el Router (`_fila_admin()`), decisión del issue [#454](https://github.com/mmasias/pyCelda/issues/454) -- mismo criterio de "el `<<choice>>` se resuelve antes de mostrar el formulario" que `semestre_default_bloqueado` en `editarAsignaturaPrograma()`.
- **Sin capa Service**: Router delgado -> Modelo/Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de escritura; el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`editarCursoAcademico()` en Análisis](/RUP/02-analisis/casos-uso/editarCursoAcademico/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/README.md).
- [`editarPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarPrograma/README.md) -- plantilla de `GET` previo + `PUT` sin `alt` de negocio (aquí con `alt` bloqueante añadido).
- [`eliminarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md) -- plantilla del `<<choice>>` bloqueante sin excepción de dominio.
- [`activarCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md) -- mismo molde de `404` + bloqueo, con `409` en vez de `400`.
- [`abrirCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/abrirCursoAcademico/README.md) -- mecanismo de carga reutilizado y origen del botón.
- [`activarSemestre()` en Diseño](/RUP/03-diseño/casos-uso/activarSemestre/README.md) -- comparte `obtener()`/`actualizar()` del repositorio.

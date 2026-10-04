<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCursosAcademicos() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirCursosAcademicos/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirCursosAcademicos()`](/RUP/02-analisis/casos-uso/abrirCursosAcademicos/README.md): un solo paso, de solo lectura. `GET /api/v1/universidades/{universidad_id}/cursos-academicos` -- la colección cuelga de la `Universidad` en la URL (misma decisión que [`abrirFacultades()`](/RUP/03-diseño/casos-uso/abrirFacultades/README.md)), y cada fila se construye explícitamente con dos campos derivados (`elegible_para_activar`, `tiene_guia_asociada`) que ni la fila ORM ni `CursoAcademicoResponse` poseen. `CursoAcademicoController` converge en `routers/curso_academico.py`, función suelta, sin capa Service.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirCursosAcademicos/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirCursosAcademicosView` (`CursosAcademicosAdmin.tsx`, `/admin/cursos-academicos`) -- carga primero las `Universidad` (`listarUniversidades()`), preselecciona la primera y pide `GET /api/v1/universidades/{universidad_id}/cursos-academicos`; presenta curso, estado y semestre activo por fila, con `[Abrir]` siempre y `[Activar]` solo si `elegible_para_activar`.
- **API**: `routers/curso_academico.py::listar_cursos_academicos(universidad_id)` -- función suelta; el helper privado `_fila_admin(repo, curso)` construye `CursoAcademicoAdminResponse` campo a campo.
- **Modelo**: `CursoAcademico.tiene_guia_asociada()` -- consulta la relación ORM `guias` (`len(self.guias) > 0`).
- **Repositorio**: `CursoAcademicoRepository.listar(universidad_id)` -- `SELECT` filtrado por `universidad_id`, `ORDER BY id ASC`; `CursoAcademicoRepository.es_elegible_para_activar(curso_academico_id)` -- la regla del `<<choice>>` de `activarCursoAcademico()`, reutilizada tal cual.

## Decisiones de diseño

- **Ruta anidada bajo la `Universidad`**: `GET /api/v1/universidades/{universidad_id}/cursos-academicos`, no un plano `/api/v1/cursos-academicos?universidad_id=...` -- la composición del modelo de dominio se expresa en la URL (issue [#471](https://github.com/mmasias/pyCelda/issues/471): cada `Universidad` tiene su propio plan de cursos).
- **Dos endpoints distintos sobre la misma colección, no confundirlos**: este (`require_admin`, listado de gestión, con campos derivados) y `GET /api/v1/cursos-academicos` (`listar_cursos_academicos_selector()`), el `<select>` de solo lectura de `Admin`+`DirectorPrograma` que consumen [`consultarEstadoGuias()`](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) y [`consultarHistorialCambios()`](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md), sin los campos derivados. `CursoAcademicoResponse` no se toca; `CursoAcademicoAdminResponse` lo extiende solo para este listado (issue [#446](https://github.com/mmasias/pyCelda/issues/446)).
- **Datos derivados calculados en el Router, no persistidos**: `elegible_para_activar` cambia en tiempo real (depende de si el último curso gana actividad registrada), así que no puede ser una columna ni cachearse. `tiene_guia_asociada` se entrega ya resuelto para que la pantalla de `editarCursoAcademico()` decida formulario o bloqueo sin tentar el `PUT` (issue [#454](https://github.com/mmasias/pyCelda/issues/454)).
- **Coste por fila, conocido y no corregido aquí**: `es_elegible_para_activar()` (`ultimo()`/`penultimo()` y, a veces, `tiene_actividad_registrada()`) y `tiene_guia_asociada()` (carga perezosa de `guias`) se evalúan por cada `CursoAcademico` del listado -- el tamaño real es de un puñado de cursos por institución, así que no se ha optimizado.
- **Sin `404` si la `Universidad` no existe**: la ruta devuelve lista vacía, no valida existencia de la `Universidad` -- el identificador siempre sale del selector de la propia pantalla, que se alimenta del listado real.
- **Sin `<<choice>>` de bloqueo**: ninguna precondición puede rechazar esta lectura -- una `Universidad` sin cursos es un estado válido (lista vacía, `200`).
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de gestión de `Admin`, sin pertenencia que verificar. El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`abrirCursosAcademicos()` en Análisis](/RUP/02-analisis/casos-uso/abrirCursosAcademicos/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md).
- [`abrirFacultades()` en Diseño](/RUP/03-diseño/casos-uso/abrirFacultades/README.md) -- plantilla del listado anidado bajo la `Universidad`.
- [`activarCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md) -- origen de la regla `es_elegible_para_activar()` evaluada por fila.
- [`editarCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/editarCursoAcademico/README.md) -- consumidor de `tiene_guia_asociada`.
- [`abrirCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/abrirCursoAcademico/README.md) -- reutiliza este mismo `GET` como fuente del detalle.

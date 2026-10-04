<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > activarSemestre() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/README.md)|[Análisis](/RUP/02-analisis/casos-uso/activarSemestre/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`activarSemestre()`](/RUP/02-analisis/casos-uso/activarSemestre/README.md): CRUD real e inmediato, `PUT /api/v1/admin/cursos-academicos/{curso_academico_id}/semestre`, sin ninguna llamada a otra entidad. Sin `alt` de negocio -- la única validación es de forma (`semestre` en `{1, 2}`), resuelta por Pydantic con `Literal[1, 2]` (`422` automático). `CursoAcademico` gana aquí su método `activar_semestre(semestre)`, simétrico a `Universidad.actualizar(nombre)`. Mismo molde que [`editarUniversidad()`](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) en su parte de `PUT`; la carga previa, en cambio, no tiene `GET` propio (ver abajo).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/activarSemestre/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ActivarSemestreView` (`ActivarSemestreCursoAcademicoAdmin.tsx`, `/admin/cursos-academicos/:id/semestre`) -- carga el curso con `buscarCursoAcademicoAdminPorId(id)` (el listado de gestión de [`abrirCursosAcademicos()`](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md), buscado en el cliente, ver [`abrirCursoAcademico()`](/RUP/03-diseño/casos-uso/abrirCursoAcademico/README.md)); presenta dos radio buttons (1/2) con el semestre actual preseleccionado; envía el cambio con `PUT` y, al terminar, navega al detalle del curso (`/admin/cursos-academicos/:id`).
- **API**: `routers/curso_academico.py::activar_semestre(curso_academico_id, datos)` -- función suelta; sin validación de negocio, solo coordina la actualización. Comentario explícito en el Router: sin ninguna precondición de estado, no añadir chequeos.
- **Modelo**: `CursoAcademico.activar_semestre(semestre)` -- asigna `semestre_activo`.
- **Repositorio**: `CursoAcademicoRepository.obtener(curso_academico_id)` (reutilizado); `.actualizar(curso)` -- `commit()` + `refresh()`, compartido con `editarCursoAcademico()` (el modelo ya mutó sus atributos antes de llegar al repositorio, mismo patrón que `GuiaRepository.actualizar()`).

## Decisiones de diseño

- **Sin `alt` de negocio, a diferencia de `editarCursoAcademico()` y `activarCursoAcademico()`**: ninguna precondición rechaza el cambio. Aplica igual sobre un curso `Activo` que `Inactivo`, con o sin `Guia` asociadas -- el `semestre_activo` no condiciona la integridad de las `Guia` (solo filtra notificaciones, fuera de este caso de uso).
- **`Literal[1, 2]` en `SemestreActivoRequest`, no una validación en el Router**: primer `Literal` del proyecto para este campo; los dos radio buttons del wireframe son los únicos valores posibles y cualquier otro (`0`, `3`, texto) devuelve `422` sin lógica propia.
- **Sin evento simétrico "desactivar semestre"**: `semestre_activo` es `nullable` en la columna (`--` en la UI mientras no se haya fijado nunca), pero ningún caso de uso lo devuelve a `None`; el valor nuevo solo sustituye al anterior.
- **Nunca inferido de la fecha de hoy**: `semestre_activo` es un evento explícito del `Admin`, no se calcula a partir de `inicio`/`fin` del curso.
- **`PUT`, no `PATCH` ni `POST`**: sustituye un único atributo de un recurso ya existente, idempotente (repetir el mismo valor deja la fila igual) -- ruta propia `/semestre` colgando del curso, bajo el prefijo `/admin/` de las escrituras de `Admin`.
- **Sin `GET` previo propio**: la carga reutiliza el listado de gestión; la pantalla no reconsulta tras el `PUT`, navega al detalle, que vuelve a cargar.
- **`404` si el identificador no existe** (`CursoAcademico no encontrado`) -- guardia de Router sobre el `None` del repositorio.
- **Sin capa Service**: Router delgado -> Modelo/Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de escritura; el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`activarSemestre()` en Análisis](/RUP/02-analisis/casos-uso/activarSemestre/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/README.md).
- [`editarUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) -- plantilla de `PUT` sin `alt` de negocio.
- [`editarPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarPrograma/README.md) -- plantilla de formato de la ficha.
- [`abrirCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/abrirCursoAcademico/README.md) -- mecanismo de carga reutilizado y origen del botón.
- [`editarCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/editarCursoAcademico/README.md) -- comparte `obtener()`/`actualizar()` del repositorio.

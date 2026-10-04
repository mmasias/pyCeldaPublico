<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCursoAcademico() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursoAcademico/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirCursoAcademico/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirCursoAcademico()`](/RUP/02-analisis/casos-uso/abrirCursoAcademico/README.md): un solo paso, de solo lectura. **No existe `GET /api/v1/cursos-academicos/{id}`**: la Vista reutiliza el `GET` de gestión de [`abrirCursosAcademicos()`](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md) y localiza el curso por `id` en el cliente, recorriendo las `Universidad` una a una (`buscarCursoAcademicoAdminPorId()`). Es una decisión de diseño asumida (issue [#454](https://github.com/mmasias/pyCelda/issues/454)), distinta del patrón `abrirFacultad()`, que sí tiene su `GET` propio por identificador -- el diagrama de secuencia refleja el comportamiento real, no el de la plantilla.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirCursoAcademico/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirCursoAcademicoView` (`AbrirCursoAcademicoAdmin.tsx`, `/admin/cursos-academicos/:id`) -- llama a `buscarCursoAcademicoAdminPorId(id)` (`api.ts`); presenta `inicio`, `fin`, `estado` y `semestre_activo`, con `[Editar]`, `[Activar semestre]` y `[Volver a los Cursos académicos]`. Si el `id` no es un entero positivo o no aparece en ninguna `Universidad`, presenta "Curso académico no encontrado" sin llamar a un `404` de servidor.
- **API**: `routers/curso_academico.py::listar_cursos_academicos(universidad_id)` -- la misma función de `abrirCursosAcademicos()`, una llamada por `Universidad` hasta encontrar el curso.
- **Modelo**: ninguno con lógica propia invocada -- `CursoAcademico` solo porta los datos presentados.
- **Repositorio**: `CursoAcademicoRepository.listar(universidad_id)` (reutilizado).

## Decisiones de diseño

- **Sin endpoint de detalle individual, búsqueda en el cliente**: el identificador de `CursoAcademico` es global, pero la API solo expone la colección por `Universidad`. `buscarCursoAcademicoAdminPorId()` pide `listarUniversidades()` y recorre secuencialmente `listarCursosAcademicosAdmin(universidad.id)` hasta dar con el `id` -- no `Promise.all`: con una sola `Universidad` real son dos peticiones y el caso de varias es backlog de gestión, no una pantalla de alto tráfico. Devuelve también el resto de cursos de la misma `Universidad`, dato que necesita [`activarCursoAcademico()`](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md) y que aquí no se usa.
- **El `404` es de la Vista, no del servidor**: no hay ruta que falle por identificador desconocido; `null` en `buscarCursoAcademicoAdminPorId()` se traduce a la pantalla "Curso académico no encontrado". Este caso de uso no define un código de estado propio.
- **`[Editar]` y `[Activar semestre]` sin `disabled` ni condición**: el bloqueo de `editarCursoAcademico()` por `Guia` asociadas se resuelve en esa pantalla al cargar (`tiene_guia_asociada` del mismo listado), no como filtro previo aquí -- decisión de Requisitos.
- **Reutiliza los datos derivados del listado sin mostrarlos**: la respuesta incluye `elegible_para_activar` y `tiene_guia_asociada` (`CursoAcademicoAdminResponse`), que esta pantalla no presenta.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** -- heredada del endpoint reutilizado; un `401`/`403` redirige a `/admin/login`.

## Referencias

- [`abrirCursoAcademico()` en Análisis](/RUP/02-analisis/casos-uso/abrirCursoAcademico/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursoAcademico/README.md).
- [`abrirCursosAcademicos()` en Diseño](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md) -- el `GET` que este caso de uso reutiliza.
- [`abrirFacultad()` en Diseño](/RUP/03-diseño/casos-uso/abrirFacultad/README.md) -- plantilla de forma del detalle (que sí tiene `GET` por identificador, a diferencia de este).
- [`editarCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/editarCursoAcademico/README.md) / [`activarSemestre()` en Diseño](/RUP/03-diseño/casos-uso/activarSemestre/README.md) -- mismo mecanismo de carga, destinos de los botones.

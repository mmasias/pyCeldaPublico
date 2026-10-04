<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`asociarResultadoAprendizajeAAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md): sin `<<choice>>` -- segundo escalón de la cascada `ResultadoAprendizaje`, mismo patrón que `asociarMetodologiaDocenteAAsignaturaPrograma()`. La regla de consistencia (solo RA ya asignados a la `Materia`) vive en la consulta de disponibles; el `POST` inserta en la tabla intermedia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarResultadoAprendizajeAAsignaturaProgramaView` (React) -- selector del subconjunto válido; pide `GET .../disponibles` y `POST /api/v1/asignaturas-programa/{asignatura_programa_id}/resultados-aprendizaje`.
- **API**: `routers/asignatura_programa.py::listar_resultados_aprendizaje_disponibles(asignatura_programa_id)` / `::asociar_resultado_aprendizaje(asignatura_programa_id, datos)` -- funciones sueltas.
- **Modelo**: `AsignaturaPrograma` gana un `ResultadoAprendizaje` en su colección -- sin método invocado.
- **Repositorio**: `ResultadoAprendizajeRepository.listar_disponibles_para_asignatura_programa(asignatura_programa_id)` -- regla de consistencia en la consulta; `AsignaturaProgramaRepository.asociar_resultado_aprendizaje(asignatura_programa_id, resultado_aprendizaje_id)` -- `INSERT` en `asignaturas_programa_resultados_aprendizaje`.

## Decisiones de diseño

- **El listado de disponibles lo firma `ResultadoAprendizajeRepository`** (igual que su gemelo de `MetodologiaDocente` lo firmaba `MetodologiaDocenteRepository`): consulta filas de `resultados_aprendizaje`, el agregado que devuelve -- aunque el criterio ("ya en la `Materia`, no aún en la `AsignaturaPrograma`") atraviese tablas ajenas.
- **El `POST` persiste en `AsignaturaProgramaRepository`** -- la tabla intermedia es dominio del agregado `AsignaturaPrograma`, misma convención que el resto de asociaciones simples de este lote.
- **204 No Content** y cuerpo mínimo (`AsociarResultadoAprendizajeCreate` solo transporta `resultado_aprendizaje_id`).

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: endpoint espejo bajo `/api/v1/admin/...` (`GET`/`POST /api/v1/admin/asignaturas-programa/{id}/resultados-aprendizaje[/disponibles]`), autenticado con `require_admin` en vez de `get_current_director_programa_id` + comprobación de propiedad; reutiliza sin cambios los mismos métodos de repositorio. La secuencia es idéntica con `Admin` como actor.

## Referencias

- [`asociarResultadoAprendizajeAAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md).
- [`asociarResultadoAprendizajeAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAMateria/README.md) -- primer escalón de la misma cascada.
- [`desasociarResultadoAprendizajeAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- caso de uso complementario.

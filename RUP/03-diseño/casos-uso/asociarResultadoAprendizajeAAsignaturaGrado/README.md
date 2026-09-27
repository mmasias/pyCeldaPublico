<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`asociarResultadoAprendizajeAAsignaturaGrado()`](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md): sin `<<choice>>` -- segundo escalón de la cascada `ResultadoAprendizaje`, mismo patrón que `asociarMetodologiaDocenteAAsignaturaGrado()`. La regla de consistencia (solo RA ya asignados a la `Materia`) vive en la consulta de disponibles; el `POST` inserta en la tabla intermedia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AsociarResultadoAprendizajeAAsignaturaGradoView` (React) -- selector del subconjunto válido; pide `GET .../disponibles` y `POST /api/v1/asignaturas-grado/{asignatura_grado_id}/resultados-aprendizaje`.
- **API**: `routers/asignatura_grado.py::listar_resultados_aprendizaje_disponibles(asignatura_grado_id)` / `::asociar_resultado_aprendizaje(asignatura_grado_id, datos)` -- funciones sueltas.
- **Modelo**: `AsignaturaGrado` gana un `ResultadoAprendizaje` en su colección -- sin método invocado.
- **Repositorio**: `ResultadoAprendizajeRepository.listar_disponibles_para_asignatura_grado(asignatura_grado_id)` -- regla de consistencia en la consulta; `AsignaturaGradoRepository.asociar_resultado_aprendizaje(asignatura_grado_id, resultado_aprendizaje_id)` -- `INSERT` en `asignaturas_grado_resultados_aprendizaje`.

## Decisiones de diseño

- **El listado de disponibles lo firma `ResultadoAprendizajeRepository`** (igual que su gemelo de `MetodologiaDocente` lo firmaba `MetodologiaDocenteRepository`): consulta filas de `resultados_aprendizaje`, el agregado que devuelve -- aunque el criterio ("ya en la `Materia`, no aún en la `AsignaturaGrado`") atraviese tablas ajenas.
- **El `POST` persiste en `AsignaturaGradoRepository`** -- la tabla intermedia es dominio del agregado `AsignaturaGrado`, misma convención que el resto de asociaciones simples de este lote.
- **204 No Content** y cuerpo mínimo (`AsociarResultadoAprendizajeCreate` solo transporta `resultado_aprendizaje_id`).

## Referencias

- [`asociarResultadoAprendizajeAAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md).
- [`asociarResultadoAprendizajeAMateria()` en Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAMateria/README.md) -- primer escalón de la misma cascada.
- [`desasociarResultadoAprendizajeAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md) -- caso de uso complementario.

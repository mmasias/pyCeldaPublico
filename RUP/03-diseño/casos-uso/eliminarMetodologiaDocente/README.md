<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`eliminarMetodologiaDocente()`](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): la vista decide la rama con las asignaciones (mismo endpoint que la ficha) y el `DELETE` las vuelve a comprobar.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarMetodologiaDocente` (React), prop `admin`.
- **API**: `routers/metodologia_docente.py::eliminar_metodologia_docente(metodologia_docente_id)`.
- **Repositorio**: `MetodologiaDocenteRepository.asignaciones()`, `eliminar()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`_autorizar_programa`/`_puede_en_programa`, importados de `routers/competencia.py`, y `_autorizar_metodologia` en `routers/metodologia_docente.py`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que `Competencia`.
- **Sin endpoint `esta-asignado` propio**: la vista reutiliza `/asignaciones`, que además da los nombres para el mensaje de bloqueo.
- **Bloquean los dos niveles**: `metodologias_materia` y `asignaturas_programa_metodologias_docentes`. Hasta #772 solo se miraba la `Materia`.


## Referencias

- [`eliminarMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md).

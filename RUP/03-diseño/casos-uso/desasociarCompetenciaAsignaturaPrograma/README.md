<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarCompetenciaAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-14
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`desasociarCompetenciaAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md): un solo `DELETE`, sin consulta previa.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarCompetenciaAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarCompetenciaAsignaturaPrograma` (React), prop `admin`.
- **API**: `routers/competencia.py::desasociar_competencia_asignatura_programa()`.
- **Repositorio**: `CompetenciaRepository.desasociar_de_asignatura_programa()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`routers/competencia.py::_puede_en_programa`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que los endpoints de programa de `ResultadoAprendizaje`.
- **Sin endpoint `quedaria-sin-...`**: a diferencia del RA no hay advertencia de último elemento (#761, punto 3).

## Referencias

- [`desasociarCompetenciaAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md).

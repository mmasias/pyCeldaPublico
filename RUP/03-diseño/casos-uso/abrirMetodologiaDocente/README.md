<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`abrirMetodologiaDocente()`](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): la ficha y la distribución son dos peticiones independientes, como en `abrirCompetencia()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `MetodologiaDocente` (React), prop `admin` para la vista de Admin; la Distribución la pinta el componente `Distribucion`, compartido con `Competencia` y `ResultadoAprendizaje`.
- **API**: `obtener_metodologia_docente()`, `obtener_asignaciones_metodologia_docente()`.
- **Repositorio**: `MetodologiaDocenteRepository.obtener()`, `asignaciones()` (id y nombre, ordenados por nombre, para enlazar cada uno).

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`_autorizar_programa`/`_puede_en_programa`, importados de `routers/competencia.py`, y `_autorizar_metodologia` en `routers/metodologia_docente.py`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que `Competencia`.


## Referencias

- [`abrirMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiaDocente/README.md).

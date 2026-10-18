<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`crearMetodologiaDocente()`](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): la forma la valida Pydantic (422) y el `<<choice>>` de código repetido lo resuelve el router antes del `INSERT` (409).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearMetodologiaDocente` (React), prop `admin`; campos en `FormularioCatalogoPrograma`, compartido con `ActividadFormativa`.
- **API**: `routers/metodologia_docente.py::crear_metodologia_docente(programa_id, datos)`, `_rechazar_codigo_repetido()`.
- **Schema**: `MetodologiaDocenteCreate` (`_DatosMetodologiaDocente`: no vacíos tras `strip`, `LIMITE_CODIGO` 20, `LIMITE_DESCRIPCION` 500).
- **Repositorio**: `MetodologiaDocenteRepository.codigo_en_uso()`, `crear()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`_autorizar_programa`/`_puede_en_programa`, importados de `routers/competencia.py`, y `_autorizar_metodologia` en `routers/metodologia_docente.py`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que `Competencia`.
- **Unicidad doble**: el router responde 409 con mensaje legible (`_rechazar_codigo_repetido()`, comparación con `UPPER` en las dos partes); la restricción `UNIQUE (programa_id, codigo)` de la tabla queda como red de seguridad ante dos peticiones simultáneas, y `_commit_o_409()` traduce el `IntegrityError` a 409, no a 500. La restricción de la tabla distingue mayúsculas; la comprobación previa, no.
- **Hasta #772** el catálogo era de `Universidad` (`/api/v1/universidades/{universidad_id}/metodologias-docentes`, solo `require_admin`) y el `Programa` habilitaba un subconjunto en `programas_metodologias_docentes`; ese endpoint y esa tabla desaparecen (la migración `migrar_catalogos_por_programa.py` copia a cada programa las que tenía habilitadas o en uso).

## Referencias

- [`crearMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md).

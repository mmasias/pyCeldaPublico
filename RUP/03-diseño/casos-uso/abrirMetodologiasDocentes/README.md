<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMetodologiasDocentes() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`abrirMetodologiasDocentes()`](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): dos consultas, el listado y un conteo agregado (una sola consulta `GROUP BY`, sin N+1), como en `abrirCompetencias()`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `MetodologiasDocentes` (React), la misma página en las dos vistas (`/programas/:id/metodologias-docentes` y `/admin/programas/:id/metodologias-docentes`, prop `admin`).
- **API**: `routers/metodologia_docente.py::listar_metodologias_docentes_del_programa(programa_id)`.
- **Repositorio**: `MetodologiaDocenteRepository.listar_del_programa()`, `conteo_asignaturas_del_programa()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`_autorizar_programa`/`_puede_en_programa`, importados de `routers/competencia.py`, y `_autorizar_metodologia` en `routers/metodologia_docente.py`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Resuelve la identidad con `get_current_admin_email_opcional` y `get_current_director_programa_id_opcional`: con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, 404 uniforme, sin distinguir "no existe" de "no es tuyo" -- mismo criterio que `Competencia`.
- **Orden natural de códigos** en Python (`ordenadas()` con `clave_codigo`), no en SQL: MD1, MD2, MD10.
- **Conteo informativo**: `numero_asignaturas` no bloquea nada; solo lo rellena la lista del programa (en la ficha queda a `null`).
- **Hasta #772** el catálogo era de `Universidad` (`/api/v1/universidades/{universidad_id}/metodologias-docentes`, solo `require_admin`) y el `Programa` habilitaba un subconjunto en `programas_metodologias_docentes`; ese endpoint y esa tabla desaparecen (la migración `migrar_catalogos_por_programa.py` copia a cada programa las que tenía habilitadas o en uso).

## Referencias

- [`abrirMetodologiasDocentes()` en Análisis](/RUP/02-analisis/casos-uso/abrirMetodologiasDocentes/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentes/README.md).

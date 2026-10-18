<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadesFormativas() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`abrirActividadesFormativas()`](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): un `GET` de solo lectura sobre el catálogo del `Programa`, con la autorización compartida Admin/Director de `Competencia`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirActividadesFormativas/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ActividadesFormativas` (React), prop `admin` -- `GET /api/v1/programas/{programa_id}/actividades-formativas`; presenta `nombre` y `codigo` por fila.
- **API**: `routers/actividad_formativa.py::listar_actividades_formativas(programa_id)`.
- **Repositorio**: `ActividadFormativaRepository.listar_del_programa(programa_id)` -- `SELECT` filtrado por `programa_id`, orden de alta (`id` ascendente).

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`routers/competencia.py::_autorizar_programa` sobre `_puede_en_programa`, reutilizados): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`. Con sesión Admin, cualquier `Programa`; sin ella, solo los que dirige el director. Fuera de eso, `404` uniforme, sin distinguir "no existe" de "no es tuyo".
- **Orden de alta, no por código**: es el orden canónico que comparten las filas de `ActividadFormativaMateria` y `ActividadFormativaAsignaturaPrograma` (`_catalogo_ids()`), y el de la memoria cuando el catálogo se importa del RUCT. `Competencia` ordena por código; aquí no, para que listado y rejillas coincidan.
- **Programa sin catálogo**: lista vacía (`200`).
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Histórico**: hasta #772 el listado colgaba de `/api/v1/universidades/{universidad_id}/actividades-formativas` con `Depends(require_admin)` (issue [#655](https://github.com/mmasias/pyCelda/issues/655)).

## Referencias

- [`abrirActividadesFormativas()` en Análisis](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md).
- [`abrirCompetencias()` en Diseño](/RUP/03-diseño/casos-uso/abrirCompetencias/README.md) -- patrón de autorización.

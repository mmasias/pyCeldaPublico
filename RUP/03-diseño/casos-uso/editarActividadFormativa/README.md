<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`editarActividadFormativa()`](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): `GET` previo + `PUT`, con el `<<choice>>` de código repetido resuelto en el router (409) y la forma en Pydantic (422).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadFormativa` (React), prop `admin`; formulario común `FormularioCatalogoPrograma`.
- **API**: `routers/actividad_formativa.py::editar_actividad_formativa(actividad_formativa_id, datos)`, `_autorizar_actividad()`, `_rechazar_codigo_repetido(..., salvo_id)`.
- **Schema**: `ActividadFormativaUpdate` (`_DatosActividadFormativa`, mismas reglas que el alta).
- **Modelo**: `ActividadFormativa.actualizar(codigo, nombre)`.
- **Repositorio**: `ActividadFormativaRepository.codigo_en_uso()`, `editar(actividad, codigo, nombre)`.

## Decisiones de diseño

- **`programa_id` no forma parte de `ActividadFormativaUpdate`**: una actividad no migra de `Programa`.
- **Unicidad doble**, como en el alta: `409` legible del router y `UNIQUE (programa_id, codigo)` como red, con el `IntegrityError` traducido a `409` en `_commit_o_409()`.
- **Editar no toca el reparto**: `ActividadFormativaMateria`/`ActividadFormativaAsignaturaPrograma` referencian la actividad por `actividad_formativa_id`.
- **Autorización compartida Admin/Director** por el `Programa` de la actividad; `404` uniforme fuera de alcance.
- **Histórico**: hasta #772 el `codigo` viajaba en el `PUT` pero la Vista lo presentaba de solo lectura, y la autorización era `Depends(require_admin)`.

## Referencias

- [`editarActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md).
- [`editarCompetencia()` en Diseño](/RUP/03-diseño/casos-uso/editarCompetencia/README.md) -- patrón de origen.

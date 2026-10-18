<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`abrirActividadFormativa()`](/RUP/02-analisis/casos-uso/abrirActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): un `GET` por identificador propio, autorizado por el `Programa` de la actividad.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ActividadFormativa` (React), prop `admin` -- `GET /api/v1/actividades-formativas/{actividad_formativa_id}`; con `programa_id` de la respuesta monta la miga y la pestaña del programa.
- **API**: `routers/actividad_formativa.py::obtener_actividad_formativa(actividad_formativa_id)`, `_autorizar_actividad()`.
- **Repositorio**: `ActividadFormativaRepository.obtener(actividad_formativa_id)` -- `SELECT` por clave primaria.

## Decisiones de diseño

- **Detalle por identificador propio, sin `programa_id` en la ruta**, como `Competencia`: `_autorizar_actividad()` carga la actividad y comprueba `_puede_en_programa()` sobre su `programa_id`. Inexistente o de un programa fuera del alcance: `404` uniforme.
- **Sin endpoint de asignaciones**: a diferencia de `GET /competencias/{id}/asignaciones`, aquí no hay nada que listar (autopoblado: todas las `Materia`/`AsignaturaPrograma` del programa tienen fila).
- **Reutiliza el endpoint** que `editarActividadFormativa()` y `eliminarActividadFormativa()` usan como carga previa.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/abrirActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md).
- [`abrirCompetencia()` en Diseño](/RUP/03-diseño/casos-uso/abrirCompetencia/README.md) -- patrón de autorización por la entidad.

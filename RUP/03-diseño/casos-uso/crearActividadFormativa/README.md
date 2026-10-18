<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño de [`crearActividadFormativa()`](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md) (issue [#772](https://github.com/mmasias/pyCelda/issues/772)): la forma la valida Pydantic (422), el `<<choice>>` de código repetido lo resuelve el router antes del `INSERT` (409) y el repositorio mantiene la invariante de autopoblado en la misma transacción.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearActividadFormativa` (React), prop `admin`; formulario común `FormularioCatalogoPrograma`.
- **API**: `routers/actividad_formativa.py::crear_actividad_formativa(programa_id, datos)`, `_rechazar_codigo_repetido()`.
- **Schema**: `ActividadFormativaCreate` (`_DatosActividadFormativa`).
- **Repositorio**: `ActividadFormativaRepository.codigo_en_uso()`, `crear()`; helpers `poblar_actividades_formativas_materia()` / `poblar_actividades_formativas_asignatura_programa()`.

## Decisiones de diseño

- **Autorización compartida Admin/Director** (`_autorizar_programa` sobre `_puede_en_programa`, de `routers/competencia.py`): un mismo endpoint para los dos actores, sin espejo `/api/v1/admin/...`; fuera de alcance, `404` uniforme.
- **Unicidad doble**: el router responde `409` con mensaje legible (comparación sin distinguir mayúsculas); la restricción `UNIQUE (programa_id, codigo)` de la tabla queda como red de seguridad ante dos altas simultáneas (el `IntegrityError` se traduce también a `409`, no a `500`).
- **Invariante de autopoblado en el propio `crear()`**: toda `Materia`/`AsignaturaPrograma` tiene una fila por cada `ActividadFormativa` del catálogo de su `Programa`; al crear una nueva, el repositorio puebla a 0 las de ese programa (y solo las de ese programa) antes del `COMMIT`. Es lógica de aplicación, no un trigger de BD. Las filas de `Materia` nacen con `porcentaje_presencialidad = 0`.
- **`201 Created` con el objeto creado**: la Vista navega a la ficha (`abrirActividadFormativa()`), desde la que se edita.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Histórico**: hasta #772, `POST /api/v1/universidades/{universidad_id}/actividades-formativas` con `Depends(require_admin)`, guarda `404` de `Universidad` y autopoblado sobre las `Materia`/`AsignaturaPrograma` de la `Universidad` (issue [#655](https://github.com/mmasias/pyCelda/issues/655)).

## Referencias

- [`crearActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md).
- [`crearCompetencia()` en Diseño](/RUP/03-diseño/casos-uso/crearCompetencia/README.md) -- patrón de origen.

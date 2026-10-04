<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: ClaudeF-pyCelda-SDF1

## Propósito

Bajada a diseño del caso de análisis [`editarActividadFormativa()`](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md): CRUD real e inmediato, `PUT /api/v1/actividades-formativas/{actividad_formativa_id}`, sin ninguna llamada a otra entidad. Sin `alt` de negocio -- la única validación es de forma (`codigo` y `nombre` obligatorios), resuelta por Pydantic. `ActividadFormativa` gana aquí su método `actualizar(codigo, nombre)`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadFormativaView` (React) -- carga el formulario con `GET /api/v1/actividades-formativas/{actividad_formativa_id}` (mismo endpoint que `abrirActividadFormativa()`), envía cambios con `PUT`; el `codigo` se presenta de solo lectura (regla de Requisitos: no editable una vez creada la actividad).
- **API**: `routers/actividad_formativa.py::editar_actividad_formativa(actividad_formativa_id, datos)` -- función suelta; `404` si no existe.
- **Modelo**: `ActividadFormativa.actualizar(codigo, nombre)`.
- **Repositorio**: `ActividadFormativaRepository.obtener(actividad_formativa_id)` (reutilizado) / `.editar(actividad, codigo, nombre)`.

## Decisiones de diseño

- **Sin `alt` de negocio**: la única validación es de forma, resuelta por `ActividadFormativaUpdate` (Pydantic: `codigo` y `nombre` obligatorios).
- **El `codigo` viaja en `ActividadFormativaUpdate` aunque el formulario no lo edita**: regla de Requisitos resuelta en la Vista (campo de solo lectura, reenviado sin cambios); el esquema de entrada no distingue campos por caso de uso.
- **`ActividadFormativaRepository.editar(actividad, codigo, nombre)`** invoca `ActividadFormativa.actualizar(codigo, nombre)` y persiste -- mismo reparto Modelo-muta/Repository-persiste que `Asignatura.actualizar()` + `AsignaturaRepository.actualizar()`.
- **`universidad_id` no cambia**: no forma parte de `ActividadFormativaUpdate`; una actividad no migra de `Universidad`.
- **Reutiliza el `GET` de `abrirActividadFormativa()`**: mismo endpoint de carga.
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT`.
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de `Admin`, sin pertenencia que verificar (sin `get_current_director_programa_id`). El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor. Especialmente relevante por ser endpoint de escritura.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`editarActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/README.md).
- [`editarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md) -- clúster plantilla.
- [`abrirActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/abrirActividadFormativa/README.md) -- mismo endpoint `GET`, reutilizado.
- [`crearActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/crearActividadFormativa/README.md) -- el alta alcanza el detalle desde el que se edita.
- [`editarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md) -- mismo patrón de `GET` previo + `PUT` sin `alt` de negocio.

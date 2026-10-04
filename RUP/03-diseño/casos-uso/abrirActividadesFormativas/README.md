<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadesFormativas() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: ClaudeF-pyCelda-SDF1

## Propósito

Bajada a diseño del caso de análisis [`abrirActividadesFormativas()`](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md): un solo paso, de solo lectura. Presenta el listado de `ActividadFormativa` de una `Universidad` -- cada fila presenta `codigo` y `nombre`. El controlador de Análisis converge en `routers/actividad_formativa.py`, módulo de funciones sueltas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirActividadesFormativas/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirActividadesFormativasView` (React) -- pide `GET /api/v1/universidades/{universidad_id}/actividades-formativas`; presenta `codigo` y `nombre` por fila. Preselecciona la primera `Universidad` y permite cambiar de una a otra.
- **API**: `routers/actividad_formativa.py::listar_actividades_formativas(universidad_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada -- `ActividadFormativa` solo porta los datos de cada fila.
- **Repositorio**: `ActividadFormativaRepository.listar_de_la_universidad(universidad_id)` -- `SELECT` filtrado por `universidad_id`, orden de alta (`id` ascendente).

## Decisiones de diseño

- **Listado por `Universidad`, no global**: `ActividadFormativa` es catálogo de `Universidad` (`universidad_id` NOT NULL, issue [#655](https://github.com/mmasias/pyCelda/issues/655)): cada `Universidad` tiene el suyo, por eso el listado y el alta cuelgan de `/universidades/{universidad_id}` y el detalle/edición/borrado por identificador propio. Es la diferencia estructural con el listado de `MetodologiaDocente` documentado en su ficha original, que era plano.
- **Sin `404` para una `Universidad` sin catálogo**: lista vacía (`200`); la `Universidad` inexistente tampoco se valida en el `GET` (solo en el `POST`).
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de `Admin`, sin pertenencia que verificar (sin `get_current_director_programa_id`). El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirActividadesFormativas()` en Análisis](/RUP/02-analisis/casos-uso/abrirActividadesFormativas/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadesFormativas/README.md).
- [`abrirActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/abrirActividadFormativa/README.md) / [`crearActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/crearActividadFormativa/README.md) / [`eliminarActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/eliminarActividadFormativa/README.md) -- destinos de navegación del listado.
- [`abrirMetodologiasDocentes()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiasDocentes/README.md) -- clúster plantilla.

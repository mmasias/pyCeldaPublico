<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: ClaudeF-pyCelda-SDF1

## Propósito

Bajada a diseño del caso de análisis [`abrirActividadFormativa()`](/RUP/02-analisis/casos-uso/abrirActividadFormativa/README.md): un solo paso, de solo lectura. Presenta `codigo` y `nombre` de la `ActividadFormativa`; no hay navegación a ningún catálogo hijo, solo `[Editar]`/`[Volver al listado]`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirActividadFormativaView` (React) -- pide `GET /api/v1/actividades-formativas/{actividad_formativa_id}`; presenta los dos datos y la navegación.
- **API**: `routers/actividad_formativa.py::obtener_actividad_formativa(actividad_formativa_id)` -- función suelta.
- **Modelo**: ninguno con lógica propia invocada.
- **Repositorio**: `ActividadFormativaRepository.obtener(actividad_formativa_id)` -- `SELECT` por clave primaria.

## Decisiones de diseño

- **`404` si el repositorio devuelve `None`** (`ActividadFormativa no encontrada`): guardia en la función del Router -- no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Detalle por identificador propio, sin `universidad_id` en la ruta**: la respuesta (`ActividadFormativaResponse`) sí incluye `universidad_id`.
- **Reutiliza el endpoint que `editarActividadFormativa()` y `eliminarActividadFormativa()` usan como carga previa**: mismo `GET`, sin duplicar lógica de lectura.
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de `Admin`, sin pertenencia que verificar (sin `get_current_director_programa_id`). El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`abrirActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/abrirActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirActividadFormativa/README.md).
- [`abrirMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md) -- clúster plantilla.
- [`editarActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md) -- mismo endpoint `GET`, reutilizado como carga del formulario.
- [`abrirActividadesFormativas()` en Diseño](/RUP/03-diseño/casos-uso/abrirActividadesFormativas/README.md) -- listado desde el que se alcanza este caso de uso.

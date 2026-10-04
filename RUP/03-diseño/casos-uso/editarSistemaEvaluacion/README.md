<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSistemaEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarSistemaEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/editarSistemaEvaluacion/README.md): sin `<<choice>>` -- edición de los cuatro campos (`tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`) sobre el formulario precargado, todos editables. Traducción directa del `guardarCambios()` de Análisis: cargar por Repository, mutar en el Modelo (`actualizar()`), persistir por Repository.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarSistemaEvaluacion` (React, ruta `/admin/sistemas-evaluacion/:id/editar`) -- formulario precargado vía `GET /api/v1/sistemas-evaluacion/{id}`; pide `PUT /api/v1/sistemas-evaluacion/{sistema_evaluacion_id}`.
- **API**: `routers/sistema_evaluacion.py::editar_sistema_evaluacion(sistema_evaluacion_id, datos)` -- función suelta, sin capa Service.
- **Modelo**: `SistemaEvaluacion.actualizar(tipo, descripcion, ponderacion_minima, ponderacion_maxima)` -- aplica los cuatro campos sobre sí mismo, método nuevo; el existente `validar_maximo(ponderacion)` queda intacto (lo usa `PonderacionEvaluacion`).
- **Repositorio**: `SistemaEvaluacionRepository.obtener(sistema_evaluacion_id)` / `.editar(sistema_evaluacion, tipo, descripcion, ponderacion_minima, ponderacion_maxima)`.

## Decisiones de diseño

- **Sin rama de fallo**: Análisis cierra el caso sin `<<choice>>` ni validación de negocio -- los obligatorios son de forma (Pydantic, `SistemaEvaluacionUpdate`) y no hay invariante de estado que proteger; el `PUT` es un camino único.
- **La coherencia del rango es validación de forma de la Vista**, igual que en el alta: `0 <= mínima <= máxima <= 100` se comprueba en el formulario antes de enviar; el backend no la exige.
- **Sin pantalla previa de carga propia**: el formulario llega precargado con el `GET` de [`abrirSistemaEvaluacion()`](../abrirSistemaEvaluacion/README.md), no se duplica endpoint.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`editarSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/editarSistemaEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/README.md).
- [`editarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md) -- mismo patrón de edición sin `<<choice>>`; allí `codigo` fijo desde el alta, aquí los cuatro campos editables.
- [`crearSistemaEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/crearSistemaEvaluacion/README.md) -- mismo formulario en el alta.

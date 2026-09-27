<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarPonderacionEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarPonderacionEvaluacion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/editarPonderacionEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarPonderacionEvaluacion()`](/RUP/02-analisis/casos-uso/editarPonderacionEvaluacion/README.md): CRUD real e inmediato contra `PonderacionEvaluacionRepository`, sin capa Service. Misma validación de máximo puntual que [`crearPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md) -- sin exclusión del valor anterior, porque ya no hay suma de hermanas de la que excluirlo: el máximo se comprueba sobre el valor nuevo, en solitario. Tres pasos -- cargar la ponderación actual, cargar el selector de `SistemaEvaluacion`, y guardar -- con `<<choice>>` de éxito/rechazo, ambos terminando en la misma pantalla (self-loop).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarPonderacionEvaluacionView` (React) -- `GET /api/v1/ponderaciones-evaluacion/{ponderacion_id}` y `GET /api/v1/materias/{materia_id}/sistemas-evaluacion` para poblar el formulario; `PUT /api/v1/ponderaciones-evaluacion/{ponderacion_id}` al confirmar.
- **API**: `routers/ponderacion_evaluacion.py::obtener_ponderacion_evaluacion(ponderacion_id)`, `listar_sistemas_evaluacion(materia_id)` (reutilizada de [`crearPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md)), `editar_ponderacion_evaluacion(ponderacion_id, datos)`.
- **Modelo**: `PonderacionEvaluacion.actualizar(sistema_evaluacion_id, descripcion, ponderacion)` -- se actualiza a sí misma, Fat Model; `SistemaEvaluacion.validar_maximo(ponderacion)`, mismo mecanismo que en creación.
- **Repositorio**: `PonderacionEvaluacionRepository.obtener(ponderacion_id)` / `.actualizar(ponderacion)`; `MateriaRepository.obtener(materia_id)`; `SistemaEvaluacionRepository.obtener(sistema_evaluacion_id)`.

## Decisiones de diseño

- **Sin capa Service**: mismo criterio que el resto de la rebanada -- decisión cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **`PonderacionEvaluacion.actualizar()` en vez de `Repository.actualizar()` construyendo el UPDATE directamente**: la mutación del propio objeto es responsabilidad del Modelo (Fat Model); el Repository solo persiste el objeto ya mutado -- mismo patrón que `Guia.sincronizar*()` en [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md).
- **`MateriaRepository`/`SistemaEvaluacionRepository` reutilizados de [`crearPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md)**, misma justificación: repositorios mínimos de solo lectura para materializar clases que Análisis referencia sin repositorio propio.
- **Ambas ramas terminan en la misma pantalla** (self-loop, verde con datos actualizados / rojo sin cambios) -- no hay navegación de salida distinta entre éxito y fallo, a diferencia de la creación (que sí navega a `<<include>>` en éxito).
- **`200 OK`** en éxito (no `201 Created`, no se crea nada nuevo) y **`422 Unprocessable Entity`** en rechazo, mismo código que en creación.

## Referencias

- [`editarPonderacionEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/editarPonderacionEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/README.md).
- [`crearPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md) -- misma validación de máximo puntual y mismo par de repositorios de solo lectura.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño.

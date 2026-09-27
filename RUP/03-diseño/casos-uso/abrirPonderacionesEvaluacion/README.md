<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirPonderacionesEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirPonderacionesEvaluacion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirPonderacionesEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirPonderacionesEvaluacion()`](/RUP/02-analisis/casos-uso/abrirPonderacionesEvaluacion/README.md): dos endpoints de lectura, sin capa Service, pedidos en paralelo por la Vista (`Promise.all`). El primero (`listar_ponderaciones_evaluacion`) orquesta `GuiaRepository` y `PonderacionEvaluacionRepository` y fusiona vinculadas + pendientes, mismo patrón de agregación de lectura que [`abrirGuia()`](/RUP/03-diseño/casos-uso/abrirGuia/README.md) aplicado a una única colección. El segundo (`listar_sistemas_evaluacion_de_guia`) resuelve el catálogo completo de `SistemaEvaluacion` de la materia -- `Guia` -> `AsignaturaGrado` -> `Materia` -> `Materia.listar_sistemas_evaluacion()` -- para la segunda tabla "Sistemas de evaluación de la materia" (discussion [#38](https://github.com/mmasias/pyCelda/discussions/38)), que la Vista usa para el medidor de completitud por rango (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)). Este segundo endpoint no estaba reflejado en este artefacto antes de esta corrección ([issue #212](https://github.com/mmasias/pyCelda/issues/212)).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirPonderacionesEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirPonderacionesEvaluacionView` (React) -- pide, en paralelo (`Promise.all`), `GET /api/v1/guias/{guia_id}/ponderaciones-evaluacion` y `GET /api/v1/guias/{guia_id}/sistemas-evaluacion`.
- **API**: `routers/ponderacion_evaluacion.py::listar_ponderaciones_evaluacion(guia_id)` -- función suelta; obtiene la `Guia`, lista vinculadas y pendientes, y fusiona. `routers/ponderacion_evaluacion.py::listar_sistemas_evaluacion_de_guia(guia_id)` -- función suelta; resuelve `Guia` -> `AsignaturaGrado` -> `Materia` y devuelve `materia.listar_sistemas_evaluacion()` (issue [#212](https://github.com/mmasias/pyCelda/issues/212)).
- **Modelo**: `Guia`/`AsignaturaGrado`/`Materia` -- sin lógica propia invocada salvo `Materia.listar_sistemas_evaluacion()`, que solo expone la relación (`return self.sistemas_evaluacion`); ninguna aplica una regla de dominio en este caso de uso.
- **Repositorio**: `GuiaRepository.obtener(guia_id)`; `PonderacionEvaluacionRepository.listar_vinculadas_de(guia)` / `listar_pendientes_de(guia_id)` -- mismos métodos ya usados por `abrirGuia()`. `AsignaturaGradoRepository.obtener(guia.asignatura_grado_id)`; `MateriaRepository.obtener(asignatura_grado.materia_id)` -- cadena de tres saltos para llegar al catálogo, sin repositorio propio de `SistemaEvaluacion` en esta ruta.

## Decisiones de diseño

- **Fusión en el Router, no en `Guia`**: mismo criterio que `abrirGuia()`, agregación de lectura sin regla de dominio.
- **El medidor de completitud lo calcula la Vista** (Bloque 1 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): total asignado contra 100% y subtotal por `SistemaEvaluacion` contra su rango, sobre la lista fusionada -- presentación, sin backend, consistente con el mismo medidor en [`abrirGuia()`](/RUP/03-diseño/casos-uso/abrirGuia/README.md). El rango de cada `SistemaEvaluacion` no viene en la respuesta de `listar_ponderaciones_evaluacion()`: la Vista lo cruza contra la segunda petición (issue [#212](https://github.com/mmasias/pyCelda/issues/212)).
- **Dos peticiones independientes, no una sola con joins**: `listar_sistemas_evaluacion_de_guia()` no se apoya en `listar_ponderaciones_evaluacion()` ni comparte caché entre sí -- son dos llamadas HTTP separadas desde la Vista (`Promise.all`), cada una con su propia cadena de repositorios. No se introduce una optimización sin evidencia de que haga falta, mismo criterio que [`abrirGuia()`](/RUP/03-diseño/casos-uso/abrirGuia/README.md).
- **Sin capa Service**: Router delgado -> Modelo/Repository directamente.
- **Endpoints nuevos, repositorios reutilizados**: `listar_ponderaciones_evaluacion(guia_id)` y `listar_sistemas_evaluacion_de_guia(guia_id)` son funciones nuevas en `routers/ponderacion_evaluacion.py`, pero ninguna introduce un método nuevo en su repositorio -- la primera reutiliza `listar_vinculadas_de`/`listar_pendientes_de` (ya usados por `abrirGuia()`); la segunda reutiliza `GuiaRepository.obtener()`, `AsignaturaGradoRepository.obtener()` y `MateriaRepository.obtener()`, y termina en `Materia.listar_sistemas_evaluacion()` -- no hay `SistemaEvaluacionRepository` en esta ruta pese a existir esa clase (se usa en otros CU, no en este).
- **Autenticación fuera de este diagrama**: `profesor_id` llega inyectado por *dependency override* de FastAPI, mismo criterio que el resto de la rebanada.

## Referencias

- [`abrirPonderacionesEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/abrirPonderacionesEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/README.md).
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- mismo mecanismo de fusión vinculado+pendiente.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño, sin capa Service.
- Discussion [#38](https://github.com/mmasias/pyCelda/discussions/38) -- origen de `listar_sistemas_evaluacion_de_guia()`.
- [Issue #212](https://github.com/mmasias/pyCelda/issues/212) -- deriva de este artefacto anterior a #206, cerrada aquí: faltaba el segundo endpoint (`listar_sistemas_evaluacion_de_guia`) y su cadena `Guia` -> `AsignaturaGrado` -> `Materia`.

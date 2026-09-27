<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarSesion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarSesion/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/editarSesion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-30
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarSesion()`](/RUP/02-analisis/casos-uso/editarSesion/README.md): CRUD real e inmediato contra `SesionRepository`, sin capa Service. Dos pasos -- cargar la sesión actual y guardar -- a diferencia de [`editarPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md), que necesita un tercero para el selector de `SistemaEvaluacion`. **Sin `<<choice>>`**: sin enlace estructural a `SistemaEvaluacion`/`PonderacionEvaluacion` (decisión 4 de la discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)), no hay regla de negocio que pueda rechazar la edición. Solo `tipo` y `descripcion` son editables; `numero` es correlativo automático y permanece sin cambios (decisión 6).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarSesion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarSesionView` (React) -- `GET /api/v1/sesiones/{sesion_id}` para poblar el formulario (`numero` visible, no editable; `tipo`/`descripcion` editables); `PUT /api/v1/sesiones/{sesion_id}` al confirmar.
- **API**: `routers/sesion.py::obtener_sesion(sesion_id)` / `editar_sesion(sesion_id, datos)` -- funciones sueltas, sin capa Service.
- **Modelo**: `Sesion.actualizar(tipo, descripcion)` -- se actualiza a sí misma, Fat Model.
- **Repositorio**: `SesionRepository.obtener(sesion_id)` / `actualizar(sesion)` -- `UPDATE` sobre `sesiones`.

## Decisiones de diseño

- **Sin capa Service**: mismo criterio que el resto de la rebanada -- decisión cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **`Sesion.actualizar()` en vez de `Repository.actualizar()` construyendo el `UPDATE` directamente**: la mutación del propio objeto es responsabilidad del Modelo (Fat Model); el Repository solo persiste el objeto ya mutado -- mismo patrón que `PonderacionEvaluacion.actualizar()` y que `Guia.sincronizar*()` en [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md).
- **Sin `<<choice>>`, a diferencia de `editarPonderacionEvaluacion()`**: allí el `alt` con self-loop en ambas ramas separaba éxito de "supera el máximo" (`SistemaEvaluacion.validar_maximo()`); aquí no hay validación de negocio que pueda fallar (decisión 4 de la discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)) -- el `PUT` es camino único y el retorno al listado es self-loop simple.
- **`numero` no editable**: `SesionUpdate` solo lleva `tipo` y `descripcion` -- el correlativo asignado por `crearSesion()` permanece (decisión 6 de la discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)).
- **`validarDatosObligatorios(tipo, descripcion)` de `PlanificacionDocenteController` (Análisis) se disuelve en Pydantic**: `SesionUpdate` (`schemas/`, fuera de este diagrama) exige los campos obligatorios antes de que la función del router se ejecute -- mismo mecanismo ya citado para `PonderacionEvaluacionCreate`/`Update` (hallazgo de la discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)). No es un hueco -- es validación de forma resuelta por el framework, fuera de la capa que este diagrama cubre.
- **`200 OK`** en éxito (no `201 Created`, no se crea nada nuevo). Sin rama de rechazo de negocio: la única respuesta de error posible es la `422` de forma que Pydantic resuelve antes del router.
- **Autenticación fuera de este diagrama**: `profesor_id` llega inyectado por *dependency override* de FastAPI, mismo criterio que el resto de la rebanada.

## Referencias

- [`editarSesion()` en Análisis](/RUP/02-analisis/casos-uso/editarSesion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/README.md).
- [`editarPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) -- mismo patrón Fat Model `actualizar()` + `UPDATE`; contraste: sin selector que cargar y sin `<<choice>>`.
- [`crearSesion()` en Diseño](/RUP/03-diseño/casos-uso/crearSesion/README.md) -- quien asigna el `numero` correlativo que aquí permanece sin cambios.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño, sin capa Service.
- Discussion [#140](https://github.com/mmasias/pyCelda/discussions/140) -- decisión 4 (sin enlace a `SistemaEvaluacion`) y decisión 6 (`numero` automático).

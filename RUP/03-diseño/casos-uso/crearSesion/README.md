<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearSesion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearSesion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-30
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearSesion()`](/RUP/02-analisis/casos-uso/crearSesion/README.md): CRUD real e inmediato contra `SesionRepository`, sin capa Service. Un solo paso -- crear -- y **sin `<<choice>>`**: `Sesion` no se enlaza estructuralmente con `SistemaEvaluacion`/`PonderacionEvaluacion` en esta iteración (decisión 4 de la discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)), así que no hay regla de negocio que pueda rechazar el alta. `numero` no se solicita: lo calcula el servidor con el siguiente correlativo y el formulario lo muestra como automático, no editable (decisión 6). Sin carga previa de selector, a diferencia de [`crearPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md): el enum cerrado de `tipo` viaja con el propio formulario, no hay que pedir `SistemaEvaluacion`/`Materia` a nadie.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearSesion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearSesionView` (React) -- presenta el formulario (selector `tipo` con los seis valores del enum cerrado, `descripcion`; `numero` automático, no editable, no se pide) y envía `POST /api/v1/guias/{guia_id}/sesiones` al confirmar.
- **API**: `routers/sesion.py::crear_sesion(guia_id, datos)` -- función suelta, sin capa Service.
- **Modelo**: `Sesion` -- creada por el repositorio; porta `id`, `guia_id`, `numero`, `tipo`, `descripcion` y `vinculada` (nace `false`), sin método propio invocado: el correlativo es una consulta agregada, no una regla del objeto.
- **Repositorio**: `SesionRepository.siguiente_numero(guia_id)` / `crear(guia_id, numero, tipo, descripcion)` -- persistencia real e inmediata en `sesiones`.

## Decisiones de diseño

- **Sin capa Service**: el Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Sin `<<choice>>`, a diferencia de `crearPonderacionEvaluacion()`**: allí el `alt` separaba éxito de "supera el máximo" (`SistemaEvaluacion.validar_maximo()`); aquí no hay nada que validar como regla de negocio -- sin enlace a `SistemaEvaluacion` (decisión 4 de la discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)), el alta es camino único.
- **`validarDatosObligatorios(tipo, descripcion)` de `PlanificacionDocenteController` (Análisis) se disuelve en Pydantic**: `SesionCreate` (`schemas/`, fuera de este diagrama) exige los campos obligatorios antes de que la función del router se ejecute -- mismo mecanismo ya citado para `PonderacionEvaluacionCreate`/`Update` (hallazgo de la discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)). No es un hueco -- es validación de forma resuelta por el framework, fuera de la capa que este diagrama cubre.
- **`numero` calculado por el servidor, no pedido**: `SesionCreate` no lleva `numero`; lo calcula `SesionRepository.siguiente_numero(guia_id)` con `SELECT COALESCE(MAX(numero), 0) + 1` (o `1` si la planificación docente está vacía) -- decisión 6 de la discussion [#140](https://github.com/mmasias/pyCelda/discussions/140). El correlativo vive como consulta del repositorio, no como método de `Sesion`: no hay objeto sobre el que preguntar antes de que exista.
- **Sin `<<include>>` a edición**: a diferencia de `crearPonderacionEvaluacion()`/`crearReferenciaBibliografica()`, que navegan tras crear a la vista de edición (`<<include>>`), aquí se vuelve directamente al listado de `abrirPlanificacionDocente()` con la sesión nueva ya visible -- topología ya cerrada en Análisis (discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)): catálogo inline sobre `PLANIFICACION_DOCENTE_ABIERTO`, sin estado de detalle de `Sesion` separado.
- **La fila nace con `guia_id` pero sin vincular** (`vinculada = false`), mismo mecanismo que `crearPonderacionEvaluacion()`/`crearReferenciaBibliografica()` -- decisión 1 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Autenticación fuera de este diagrama**: `profesor_id` llega inyectado por *dependency override* de FastAPI, mismo criterio que el resto de la rebanada.

## Referencias

- [`crearSesion()` en Análisis](/RUP/02-analisis/casos-uso/crearSesion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/README.md).
- [`crearPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md) -- contraste en los tres puntos que aquí se simplifican: sin selector que cargar, sin `<<choice>>` de máximo, sin `<<include>>` a edición.
- [`abrirPlanificacionDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirPlanificacionDocente/README.md) -- el listado al que se vuelve con la sesión nueva ya visible.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño, sin capa Service.
- Discussion [#140](https://github.com/mmasias/pyCelda/discussions/140) -- decisión 4 (sin enlace a `SistemaEvaluacion`) y decisión 6 (correlativo automático).

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirPlanificacionDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirPlanificacionDocente/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirPlanificacionDocente/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-30
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`abrirPlanificacionDocente()`](/RUP/02-analisis/casos-uso/abrirPlanificacionDocente/README.md): un único endpoint de lectura, sin `<<choice>>` y sin capa Service -- el Router orquesta `GuiaRepository` y `SesionRepository`, fusiona vinculadas + pendientes y ordena por `numero`, mismo patrón de agregación de lectura que [`abrirPonderacionesEvaluacion()`](/RUP/03-diseño/casos-uso/abrirPonderacionesEvaluacion/README.md) aplicado a la colección de `Sesion` de la `PlanificacionDocente`. La respuesta es un envelope `AbrirPlanificacionDocenteResponse { sesiones, sesiones_minimas }` (Bloque 3 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): `sesiones_minimas` sale de `Guia.sesiones_minimas` y es la `M` del medidor "N / M sesiones" que calcula la Vista.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/abrirPlanificacionDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AbrirPlanificacionDocenteView` (React) -- pide `GET /api/v1/guias/{guia_id}/sesiones`.
- **API**: `routers/sesion.py::listar_sesiones(guia_id)` -- función suelta; obtiene la `Guia`, lista vinculadas y pendientes, fusiona ordenando por `numero` y devuelve `AbrirPlanificacionDocenteResponse { sesiones, sesiones_minimas }` (`response_model` de FastAPI).
- **Modelo**: `Sesion` -- sin lógica propia invocada, solo listada (porta `id`, `guia_id`, `numero`, `tipo`, `descripcion`, `vinculada`); `Guia` -- sin lógica propia invocada, solo referenciada para la consulta de vinculadas y para `Guia.sesiones_minimas` (umbral del medidor), mismo papel que en `abrirPonderacionesEvaluacion()`.
- **Repositorio**: `GuiaRepository.obtener(guia_id)`; `SesionRepository.listar_vinculadas_de(guia)` / `listar_pendientes_de(guia_id)` -- mismos métodos que ya fijó Análisis, ahora sobre la tabla `sesiones`.

## Decisiones de diseño

- **Fusión y orden en el Router, no en `Guia` ni en `Sesion`**: mismo criterio que `abrirPonderacionesEvaluacion()`/`abrirGuia()` -- agregación de lectura sin regla de dominio, sin capa Service.
- **Respuesta con envelope, no lista pelada** (Bloque 3 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)): `AbrirPlanificacionDocenteResponse { sesiones, sesiones_minimas }` en vez de `list[SesionResponse]`. `sesiones_minimas` es atributo de la vista de planificación docente (la `M` del medidor "N / M"), no un recurso aparte, y este CU es su punto de lectura -- se decidió el envelope antes que una segunda llamada a `abrirGuia()`. Único consumidor: `PlanificacionDocente.tsx`. El medidor "N / M sesiones" (rojo si `N < M`) lo calcula la Vista sobre las sesiones visibles.
- **`PlanificacionDocenteController` (Análisis) converge en `routers/sesion.py`**, módulo de funciones sueltas, no una clase -- `PlanificacionDocenteController.listarSesiones(guiaId)` baja a `listar_sesiones(guia_id)`. El módulo, la tabla (`sesiones`) y los schemas se llaman por la entidad, `Sesion`, sin sufijo: el renombrado `Cronograma` -> `Planificación docente` de la discussion [#198](https://github.com/mmasias/pyCelda/discussions/198) retiró el sufijo `_cronograma` que antes desambiguaba frente a la sesión de usuario. Esa sesión vive en `routers/auth.py` (`/auth/me`, `iniciarSesion()`/`cerrarSesion()`), sin fichero `sesion.py` propio, así que no hay colisión de nombre de módulo; la desambiguación que queda es solo de concepto, y la resuelve el nombre del controlador (`PlanificacionDocenteController`, no `SesionController`).
- **`PlanificacionDocente` sigue sin aparecer**: ni tabla ni clase -- toda referencia se resuelve por `guia_id` sobre `sesiones`, mismo hallazgo ya cerrado en Análisis (composición 1:1 con `Guia` sin estado ni comportamiento propio en esta iteración).
- **Autenticación fuera de este diagrama**: `profesor_id` llega inyectado por *dependency override* de FastAPI, mismo criterio que el resto de la rebanada.

## Referencias

- [`abrirPlanificacionDocente()` en Análisis](/RUP/02-analisis/casos-uso/abrirPlanificacionDocente/README.md) -- diagrama de colaboración origen, incluido el hallazgo del `numero` presentado como posición en la lista fusionada, no valor persistido.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/README.md).
- [`abrirPonderacionesEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/abrirPonderacionesEvaluacion/README.md) -- mismo mecanismo de fusión vinculado+pendiente, mismo patrón `GuiaRepository.obtener()` previo.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño, sin capa Service.
- Discussion [#140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente.

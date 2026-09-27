<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > generarPlanificacionDocenteGenerica() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/README.md)|[Análisis](/RUP/02-analisis/casos-uso/generarPlanificacionDocenteGenerica/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-06
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño de [`generarPlanificacionDocenteGenerica()`](/RUP/02-analisis/casos-uso/generarPlanificacionDocenteGenerica/README.md) (familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184)). Comparte `SesionRepository` y la traza de `HistorialCambio` con [`importarPlanificacionDocenteDeGuiaHermana()`](../importarPlanificacionDocenteDeGuiaHermana/README.md), pero **no** el router `importar_guia_hermana.py`: aquí no hay guía origen ni lectura cross-grado, así que el endpoint vive en `routers/sesion.py`, junto al resto del CRUD de la planificación docente.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/generarPlanificacionDocenteGenerica/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Diseño

- **Endpoint**: `POST /api/v1/guias/{guia_id}/sesiones/generar-genericas`, **body vacío**, respuesta `AbrirPlanificacionDocenteResponse` (el mismo shape que `GET /guias/{guia_id}/sesiones`) -- el frontend recarga el listado con la respuesta directa, sin segundo round-trip. Autorización: `get_current_profesor_id` + `AsignaturaGradoRepository.imparte(...)`, **404 uniforme** si el `Profesor` no imparte la `AsignaturaGrado` de la guía (sin la relajación cross-grado de `importarPlanificacionDocenteDeGuiaHermana()`).
- **`Guia.planificacion_docente_vacia() -> bool`** (Fat Model, método nuevo en `models/guia.py`): `not self.sesiones` -- ni vinculadas ni pendientes. El endpoint responde `409` (`detail="La planificación docente ya tiene sesiones"`) si no está vacía. `409` y no `404` porque la guía **sí** existe y el `Profesor` **sí** tiene acceso -- es un conflicto de estado, no un problema de identidad/autorización; la 404-uniforme protege identidad, no impide informar de un conflicto sobre un recurso ya visible. La rama roja de la especificación (salvaguarda server-side): el botón solo se ofrece en el empty-state de `PlanificacionDocente.tsx`.
- **`SesionRepository.generar_genericas(guia, cantidad) -> list[Sesion]`** (método nuevo, simétrico a `reemplazar_desde()`): crea `cantidad` filas `Sesion(guia_id=guia.id, numero=i, tipo="CLASE_TEORICA", descripcion="", vinculada=True)` para `i` en `1..cantidad`, `add_all` + `flush()` **sin commit** -- el commit lo hace el handler, en la misma transacción que el `HistorialCambio` y el `fecha_ultima_modificacion`. Sin borrado previo: la precondición `planificacion_docente_vacia()` garantiza que no hay nada que borrar.
- **`cantidad = guia.sesiones_minimas`** -- resuelto en el handler, no parámetro del cliente. `CLASE_TEORICA` como literal (valor de `SesionTipo`, ver `schemas/sesion.py`); si el enum cambiara de default, este es uno de los sitios a tocar.
- **`HistorialCambio`**: `HistorialCambio.registrar(guia_id=guia.id, autor_id=profesor_id, campo="planificacion_docente", valor_anterior="0 sesiones", valor_nuevo=f"{cantidad} sesiones", comentario=f"planificación docente generada ({cantidad} sesiones genéricas)")` -- una fila, mismo patrón que `_registrar_importacion` de `importar_guia_hermana.py`.
- **`Guia.confirmar_guardado()`**: reutilizado tal cual -- toca `fecha_ultima_modificacion`; sobre una guía vacía nunca dispara `Aprobada -> Borrador` (no puede estar `Aprobada`).
- **Frontend**: `PlanificacionDocente.tsx` -- en el empty-state (`sesionesVisibles.length === 0` y sin error), botón `[Crear N sesiones genéricas]` (N = `sesionesMinimas`, del estado ya cargado). Confirmación por **doble pulsación** (patrón del `[Eliminar]` ya presente en la página; sin modal). Al confirmar, `generarSesionesGenericas(guiaId)` (nuevo en `api.ts`) -> `POST .../generar-genericas` -> `setEstado` con la respuesta (`sesiones`, `sesiones_minimas`). El `409` se trata como "recargar" (alguien creó sesiones entre medias): re-`listarSesiones` y quitar el botón.
- **Punto de extensión futuro (no construido)**: un patrón semanal (`{patron: "2T-1P", semanas: 15}`) entraría como campo opcional del body; hoy el body es `{}`. El endpoint y el nombre (`generar-genericas`, no `generar-plana`) dejan sitio sin comprometerse.
- **Divergencia lateral registrada** (no la resuelve este CU): el Modelo declara `Guia *-- PlanificacionDocente *-- Sesion`; el código aplana `Sesion.guia_id` directo. `generar_genericas` y `planificacion_docente_vacia()` operan sobre `Guia.sesiones` como el resto del código.

## Contrato de endpoint

### POST `/api/v1/guias/{guia_id}/sesiones/generar-genericas`

**Request:** body vacío.

**Response (200):** `AbrirPlanificacionDocenteResponse` -- `{ sesiones: [...N sesiones CLASE_TEORICA, vinculadas, numero 1..N...], sesiones_minimas: N }`.

**Response (404 Not Found):** `{ "detail": "Guia no encontrada" }` -- guía inexistente o el `Profesor` no la imparte.

**Response (409 Conflict):** `{ "detail": "La planificación docente ya tiene sesiones" }` -- la guía ya tiene alguna `Sesion`.

## Referencias

- [`generarPlanificacionDocenteGenerica()` en Análisis](/RUP/02-analisis/casos-uso/generarPlanificacionDocenteGenerica/README.md).
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/generarPlanificacionDocenteGenerica/README.md).
- [`importarPlanificacionDocenteDeGuiaHermana()` en Diseño](../importarPlanificacionDocenteDeGuiaHermana/README.md) -- comparte `SesionRepository` y la forma de la traza; router distinto.
- [`abrirPlanificacionDocente()` en Diseño](../abrirPlanificacionDocente/README.md) -- `AbrirPlanificacionDocenteResponse`, `PlanificacionDocente.tsx`.
- [`enviarGuiaARevision()` en Detalle](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md) -- regla `c3` (`sesiones_minimas`).

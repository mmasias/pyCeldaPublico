<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > enviarGuiaARevision() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md)|[Análisis](/RUP/02-analisis/casos-uso/enviarGuiaARevision/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/enviarGuiaARevision/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`enviarGuiaARevision()`](/RUP/02-analisis/casos-uso/enviarGuiaARevision/README.md): tres comprobaciones en cascada sobre la `Guia` ya vinculada -- nunca materializa ni vincula nada él mismo, eso ya lo hizo [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) antes. Primero, una **precondición** (`c1`): si queda algo pendiente-sin-vincular (`PonderacionEvaluacion`, `ReferenciaBibliografica` o `Sesion`), rechaza pidiendo guardar primero, sin llegar a validar nada más. Si no hay pendientes, valida contra lo ya vinculado las reglas agregadas del dominio: rango por **todos** los `SistemaEvaluacion` de la materia y suma total exactamente 100% (`Guia.bloqueo_ponderaciones()`, `c2`); y planificación docente con al menos `Guia.sesiones_minimas` `Sesion` vinculadas (`Guia.planificacion_docente_completa()`, `c3`). Ambas son Fat Model. Si las tres pasan, transiciona la `Guia` a `EnRevision` y persiste solo la `Guia`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/enviarGuiaARevision/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EnviarGuiaARevisionView` (React) -- un único paso, sin formulario; pide `POST /api/v1/guias/{guia_id}/enviar-a-revision`.
- **API**: `routers/guia.py::enviar_guia_a_revision(guia_id)` -- función suelta, sin capa Service; encadena la precondición `c1` y las validaciones de negocio `c2`/`c3` antes de decidir.
- **Modelo**: `Guia.bloqueo_ponderaciones()` (`c2`) -- devuelve el motivo concreto (`str`) del primer incumplimiento de rango por `SistemaEvaluacion` o de suma total, o `None` si puede enviarse; `puede_enviarse_a_revision()` sigue existiendo como `bloqueo_ponderaciones() is None`, pero el router ya no la llama. `Guia.planificacion_docente_completa()` (`c3`) -- `sesiones_vinculadas_count() >= self.sesiones_minimas`; `Guia.enviar_a_revision()` -- aplica `Borrador -> EnRevision` / `Rechazada -> EnRevision` sobre sí misma.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`; `PonderacionEvaluacionRepository.existe_pendiente_de(guia_id)`, `ReferenciaBibliograficaRepository.existe_pendiente_de(guia_id)`, `SesionRepository.existe_pendiente_de(guia_id)` -- estos tres, la precondición `c1`.

## Decisiones de diseño

- **Sin capa Service**: el Router encadena las comprobaciones directamente contra repositorios y `Guia` -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **La precondición corta antes de tocar la regla de negocio**: si cualquiera de los dos `existe_pendiente_de()` responde `true`, la secuencia rechaza sin llamar siquiera a `Guia.puede_enviarse_a_revision()` -- evita computar una validación agregada sobre datos que el propio `Profesor` sabe que están incompletos.
- **`409 Conflict` para la precondición `c1`, `422 Unprocessable Entity` para las reglas de negocio `c2` y `c3`**: motivos de rechazo distintos con semántica HTTP distinta -- `c1` es un conflicto de estado de la sesión de edición (hay trabajo sin guardar), `c2`/`c3` son contenido que no cumple una regla de dominio. La especificación de Requisitos los dibuja como tres `<<choice>>` encadenados; todas las ramas rojas convergen al mismo estado de salida y la Vista, en los tres casos, se queda en la misma pantalla.
- **`c3` va después de `c2`, no en paralelo**: mismo criterio que `c1 -> c2`. Se computa la validación más barata y más "estructural" primero (ponderaciones), y solo si pasa se mira la planificación docente. El mensaje del `422` de `c3` ("Planificación docente incompleta: N de M sesiones") es distinto del de `c2`.
- **`c2` devuelve el motivo concreto en el propio valor de retorno del modelo, `c3` no** (issue #208, corrige una decisión de esta misma ficha que ya no aplicaba a `c2`): `Guia.bloqueo_ponderaciones()` es Fat Model completo -- construye él mismo el string exacto ("Falta asignar N% en \<tipo\> (mínimo M%, asignado X%)" / "Sobra N% en \<tipo\> (máximo M%, asignado X%)") y el router lo usa tal cual como `detail` del `422`, sin tocarlo. `Guia.planificacion_docente_completa()` sigue devolviendo solo `boolean`; el router arma el mensaje de `c3` ("N de M sesiones") a partir de los contadores porque ese motivo no tiene variantes -- siempre es la misma plantilla con dos números.
- **`200 OK` en éxito**, con la `Guia` ya en `EnRevision` -- la Vista navega a `ASIGNATURAS_PROGRAMA_ABIERTO` con ese resultado, sin una segunda petición.

## Referencias

- [`enviarGuiaARevision()` en Análisis](/RUP/02-analisis/casos-uso/enviarGuiaARevision/README.md) -- diagrama de colaboración origen, con las tres comprobaciones `c1`/`c2`/`c3`.
- [Discussion #206](https://github.com/mmasias/pyCelda/discussions/206) -- origen de la regla `c3` (planificación docente mínima) y del `sesiones_minimas` configurable.
- [Issue #208](https://github.com/mmasias/pyCelda/issues/208) -- `bloqueo_ponderaciones()` recorre todos los `SistemaEvaluacion` de la materia y devuelve el motivo concreto, en vez de un `boolean` genérico.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md).
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `Borrador -> EnRevision` / `Rechazada -> EnRevision`.
- [`guardarBorradorGuia()`](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md) -- quien vincula lo pendiente; su ausencia es lo que dispara la precondición de rechazo.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño.

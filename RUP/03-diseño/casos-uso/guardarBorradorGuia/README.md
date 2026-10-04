<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > guardarBorradorGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/guardarBorradorGuia/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`guardarBorradorGuia()`](/RUP/02-analisis/casos-uso/guardarBorradorGuia/README.md): un único endpoint, sin `<<choice>>` (siempre tiene éxito). Recibe la lista completa de identificadores deseada para cada colección (`PonderacionEvaluacion`, `ReferenciaBibliografica` y `Sesion` -- esta última desde el Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)) y **sincroniza por diff** contra lo que la `Guia` ya tiene vinculado -- `Guia.sincronizar_ponderaciones()`/`sincronizar_referencias()`/`sincronizar_sesiones()`, Fat Model: la decisión de qué vincular/desvincular es una regla de dominio, vive en `Guia`, no en el Router. No crea filas nuevas de esas colecciones -- `crearPonderacionEvaluacion()`/`crearReferenciaBibliografica()`/`crearSesion()` ya las crearon real e inmediato contra su propio repositorio; pero **`desvincular` sí borra la fila** (issue [#93](https://github.com/mmasias/pyCelda/issues/93): quedar fuera de la lista completa = "el profesor la excluyó"). Recibe además `datos.contenido` (temario redactado por el `Profesor`, discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)): `Guia.actualizar_contenido(texto)` lo aplica y devuelve el valor anterior si cambió, y en ese caso el Router añade una fila de `HistorialCambio` (`campo="contenido"`, autor quien escribe (`profesor_id` o, como corrección excepcional, `director_programa_id`), `valor_anterior`/`valor_nuevo` con un resumen del texto). Si la `Guia` estaba `Aprobada`, dispara `Aprobada -> Borrador`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/guardarBorradorGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `GuardarBorradorGuiaView` (React) -- recoge la lista completa de `id`s de `PonderacionEvaluacion`/`ReferenciaBibliografica`/`Sesion` que las sub-vistas de cada colección han ido curando y el texto del `contenido` (temario) del `textarea`, y pide `PUT /api/v1/guias/{guia_id}/borrador`. `contenido` ausente en el body = "no lo envío en esta petición", no "ponlo a vacío".
- **API**: `routers/guia.py::guardar_borrador_guia(guia_id, datos)` -- función suelta, sin capa Service; orquesta el diff, ejecuta las vinculaciones/desvinculaciones resultantes, aplica el `contenido` y registra `HistorialCambio` si cambió.
- **Modelo**: `Guia.sincronizar_ponderaciones(ids_final)` / `sincronizar_referencias(ids_final)` / `sincronizar_sesiones(ids_final)` -- compara la lista deseada contra lo ya vinculado, devuelve `(a_vincular, a_desvincular)`, sin tocar la base de datos; `Guia.actualizar_contenido(texto)` -- aplica el temario y devuelve el valor anterior si cambió (`None` si llega igual); `Guia.confirmar_guardado()` -- actualiza `fechaUltimaModificacion` y aplica `Aprobada -> Borrador` si corresponde, según su propia máquina de estados.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)`; `PonderacionEvaluacionRepository`, `ReferenciaBibliograficaRepository` y `SesionRepository`, cada uno con `.vincular(id, guia)` (pone `vinculada=True`) / `.desvincular(id)` (**`db.delete` de la fila**, issue [#93](https://github.com/mmasias/pyCelda/issues/93)) -- uno por cada elemento del diff; no crean filas ni editan su contenido. La fila de `HistorialCambio` se añade con `db.add()` directo (mismo patrón que `aprobar_guia()`/`rechazar_guia()`, sin repositorio propio).

## Decisiones de diseño

- **Sin capa Service**: el Router calcula el diff pidiéndoselo a `Guia` y ejecuta las llamadas de vinculación directamente contra cada repositorio -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **El diff es puro cálculo en memoria** (`Guia.sincronizar*()` no toca la base de datos): solo las llamadas de `vincular()`/`desvincular()` por cada `id` del resultado generan escritura -- una por fila afectada, no una única sentencia batch, para mantener el mismo Repository de un solo registro que ya usan el resto de casos de la rebanada.
- **`Guia.confirmar_guardado()` decide la transición `Aprobada -> Borrador` sobre sí misma** -- el Router no compara estados a mano; es la propia `Guia` quien aplica su máquina de estados, igual que `aprobar()`/`enviar_a_revision()` en los demás casos de ciclo de vida.
- **Nunca rechaza**: no hay rama de error en la secuencia -- coherente con que Análisis ya cerró este caso de uso sin `<<choice>>`.
- **`HistorialCambio` de `contenido` solo si el texto cambió** (discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)): "el historial arranca con la primera acción humana real" -- un guardado que no toca el temario no genera fila. `Guia._ultimo_cambio_historial()` ignora las filas `campo="contenido"` (solo mira `campo="estado"`) al calcular quién actualizó la guía por última vez, para no atribuir la edición del profesor al director. `valor_anterior`/`valor_nuevo` guardan un resumen del texto (columnas cortas), no el temario completo -- el detalle vive en `Guia.contenido`.
- **`200 OK` con la `Guia` completa** (no `204 No Content`): la pantalla de confirmación necesita `estado` y `fechaUltimaModificacion` actualizados para mostrarlos sin una segunda petición.
- **Corrección excepcional del `DirectorPrograma`** (issue [#612](https://github.com/mmasias/pyCelda/issues/612), Parte 2 de [#601](https://github.com/mmasias/pyCelda/issues/601)): `autorizar_escritura_guia()` (`routers/guia.py`) resuelve quién escribe -- `Profesor` que imparte (False, sin transición) o `DirectorPrograma` que dirige el `Programa` de la `Guia` (True); ninguno de los dos, `404` uniforme. Si escribe el Director, `aplicar_transicion_por_correccion_del_director()` mueve la `Guia` (`Aprobada -> Borrador` con `revocar_aprobacion()`, `EnRevision -> Rechazada` con `rechazar()`; `Borrador`/`Rechazada` se mantienen) y añade el `HistorialCambio` `campo="estado"` con comentario "corrección directa del Director"; sin `commit` propio: se confirma en la misma transacción que la escritura. Se aplica tras la comprobación del tope de longitud del `contenido` y antes de sincronizar las colecciones; `autor_id` de los historiales de colecciones y de `contenido` es el del Director. Por eso `Guia.confirmar_guardado()` ya encuentra la `Guia` en `Borrador` y solo actualiza la fecha.

## Referencias

- [`guardarBorradorGuia()` en Análisis](/RUP/02-analisis/casos-uso/guardarBorradorGuia/README.md) -- diagrama de colaboración origen, con la mecánica de sincronización completa.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/README.md).
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `Aprobada -> Borrador`.
- [`crearPonderacionEvaluacion()`](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md) / [`crearReferenciaBibliografica()`](/RUP/03-diseño/casos-uso/crearReferenciaBibliografica/README.md) / [`crearSesion()`](/RUP/03-diseño/casos-uso/crearSesion/README.md) -- quiénes crean las filas que aquí se vinculan o desvinculan (borran).
- [`enviarGuiaARevision()`](/RUP/03-diseño/casos-uso/enviarGuiaARevision/README.md) -- exige que no queden pendientes sin guardar antes de validar y transicionar a `EnRevision`.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- decisión 1 (vinculación) y criterio de arranque de Diseño.

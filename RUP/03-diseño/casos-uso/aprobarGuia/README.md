<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > aprobarGuia() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/README.md)|[Análisis](/RUP/02-analisis/casos-uso/aprobarGuia/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`aprobarGuia()`](/RUP/02-analisis/casos-uso/aprobarGuia/README.md): un solo paso, sin `<<choice>>`, sin formulario y sin pantalla de confirmación -- el `DirectorPrograma` solicita aprobar y el sistema transiciona `Guia.estado` de `EnRevision` a `Aprobada` aplicando su propia máquina de estados (`Guia.aprobar()`, Fat Model), registra el `HistorialCambio` con el comentario fijo `"aprobada sin incidencia"` y persiste el agregado completo. Único caso de uso de la rebanada cuyo actor es `DirectorPrograma`, no `Profesor`.

**Retoque posterior (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224), cierre de Frente B)**: `Guia.aprobar()` gana una segunda línea en su propio cuerpo, `self.regenerar_pdf()` -- mismo método que ya existía desde [`editarSemestreGuia()`](/RUP/03-diseño/casos-uso/editarSemestreGuia/README.md), llamado ahora también desde aquí. **El Router no cambia**: `routers/guia.py::aprobar_guia()` sigue llamando solo a `guia.aprobar()`; el efecto colateral queda encapsulado en el Modelo, no repartido entre Router y Modelo como en `editarSemestreGuia()` (que sí hace dos llamadas explícitas desde el Router: `actualizar_semestre()` y `regenerar_pdf()`). Decisión de Manuel: aprobar es ahora el disparador real de "PDF descargable" -- no se construye el botón manual de Frente B (`generarGuiaPDF()`, nunca implementado).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/aprobarGuia/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `AprobarGuiaView` (React) -- recoge la solicitud de aprobación sin pedir ningún dato; pide `POST /api/v1/guias/{guia_id}/aprobar`.
- **API**: `routers/guia.py::aprobar_guia(guia_id)` -- función suelta, sin capa Service; coordina la transición, el registro de historial y la persistencia.
- **Modelo**: `Guia.aprobar()` -- aplica `EnRevision -> Aprobada` sobre sí misma, según su máquina de estados, y llama a `self.regenerar_pdf()` (retoque posterior, discussion #224); `HistorialCambio.registrar(campo, valorAnterior, valorNuevo, comentario)` -- crea el registro en memoria, compuesto por `Guia`.
- **Repositorio**: `GuiaRepository.obtener(guia_id)` / `.actualizar(guia)` -- el `UPDATE` persiste `Guia` y, por relación ORM, el `HistorialCambio` recién compuesto.

## Decisiones de diseño

- **Sin capa Service**: el Router coordina las tres piezas (transición, registro, persistencia) directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **`GuiaRepository.obtener(guia_id)` no aparece en el diagrama de colaboración de Análisis** (que arranca directo en `GuiaController --> Guia: aprobar()`) -- Análisis asume la `Guia` ya en memoria de la sesión de revisión; Diseño sí necesita nombrar cómo llega al proceso Python de un request HTTP sin estado, así que se añade el mismo patrón de carga que el resto de la rebanada.
- **El comentario `"aprobada sin incidencia"` lo fija el propio Router**, no el `DirectorPrograma`: no hay campo de formulario que lo transporte -- coherente con que Análisis ya cerró este caso de uso sin formulario ni pantalla de confirmación (discussion [#44](https://github.com/mmasias/pyCelda/discussions/44)).
- **`HistorialCambio` se compone en memoria antes del `UPDATE`, no con un `INSERT` propio**: al ser `Guia *- HistorialCambio` una composición, un único `GuiaRepository.actualizar(guia)` basta para persistir ambos -- no se introduce un `HistorialCambioRepository` nuevo.
- **Sin rama de fallo**: la acción solo es alcanzable sobre una `Guia` en `EnRevision` -- si la máquina de estados no admite la transición, es un error de programación (llamada desde un estado inválido), no un `<<choice>>` de negocio que la secuencia deba modelar.
- **Autenticación fuera de este diagrama**: el `director_programa_id` llega inyectado por *dependency override* de FastAPI (stub, decisión 3 de la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)) -- es quien queda registrado como autor del `HistorialCambio`, pero no se modela como paso propio de la secuencia.
- **`regenerar_pdf()` como self-call dentro de `aprobar()`, no como paso separado del Router** (retoque posterior, discussion #224): a diferencia de `editarSemestreGuia()` -- donde el Router llama a `actualizar_semestre()` y `regenerar_pdf()` como dos mensajes propios, porque son dos operaciones independientes sobre la misma `Guia` -- aquí `regenerar_pdf()` es consecuencia directa e incondicional del propio cambio de estado que `aprobar()` ya aplica, así que vive dentro del método (Fat Model, sin fuga de esta regla a la capa de coordinación).
- **`_sincronizar_profesorado()` como segundo self-call dentro de `aprobar()`** (issue [#254](https://github.com/mmasias/pyCelda/issues/254)): mismo criterio que `regenerar_pdf()`. `aprobar()` (y `escalar_a_aprobada()`) hacen `if self.asignatura_programa is not None: self.profesorado = list(self.asignatura_programa.profesorado)` -- re-derivar `Guia -- Profesor` de la plantilla es consecuencia directa e incondicional de pasar a `Aprobada`, no un paso que el Router coordine. `GuiaRepository.obtener()` gana `selectinload(AsignaturaPrograma.profesorado)` para que esa lista esté cargada. Nada más cambia en el endpoint.

## Referencias

- [`aprobarGuia()` en Análisis](/RUP/02-analisis/casos-uso/aprobarGuia/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/README.md).
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_PROGRAMA_ABIERTO : aprobarGuia()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `EnRevision -> Aprobada`.
- Discussion [#58](https://github.com/mmasias/pyCelda/discussions/58) -- criterio de arranque de Diseño y decisión 3 (autenticación stub).
- [`editarSemestreGuia()` en Diseño](/RUP/03-diseño/casos-uso/editarSemestreGuia/README.md) -- disparador original de `regenerar_pdf()`, ya no en exclusiva.
- [`descargarGuiaPDF()` en Diseño](/RUP/03-diseño/casos-uso/descargarGuiaPDF/README.md) -- consumidor de `fecha_generacion_pdf`.
- Discussion [#224](https://github.com/mmasias/pyCelda/discussions/224) -- cierre de Frente B: aprobar/escalar como disparador real de "PDF descargable".

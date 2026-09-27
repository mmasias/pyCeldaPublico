<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > guardarBorradorGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/guardarBorradorGuia/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/guardarBorradorGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`guardarBorradorGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/README.md): un solo paso, sin `<<choice>>` (siempre tiene éxito, nunca rechaza). Recibe, para `PonderacionEvaluacion`, `ReferenciaBibliografica` y `Sesion`, la lista completa de identificadores tal como debe quedar la `Guia` -- no eventos de alta/baja por ítem -- y **sincroniza por diff** contra lo que la `Guia` ya tiene vinculado: lo nuevo en la lista se vincula, lo que ya no aparece se desvincula (y desvincular **borra la fila** -- issue [#93](https://github.com/mmasias/pyCelda/issues/93): la ausencia de la lista significa "el profesor la eliminó"). La sincronización de `Sesion` se añadió en el Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), con el mismo patrón que las otras dos. Recibe además el `contenido` (temario) redactado por el `Profesor` y lo aplica sobre la `Guia` (discussion [#191](https://github.com/mmasias/pyCelda/discussions/191)); si el texto cambió respecto al anterior, genera una fila de `HistorialCambio` (`campo="contenido"`). Si la `Guia` estaba `Aprobada`, dispara `Aprobada -> Borrador`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/guardarBorradorGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Mecánica de sincronización

`PonderacionEvaluacion`, `ReferenciaBibliografica` y `Sesion` no se crean aquí -- ya existen como filas reales desde que `crearPonderacionEvaluacion()`/`crearReferenciaBibliografica()`/`crearSesion()` las crearon (real e inmediato contra su propio repositorio, con `vinculada=False`). Lo que este caso de uso resuelve es qué queda oficialmente en la `Guia`: `Guia.sincronizarPonderaciones(idsFinal)` / `sincronizarReferencias(idsFinal)` / `sincronizarSesiones(idsFinal)` compara la lista recibida contra lo que ya tiene vinculado y devuelve dos listas -- a vincular, a desvincular. Vincular pone `vinculada=True`; **desvincular borra la fila** (issue [#93](https://github.com/mmasias/pyCelda/issues/93): quedar fuera de la lista completa que manda el cliente es "el profesor la excluyó", no "aún sin decidir"). La decisión de qué vincular/desvincular es una regla de dominio, por eso vive en `Guia` (Fat Model), no en el `GuiaController`.

## Clases de vista

### `GuardarBorradorGuiaView`

**Responsabilidades:**
- recoge la solicitud de guardar borrador, con la lista completa de ids de `PonderacionEvaluacion`/`ReferenciaBibliografica`/`Sesion` que la sub-vista de cada colección ha ido curando, y el texto del `contenido` (temario) tal como está en el `textarea`.
- presenta la confirmación: "BORRADOR GUARDADO", estado actual, fecha de última modificación, y la nota de que si la `Guia` estaba `Aprobada` vuelve a `Borrador`.
- permite continuar editando (vuelve a `GUIA_ABIERTO`, no sale de la sesión).

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor` solicita guardar borrador.
- **Control:** `GuiaController`.
- **Salida:** `:GUIA_ABIERTO` -- self-loop.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- recupera la `Guia` de `GuiaRepository`.
- pide a `Guia` que calcule el diff de sincronización para cada colección (`sincronizarPonderaciones(...)`, `sincronizarReferencias(...)`, `sincronizarSesiones(...)`).
- ejecuta el diff: vincula (`Repository.vincular(id, guia)`) o desvincula (`Repository.desvincular(id)`, que **borra** la fila) cada ítem, en su repositorio real -- ningún `crear()` ni `actualizar()` de contenido de las filas aquí.
- pide a `Guia` que aplique el `contenido` recibido (`actualizarContenido(texto)`): si cambió, la propia `Guia` devuelve el valor anterior y el `GuiaController` registra la fila de `HistorialCambio` (`campo="contenido"`, autor el profesor); si no cambió, no hay fila.
- pide a `Guia` que confirme el guardado (`confirmarGuardado()`): actualiza `fechaUltimaModificacion` y, si el estado era `Aprobada`, aplica `Aprobada -> Borrador` -- la propia `Guia` decide esta transición según su máquina de estados.
- persiste la `Guia` resultante (`GuiaRepository.actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `GuardarBorradorGuiaView`.
- **Salida:** `GuiaRepository`, `Guia`, `PonderacionEvaluacionRepository`, `ReferenciaBibliograficaRepository`, `SesionRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- calcula el diff de sincronización de cada colección (`sincronizarPonderaciones()`/`sincronizarReferencias()`/`sincronizarSesiones()`): compara la lista deseada contra lo que ya tiene vinculado, devuelve a-vincular/a-desvincular.
- aplica su `contenido` (temario) sobre sí misma (`actualizarContenido(texto)`) y devuelve el valor anterior si el texto cambió, para que el `GuiaController` decida si registra `HistorialCambio` -- "el historial arranca con la primera acción humana real", un guardado que no toca el texto no genera fila.
- aplica `Aprobada -> Borrador` sobre sí misma cuando corresponde (`confirmarGuardado()`), según su propia máquina de estados.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** produce los diffs que `GuiaController` ejecuta; persistida ella misma por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- recupera la `Guia`, con su colección vinculada, por identificador (`obtener(guiaId)`).
- persiste la `Guia` tras la sincronización -- `fechaUltimaModificacion` actualizada, posible cambio de `estado` (`actualizar(guia)`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- vincula (`vincular(id, guia)` -> `vinculada=True`) o desvincula (`desvincular(id)` -> **`db.delete` de la fila**) cada `PonderacionEvaluacion` según el diff -- no crea filas nuevas ni edita su contenido, pero desvincular sí borra (issue [#93](https://github.com/mmasias/pyCelda/issues/93)).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona la vinculación de `PonderacionEvaluacion`.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- vincula o desvincula (borrando la fila) cada `ReferenciaBibliografica` según el diff, mismo criterio que `PonderacionEvaluacionRepository`.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona la vinculación de `ReferenciaBibliografica`.

### `SesionRepository`

**Responsabilidades:**
- vincula o desvincula (borrando la fila) cada `Sesion` según el diff, mismo criterio que las otras dos colecciones. `existe_pendiente_de(guiaId)` -- consultado por [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), no por este caso de uso. Añadido en el Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona la vinculación de `Sesion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/guardarBorradorGuia/wireframes.puml) -- fuente de verdad del paso único y de la nota `Aprobada -> Borrador`.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> GUIA_ABIERTO : guardarBorradorGuia()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `Aprobada -> Borrador`, disparada por este caso de uso.
- [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) / [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) / [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) / [`crearSesion()`](../crearSesion/README.md) -- quiénes crean las filas que aquí se vinculan o desvinculan (borran).
- [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- exige que no queden pendientes sin guardar antes de validar y transicionar a `EnRevision`.
- [`abrirGuia()`](../abrirGuia/README.md) -- pantalla compartida donde vive el botón que dispara este caso de uso.

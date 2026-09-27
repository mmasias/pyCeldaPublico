<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > aprobarGuia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/aprobarGuia/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/aprobarGuia/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`aprobarGuia()`](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/README.md): un solo paso, sin `<<choice>>`, sin formulario y sin pantalla de confirmación -- el `DirectorGrado` solicita aprobar y el sistema transiciona `Guia.estado` de `EnRevision` a `Aprobada` aplicando su propia máquina de estados, registra el `HistorialCambio` con el comentario fijo `"aprobada sin incidencia"` y presenta el resultado. Es una decisión de revisión inmediata, con persistencia real (`GuiaRepository.actualizar(...)`).

**Retoque posterior (discussion [#224](https://github.com/mmasias/pyCelda/discussions/224), cierre de Frente B)**: `aprobar()` deja de tocar solo `estado` -- como parte del mismo cambio, regenera `fechaGeneracionPDF` (`regenerarPDF()`, ya existente desde [`editarSemestreGuia()`](../editarSemestreGuia/README.md)). Encapsulado en el propio método de `Guia` (Fat Model): no aparece como una colaboración nueva en el diagrama, mismo criterio que otros métodos de `Guia` que componen varias comprobaciones internas sin exponer cada paso como una flecha (`bloqueoPonderaciones()`). Decisión de Manuel: el disparador real de "PDF descargable" pasa a ser aprobar, no un botón manual -- el PDF siempre se re-renderiza en vivo desde la fila `Guia` (no hay artefacto que "generar"), así que `fechaGeneracionPDF` es de facto un booleano histórico ("¿ha pasado por aprobación alguna vez?").

**Retoque posterior (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: dentro del mismo `aprobar()`, y con el mismo criterio Fat Model (sin flecha nueva en el diagrama), la `Guia` re-deriva su colección `Guia -- Profesor` de `AsignaturaGrado -- Profesor` -- `if self.asignaturaGrado is not None: self.profesorado = list(self.asignaturaGrado.profesorado)`. La aprobación es el punto de sincronización de esa copia; entre aprobaciones puede quedar por detrás de la plantilla si el `Admin` la cambió, y una `Guia` que volvió a `EnRevision` por ese cambio recupera aquí la lista al día. `escalarAAprobada()` hace lo mismo.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/aprobarGuia/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AprobarGuiaView`

**Responsabilidades:**
- recoge la solicitud de aprobación de la `Guia` abierta (un único paso: no hay formulario que rellenar ni confirmación que aceptar).
- presenta la pantalla de resultado: "GUÍA APROBADA" con estado anterior (`EnRevision`), estado actual (`Aprobada`) y comentario registrado ("Aprobada sin incidencia").
- permite volver al listado de guías del grado.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `DirectorGrado` solicita aprobar la `Guia` abierta.
- **Control:** `GuiaController`.
- **Salida:** `:GUIAS_DEL_GRADO_ABIERTO`.

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- coordina la decisión de revisión en tres piezas: pide a la `Guia` que aplique su transición de estado, registra el `HistorialCambio` y persiste el agregado.
- no pide ningún dato al actor: el comentario `"aprobada sin incidencia"` lo fija el propio caso de uso (aprobar es un "sí" sin matiz que explicar; si lo hubiera, el caso de uso sería otro de la familia de decisiones).
- no modela rama de fallo: la especificación no tiene `<<choice>>` -- la acción solo es alcanzable sobre una `Guia` `EnRevision`, y su máquina de estados no define alternativa para esa transición.

**Colaboraciones:**
- **Entrada:** `AprobarGuiaView`.
- **Salida:** `Guia`, `HistorialCambio`, `GuiaRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- aplica su propia transición de estado `EnRevision -> Aprobada` (`aprobar()`), según su máquina de estados -- el controlador no muta `estado` directamente: la `Guia` guarda su ciclo de vida.
- como parte del mismo `aprobar()`, regenera `fechaGeneracionPDF` (`regenerarPDF()`) -- retoque posterior, discussion #224.
- como parte del mismo `aprobar()`, re-deriva `Guia -- Profesor` de `AsignaturaGrado -- Profesor` (issue #254) -- Fat Model, sin colaboración nueva.
- es el agregado dueño de su historial (`Guia *- HistorialCambio`).

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** compone `HistorialCambio`; persistida por `GuiaRepository`.

### `HistorialCambio`

**Responsabilidades:**
- registra el cambio con `campo = "estado"`, `valorAnterior = "EnRevision"`, `valorNuevo = "Aprobada"` y `comentario = "aprobada sin incidencia"`; fija su `fecha`.
- el autor del cambio es el `DirectorGrado` (`Actor -> HistorialCambio` en el modelo de dominio) -- el registro queda asociado a quien ejecuta el caso de uso.

**Colaboraciones:**
- **Entrada:** `GuiaController` (registro); `Guia` (composición).

### `GuiaRepository`

**Responsabilidades:**
- persiste de verdad el agregado (`actualizar(guia)`): la aprobación es una decisión de revisión inmediata, no un borrador en curso.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/aprobarGuia/wireframes.puml) -- fuente de verdad del paso único y de la pantalla de resultado.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GUIA_ABIERTO --> GUIAS_DEL_GRADO_ABIERTO : aprobarGuia()`.
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- transición `EnRevision -> Aprobada` que la `Guia` aplica en `aprobar()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `HistorialCambio{campo, valorAnterior, valorNuevo, comentario}`, `Actor -> HistorialCambio`, `Guia *- HistorialCambio`.
- [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) / [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) -- contraste: CRUD real e inmediato, pero sin vincular a la `Guia` hasta `guardarBorradorGuia()`/`enviarGuiaARevision()`.
- [Discussion #44](https://github.com/mmasias/pyCelda/discussions/44) -- cierre de "sin campo de formulario" y "sin pantalla de confirmación".
- [`editarSemestreGuia()`](../editarSemestreGuia/README.md) -- disparador original (y único) de `regenerarPDF()`; deja de serlo en exclusiva con este retoque, pero mantiene su propio efecto colateral condicional sin cambio.
- [`descargarGuiaPDF()`](../descargarGuiaPDF/README.md) -- consumidor de `fechaGeneracionPDF`, que este retoque deja de depender solo de `editarSemestreGuia()` para tener valor.
- [Discussion #224](https://github.com/mmasias/pyCelda/discussions/224) -- cierre de Frente B: el disparador de "PDF descargable" pasa a ser aprobar/escalar, no un botón manual de generación.
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- `aprobar()` re-deriva `Guia -- Profesor`; la aprobación es el punto de sincronización de la copia.

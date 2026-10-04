<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPlanificacionDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirPlanificacionDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirPlanificacionDocente()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/README.md): un solo paso, sin `<<choice>>`, de solo lectura -- no vincula nada. Presenta el listado completo de `Sesion` de la `PlanificacionDocente` de la `Guia` abierta, **fusionando** lo ya vinculado con lo pendiente-sin-vincular creado en [`crearSesion()`](../crearSesion/README.md), ordenado por `numero`, junto con `Guia.sesiones_minimas` -- el umbral de la regla `c3` de [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206)) -- para el medidor "N / M sesiones" que calcula la Vista. El control lo lleva `PlanificacionDocenteController` -- llamado así, y no `SesionController`, porque ese nombre ya existe en el [diagrama de clases consolidado](../../diagrama-clases-analisis.puml) para el controlador del inicio/cierre de sesión de usuario (`iniciarSesion()`/`cerrarSesion()`), un concepto sin relación con la `Sesion` de la `PlanificacionDocente`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirPlanificacionDocente/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirPlanificacionDocenteView`

**Responsabilidades:**
- presenta el listado de `Sesion` de la `PlanificacionDocente` de la `Guia`, ordenado por `numero`.
- ofrece la navegación a crear una sesión nueva, a editar/eliminar cada fila, y a volver a la `Guia`.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor` solicita abrir la Planificación docente desde la `Guia`. Única entrada: no existe estado de detalle de `Sesion` al que volver (catálogo inline sobre `PLANIFICACION_DOCENTE_ABIERTO`, discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)).
- **Control:** `PlanificacionDocenteController`.
- **Salida:** `:PLANIFICACION_DOCENTE_ABIERTO`.

## Clases de controlador

### `PlanificacionDocenteController`

**Responsabilidades:**
- pide, para la `Guia`, las `Sesion` ya vinculadas y las pendientes-sin-vincular por separado, y las fusiona en una sola lista por presentar -- unión simple, sin regla de negocio.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirPlanificacionDocenteView`.
- **Salida:** `SesionRepository`.

## Clases de modelo

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo` (enum cerrado de seis valores), `descripcion` y si está vinculada -- mostrada ordenada por `numero` en el listado.

**Colaboraciones:**
- **Entrada:** listada por `SesionRepository`, vinculada o pendiente.

### `SesionRepository`

**Responsabilidades:**
- lista las `Sesion` vinculadas a la `Guia` (`listarVinculadasDe(guia)`).
- lista las `Sesion` con este `guiaId` todavía sin vincular (`listarPendientesDe(guiaId)`).

**Colaboraciones:**
- **Entrada:** `PlanificacionDocenteController`.
- **Salida:** gestiona `Sesion`.

## Hallazgo: por qué `PlanificacionDocente` no aparece como clase de Análisis

`PlanificacionDocente` no participa en ninguna de las cuatro colaboraciones de este lote (ni en el [diagrama de clases consolidado](../../diagrama-clases-analisis.puml)) -- toda referencia se resuelve directamente por `guiaId` sobre `SesionRepository`, y la relación estática que queda en el consolidado es `Guia -- Sesion`, sin `PlanificacionDocente` intermedia. Decisión deliberada, no un olvido: en el [modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml), `class PlanificacionDocente` no lleva ningún atributo propio (a diferencia de `Sesion{numero, tipo, descripcion}`) -- es una composición 1:1 con `Guia` sin estado ni comportamiento propio en esta iteración, existe como concepto navegable de Requisitos (`abrirPlanificacionDocente()`) pero no como fila persistida independiente. Mismo criterio que ya usan `crearPonderacionEvaluacion()`/`eliminarPonderacionEvaluacion()` al no instanciar `Guia` como participante -- aquí se aplica un nivel más adentro, a una capa de composición vacía en vez de a la raíz. Si en una iteración futura `PlanificacionDocente` gana un atributo propio (por ejemplo, una fecha de última modificación distinta de la de cada `Sesion`), esta decisión se revisa entonces -- no se anticipa aquí sin necesidad real.

## El `numero` presentado es posición en la lista fusionada, no el valor persistido

El `numero` que este listado muestra en cada fila es su **posición dentro de la lista fusionada ya presentada** (1, 2, 3...), no el valor crudo persistido de cada `Sesion`: tras un [`eliminarSesion()`](../eliminarSesion/README.md) las filas siguientes conservan su `numero` persistido y es la Vista quien renumera lo que se ve. Ese display posicional **es** la resolución -- no hay una "renumeración real" pendiente. [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)/[`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) sincronizan la vinculación de `Sesion` (Bloque 2 de la discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), `Guia.sincronizar_sesiones()` -- copia literal de `sincronizar_ponderaciones`) pero **no tocan `Sesion.numero`**: los huecos que deja un borrado son permanentes y sin efecto observable (el orden se mantiene, `siguiente_numero` es `max + 1`). Decisión de Manuel: la renumeración de la planificación docente vive en presentación, no en el dato.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirPlanificacionDocente/wireframes.puml) -- fuente de verdad del listado ordenado por `numero`.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : abrirPlanificacionDocente()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- PlanificacionDocente`, `PlanificacionDocente *-- Sesion`, `Sesion{numero, tipo, descripcion}`.
- [`crearSesion()`](../crearSesion/README.md) / [`editarSesion()`](../editarSesion/README.md) / [`eliminarSesion()`](../eliminarSesion/README.md) -- quienes crean, editan o quitan lo que este listado presenta.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- quienes sincronizan la vinculación de `Sesion` (Bloque 2 de #206); no tocan `Sesion.numero` (ver arriba).
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > enviarGuiaARevision()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/enviarGuiaARevision/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/enviarGuiaARevision/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`enviarGuiaARevision()`](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/README.md): tres comprobaciones en cascada, sobre la `Guia` ya vinculada -- nunca materializa ni vincula nada él mismo, eso ya lo hizo [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) antes. Primero, una **precondición** (`c1`): si queda algo pendiente-sin-vincular (`PonderacionEvaluacion`, `ReferenciaBibliografica` o `Sesion` creado o editado sin haber guardado el borrador), rechaza pidiendo guardar primero. Si no hay pendientes, valida las reglas de negocio agregadas contra lo ya vinculado: rango por `SistemaEvaluacion` **y** suma total exactamente 100% (`c2`); y planificación docente con al menos `Guia.sesiones_minimas` `Sesion` vinculadas (`c3`). Si las tres pasan, transiciona la `Guia` a `EnRevision` y persiste solo la `Guia` -- ningún `crear()`/`actualizar()` de hijos aquí.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/enviarGuiaARevision/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Motivos de rechazo, modelados en Requisitos

Los tres motivos de rechazo del dominio están modelados como `<<choice>>` encadenados en la [especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/especificacion.puml): `c1` (ítems sin guardar, `409`), `c2` (rango o suma de ponderaciones, `422`) y `c3` (planificación docente incompleta, `422`). El commit `3ee9d38` (2026-08-18) llevó la especificación de un `<<choice>>` a dos; el Bloque 3 de la [discussion #206](https://github.com/mmasias/pyCelda/discussions/206) añadió `c3`. Todas las ramas rojas convergen al mismo estado de salida (`GUIA_ABIERTO`), así que el diagrama de contexto no cambia.

El [issue #208](https://github.com/mmasias/pyCelda/issues/208) (2026-09-03) cerró un hueco de `c2`: antes solo se validaba el rango de los `SistemaEvaluacion` que ya tenían alguna `PonderacionEvaluacion` vinculada, así que un sistema requerido (`ponderacionMinima > 0`) en 0% se colaba sin bloquear. El rechazo `c2` sigue siendo el mismo `<<choice>>` -- no cambia el diagrama de estados -- pero la clase de modelo que lo resuelve ahora recorre todos los `SistemaEvaluacion` de la materia, no solo los ya vinculados.

## Clases de vista

### `EnviarGuiaARevisionView`

**Responsabilidades:**
- recoge la solicitud de enviar a revisión (un único paso, sin formulario).
- presenta la confirmación de éxito: "GUÍA ENVIADA A REVISIÓN", tabla de evaluación con la suma (100%).
- presenta el rechazo `c1` por ítems sin guardar: "guarda el borrador primero".
- presenta el rechazo `c2` por validación de ponderaciones: "NO SE PUEDE ENVIAR A REVISIÓN", con el motivo concreto del primer incumplimiento (issue #208).
- presenta el rechazo `c3` por planificación docente incompleta: "N de M sesiones".

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor` solicita enviar la `Guia` a revisión.
- **Control:** `GuiaController`.
- **Salida:** `:ASIGNATURAS_GRADO_ABIERTO` (éxito); `:GUIA_ABIERTO` (rechazo, por cualquiera de las tres razones, sigue en edición).

## Clases de controlador

### `GuiaController`

**Responsabilidades:**
- recupera la `Guia` de `GuiaRepository`, con su colección vinculada.
- comprueba la precondición `c1`: pregunta a `PonderacionEvaluacionRepository`, `ReferenciaBibliograficaRepository` y `SesionRepository` si queda algo pendiente-sin-vincular para esta `Guia` (`existePendienteDe(guiaId)`) -- si alguno responde que sí, rechaza sin llegar a validar nada más.
- si no hay pendientes, pregunta a la `Guia` el motivo de bloqueo de ponderaciones (`bloqueoPonderaciones()`, `c2`) -- si no es nulo, rechaza con ese motivo como `c2`.
- si `c2` pasa, pregunta a la `Guia` si su planificación docente está completa (`planificacionDocenteCompleta()`, `c3`) -- al menos `sesionesMinimas` `Sesion` vinculadas.
- las tres reglas de dominio las responde `Guia` (o los repositorios), no el controlador.
- rama verde: pide a `Guia` que aplique su transición de estado (`enviarARevision()`) y persiste solo la `Guia`.
- ninguna rama roja toca ni persiste nada.

**Colaboraciones:**
- **Entrada:** `EnviarGuiaARevisionView`.
- **Salida:** `GuiaRepository`, `Guia`, `PonderacionEvaluacionRepository`, `ReferenciaBibliograficaRepository`, `SesionRepository`.

## Clases de modelo

### `Guia`

**Responsabilidades:**
- responde el motivo concreto de bloqueo de ponderaciones (`bloqueoPonderaciones()`, `c2`), o nulo si puede enviarse: la suma total de todas las `PonderacionEvaluacion` vinculadas debe ser exactamente 100%, **y** para **todos** los `SistemaEvaluacion` de la materia (`asignaturaGrado.materia.sistemasEvaluacion`) -- no solo los que ya tienen alguna ponderación vinculada, tratando como 0% el que no tiene ninguna -- la suma asignada debe estar dentro de `[ponderacionMinima, ponderacionMaxima]`. Un sistema con `ponderacionMinima == 0` no bloquea en 0%: el rango lo admite sin caso especial. `puedeEnviarseARevision()` sigue existiendo como `bloqueoPonderaciones() == null` (issue #208, corrige un hueco donde un sistema requerido en 0% no bloqueaba).
- responde si su planificación docente está completa (`planificacionDocenteCompleta()`, `c3`): el número de `Sesion` vinculadas es al menos `sesionesMinimas` -- regla agregada de la misma familia que la suma = 100%. `sesionesMinimas` es un atributo de la propia `Guia` (snapshot de `AsignaturaGrado.sesionesMinimas` al nacer, [discussion #206](https://github.com/mmasias/pyCelda/discussions/206)).
- aplica su propia transición de estado `Borrador -> EnRevision` / `Rechazada -> EnRevision` (`enviarARevision()`), según su máquina de estados.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** persistida por `GuiaRepository` tras la transición.

### `GuiaRepository`

**Responsabilidades:**
- recupera la `Guia`, con su colección vinculada, por identificador (`obtener(guiaId)`).
- persiste la `Guia` tras el envío exitoso -- `estado` en `EnRevision` (`actualizar(guia)`); no se invoca en ninguna rama roja.

**Colaboraciones:**
- **Entrada:** `GuiaController`.
- **Salida:** gestiona `Guia`.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- responde si hay alguna `PonderacionEvaluacion` pendiente-sin-vincular para esta `Guia` (`existePendienteDe(guiaId)`) -- la precondición del punto 1.

**Colaboraciones:**
- **Entrada:** `GuiaController`.

### `ReferenciaBibliograficaRepository`

**Responsabilidades:**
- responde si hay alguna `ReferenciaBibliografica` pendiente-sin-vincular para esta `Guia` (`existePendienteDe(guiaId)`), mismo criterio.

**Colaboraciones:**
- **Entrada:** `GuiaController`.

### `SesionRepository`

**Responsabilidades:**
- responde si hay alguna `Sesion` pendiente-sin-vincular para esta `Guia` (`existePendienteDe(guiaId)`), mismo criterio que las otras dos colecciones (Bloque 2 de la [discussion #206](https://github.com/mmasias/pyCelda/discussions/206)).

**Colaboraciones:**
- **Entrada:** `GuiaController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/enviarGuiaARevision/wireframes.puml) -- fuente de verdad de las tres comprobaciones (`c1`/`c2`/`c3`).
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : enviarGuiaARevision()` (éxito), `GUIA_ABIERTO --> GUIA_ABIERTO : enviarGuiaARevision()` (rechazo).
- [Diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) -- `Borrador -> EnRevision` / `Rechazada -> EnRevision`.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) -- quien vincula lo pendiente; su ausencia es lo que dispara la precondición de rechazo.
- [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) -- valida el máximo puntual; esta validación es distinta y agregada -- rango por `SistemaEvaluacion` y suma total.
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre original de dónde y cómo se valida el rango (revisado por esta corrección arquitectónica).
- [Issue #208](https://github.com/mmasias/pyCelda/issues/208) -- deuda de la discussion #206: un `SistemaEvaluacion` requerido en 0% no bloqueaba el envío. `bloqueoPonderaciones()` cierra el hueco.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearSesion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearSesion()`](/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/README.md): CRUD real e inmediato contra `SesionRepository`, sin ninguna interacción con `Guia`. La fila se crea con `guiaId` desde el principio (pertenece a esta `Guia` desde el momento de crearse), pero no queda **vinculada** a la `PlanificacionDocente` oficial hasta que [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md)/[`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) sincronicen. Sin `<<choice>>` -- `Sesion` no se enlaza estructuralmente con `SistemaEvaluacion`/`PonderacionEvaluacion` en esta iteración (decisión 4 de discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)): no hay regla de negocio que pueda rechazar el alta. `numero` no se solicita: lo calcula el sistema como el siguiente correlativo (o `1` si la planificación docente está vacía) y el formulario lo muestra como automático, no editable (decisión 6).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearSesion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearSesionView`

**Responsabilidades:**
- presenta el formulario de creación: selector `tipo` con los seis valores del enum cerrado (`CLASE_TEORICA`, `CLASE_PRACTICA`, `CLASE_TEORICO_PRACTICA`, `CLASE_LABORATORIO`, `EVALUACION_CONTINUA`, `EVALUACION_PARCIAL`), `descripcion`, ambos obligatorios.
- muestra `numero` como automático, no editable -- el siguiente correlativo, calculado por el sistema.
- permite solicitar crear.
- al volver, la sesión nueva ya es visible en el listado de `PLANIFICACION_DOCENTE_ABIERTO`.

**Colaboraciones:**
- **Entrada:** `:PLANIFICACION_DOCENTE_ABIERTO` -- el `Profesor` solicita crear una sesión desde el listado de la Planificación docente.
- **Control:** `PlanificacionDocenteController`.
- **Salida:** `:PLANIFICACION_DOCENTE_ABIERTO` -- sesión creada con el siguiente número correlativo, pendiente de vincular.

## Clases de controlador

### `PlanificacionDocenteController`

**Responsabilidades:**
- valida los obligatorios (`tipo`, `descripcion`).
- calcula el correlativo antes de crear (`SesionRepository.siguienteNumero(guiaId)`) -- la última `Sesion` existente más uno, o `1` si la planificación docente está vacía.
- crea la `Sesion` directamente en `SesionRepository`, real e inmediato -- ninguna llamada a `Guia`.

**Colaboraciones:**
- **Entrada:** `CrearSesionView`.
- **Salida:** `SesionRepository`.

## Clases de modelo

### `Sesion`

**Responsabilidades:**
- porta `numero`, `tipo` (enum cerrado de seis valores), `descripcion` y `guiaId` -- pertenece a una `Guia` desde su creación, aunque todavía no esté vinculada a la `PlanificacionDocente` oficial.

**Colaboraciones:**
- **Entrada:** creada por `SesionRepository`.

### `SesionRepository`

**Responsabilidades:**
- calcula el siguiente número correlativo para la `Guia` (`siguienteNumero(guiaId)`).
- crea la `Sesion` (`crear(guiaId, numero, tipo, descripcion)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `PlanificacionDocenteController`.
- **Salida:** gestiona `Sesion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearSesion/wireframes.puml) -- fuente de verdad del formulario con `numero` automático.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : crearSesion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PlanificacionDocente *-- Sesion`, `Sesion{numero, tipo, descripcion}`.
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) -- quien fusiona lo vinculado con lo pendiente-sin-vincular para presentarlo.
- [`editarSesion()`](../editarSesion/README.md) / [`eliminarSesion()`](../eliminarSesion/README.md) -- mismos participantes sobre la `Sesion` creada aquí.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- quienes vinculan esta fila a la `PlanificacionDocente` oficial, o la borran (`db.delete`) si el `Profesor` la excluyó de la lista de trabajo (issue [#93](https://github.com/mmasias/pyCelda/issues/93)).
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño (decisión 4: sin enlace a `SistemaEvaluacion`; decisión 6: correlativo automático).

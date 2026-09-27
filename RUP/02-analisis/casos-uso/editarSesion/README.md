<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarSesion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarSesion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarSesion()`](/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/README.md): CRUD real e inmediato contra `SesionRepository`, sin ninguna interacción con `Guia`. Sin `<<choice>>` -- sin enlace estructural a `SistemaEvaluacion`/`PonderacionEvaluacion` (decisión 4 de discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)), no hay regla de negocio que pueda rechazar la edición. Solo `tipo` y `descripcion` son editables; `numero` es correlativo automático y permanece sin cambios (decisión 6).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarSesion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarSesionView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la sesión: selector `tipo` con los seis valores del enum cerrado, y `descripcion`, ambos obligatorios; `numero` queda visible pero no editable.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:PLANIFICACION_DOCENTE_ABIERTO` -- el `Profesor` solicita editar una `Sesion` desde su fila en el listado.
- **Control:** `PlanificacionDocenteController`.
- **Salida:** `:PLANIFICACION_DOCENTE_ABIERTO` -- self-loop, "datos actualizados, número sin cambios".

## Clases de controlador

### `PlanificacionDocenteController`

**Responsabilidades:**
- recupera la `Sesion` a editar (`SesionRepository.obtener(sesionId)`).
- valida los obligatorios (`tipo`, `descripcion`).
- persiste la actualización: la `Sesion` se actualiza a sí misma y el repositorio la guarda.

**Colaboraciones:**
- **Entrada:** `EditarSesionView`.
- **Salida:** `Sesion`, `SesionRepository`.

## Clases de modelo

### `Sesion`

**Responsabilidades:**
- porta `numero` (visible, no editable), `tipo` (enum cerrado de seis valores) y `descripcion` -- los dos últimos editables.
- se actualiza a sí misma (`actualizar(tipo, descripcion)`).

**Colaboraciones:**
- **Entrada:** `PlanificacionDocenteController`.
- **Salida:** persistida por `SesionRepository`.

### `SesionRepository`

**Responsabilidades:**
- recupera la `Sesion` por identificador (`obtener(sesionId)`).
- persiste la actualización (`actualizar(sesion)`).

**Colaboraciones:**
- **Entrada:** `PlanificacionDocenteController`.
- **Salida:** gestiona `Sesion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarSesion/wireframes.puml) -- fuente de verdad del formulario editable.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PLANIFICACION_DOCENTE_ABIERTO --> PLANIFICACION_DOCENTE_ABIERTO : editarSesion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Sesion{numero, tipo, descripcion}`.
- [`crearSesion()`](../crearSesion/README.md) -- quien asigna el `numero` correlativo que aquí permanece sin cambios.
- [`abrirPlanificacionDocente()`](../abrirPlanificacionDocente/README.md) / [`eliminarSesion()`](../eliminarSesion/README.md) -- mismo lote sobre el mismo estado de contexto.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- quienes sincronizan la vinculación de las sesiones.
- [Discussion #140](https://github.com/mmasias/pyCelda/discussions/140) -- cierre de las 8 decisiones de diseño de la Planificación docente.

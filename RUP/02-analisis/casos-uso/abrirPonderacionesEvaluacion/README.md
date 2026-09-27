<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirPonderacionesEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirPonderacionesEvaluacion/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/abrirPonderacionesEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirPonderacionesEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/README.md): un solo paso, sin `<<choice>>`, de solo lectura -- no vincula nada. Presenta el listado completo de `PonderacionEvaluacion` de la `Guia` abierta, **fusionando** lo ya vinculado con lo pendiente-sin-vincular creado en [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md), agrupado por `SistemaEvaluacion` con la suma total. Mismo mecanismo de fusión que [`abrirGuia()`](../abrirGuia/README.md), aplicado aquí a una única colección en su propia pantalla de gestión. La Vista pide además, en paralelo, el catálogo completo de `SistemaEvaluacion` de la materia (`listarSistemasEvaluacionDeGuia()`, discussion [#38](https://github.com/mmasias/pyCelda/discussions/38)) -- no solo los que ya están en uso en esta `Guia` -- para presentar la segunda tabla "Sistemas de evaluación de la materia" con el medidor de completitud por rango (discussion [#206](https://github.com/mmasias/pyCelda/discussions/206), Bloque 1). Segunda lectura, independiente de la primera (issue [#212](https://github.com/mmasias/pyCelda/issues/212): esta rebanada original no la reflejaba).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirPonderacionesEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirPonderacionesEvaluacionView`

**Responsabilidades:**
- presenta el listado de `PonderacionEvaluacion` de la `Guia`, agrupado por `SistemaEvaluacion`, con la suma total calculada a partir de la lista fusionada.
- presenta la segunda tabla "Sistemas de evaluación de la materia": todos los `SistemaEvaluacion` del catálogo, con su rango y lo asignado (subtotal de la primera tabla por sistema), resaltando en rojo el que queda fuera de rango -- incluido en 0% si `ponderacionMinima > 0` (discussion [#208](https://github.com/mmasias/pyCelda/issues/208)).
- ofrece la navegación a crear una nueva ponderación, a abrir/eliminar cada fila, y a volver a la `Guia`.

**Colaboraciones:**
- **Entrada:** `:GUIA_ABIERTO` -- el `Profesor` solicita abrir el listado de ponderaciones desde la `Guia`; `:PONDERACION_EVALUACION_ABIERTO` -- el `Profesor` solicita volver al listado desde el detalle de una ponderación. Mismo caso de uso invocado desde ambos puntos.
- **Control:** `PonderacionEvaluacionController`.
- **Salida:** `:PONDERACIONES_EVALUACION_ABIERTO`.

## Clases de controlador

### `PonderacionEvaluacionController`

**Responsabilidades:**
- pide, para la `Guia`, las `PonderacionEvaluacion` ya vinculadas y las pendientes-sin-vincular por separado, y las fusiona en una sola lista por presentar -- mismo criterio que `GuiaController` en `abrirGuia()`: unión simple, sin regla de negocio.
- resuelve, en una segunda lectura independiente, el catálogo de `SistemaEvaluacion` de la materia de la `Guia` (`listarSistemasEvaluacionDeGuia(guiaId)`): `Guia` -> `AsignaturaGrado` -> `Materia` -> `Materia.listarSistemasEvaluacion()` -- no hay un repositorio de `SistemaEvaluacion` involucrado en esta ruta, se llega a través de `Materia` (issue [#212](https://github.com/mmasias/pyCelda/issues/212)).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirPonderacionesEvaluacionView`.
- **Salida:** `GuiaRepository`, `AsignaturaGradoRepository`, `MateriaRepository`, `PonderacionEvaluacionRepository`.

## Clases de modelo

### `Guia`, `AsignaturaGrado`, `Materia`

**Responsabilidades:**
- `Guia` porta `asignaturaGradoId`, usado para llegar a la `AsignaturaGrado` de esta `Guia`; `AsignaturaGrado` porta `materiaId`, usado para llegar a su `Materia`; `Materia` expone su catálogo de `SistemaEvaluacion` (`listarSistemasEvaluacion()`). Ninguna de las tres aplica lógica propia aquí -- es una cadena de tres saltos para llegar al catálogo, sin regla de dominio de por medio.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`, vía `GuiaRepository` / `AsignaturaGradoRepository` / `MateriaRepository` respectivamente.
- Ver [`abrirGuia()`](../abrirGuia/README.md) para el resto de responsabilidades de `Guia`/`AsignaturaGrado`, y [`abrirMateria()`](../abrirMateria/README.md) para `Materia` -- aquí solo actúan como cadena de acceso al catálogo.

### `GuiaRepository`, `AsignaturaGradoRepository`, `MateriaRepository`

**Responsabilidades:**
- `GuiaRepository.obtener(guiaId)` -- recupera la `Guia`, para la precondición de acceso y para llegar a su `AsignaturaGrado`.
- `AsignaturaGradoRepository.obtener(asignaturaGradoId)` -- recupera la `AsignaturaGrado` de la `Guia`.
- `MateriaRepository.obtener(materiaId)` -- recupera la `Materia` de esa `AsignaturaGrado`.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.

### `PonderacionEvaluacion`

**Responsabilidades:**
- porta `descripcion`, `ponderacion`, el enlace a su `SistemaEvaluacion` y si está vinculada -- mostrada agrupada, con la suma total calculada por la Vista a partir de la lista fusionada.

**Colaboraciones:**
- **Entrada:** listada por `PonderacionEvaluacionRepository`, vinculada o pendiente.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- lista las `PonderacionEvaluacion` vinculadas a la `Guia` (`listarVinculadasDe(guia)`).
- lista las `PonderacionEvaluacion` con este `guiaId` todavía sin vincular (`listarPendientesDe(guiaId)`).

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** gestiona `PonderacionEvaluacion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionesEvaluacion/wireframes.puml) -- fuente de verdad del listado agrupado con suma total.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `GUIA_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : abrirPonderacionesEvaluacion()`, `PONDERACION_EVALUACION_ABIERTO --> PONDERACIONES_EVALUACION_ABIERTO : abrirPonderacionesEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-d- PonderacionEvaluacion`, `PonderacionEvaluacion -> SistemaEvaluacion`.
- [`abrirGuia()`](../abrirGuia/README.md) -- mismo mecanismo de fusión vinculado+pendiente, aplicado a cada colección de la Guía.
- [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) / [`eliminarPonderacionEvaluacion()`](../eliminarPonderacionEvaluacion/README.md) / [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) -- quienes crean, quitan o editan lo que este listado presenta.
- [`abrirPonderacionEvaluacion()`](../abrirPonderacionEvaluacion/README.md) -- detalle de solo lectura de una fila, alcanzado desde este listado.
- [`abrirMateria()`](../abrirMateria/README.md) -- gestiona el catálogo de `SistemaEvaluacion` que esta pantalla solo consulta de solo lectura.
- Discussion [#38](https://github.com/mmasias/pyCelda/discussions/38) -- origen de `listarSistemasEvaluacionDeGuia()`: el Profesor necesita ver el catálogo completo de rangos válidos, no solo los ya usados en esta Guía.
- [Issue #212](https://github.com/mmasias/pyCelda/issues/212) -- deriva de este artefacto anterior a #206, cerrada aquí: faltaba la segunda lectura de `SistemaEvaluacion` y la segunda tabla que presenta.

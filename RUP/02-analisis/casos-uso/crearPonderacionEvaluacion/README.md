<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > crearPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearPonderacionEvaluacion/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearPonderacionEvaluacion/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearPonderacionEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/README.md): CRUD real e inmediato contra `PonderacionEvaluacionRepository`, sin ninguna interacción con `Guia`. La única validación es el **máximo puntual**: el valor introducido, por sí solo, no puede superar `ponderacionMaxima` de su `SistemaEvaluacion` -- no se comprueba contra la suma de hermanas ni contra el mínimo (ambos son reglas agregadas, se validan en [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md), no aquí). La fila se crea con `guiaId` desde el principio, pero no queda vinculada a la colección oficial de la `Guia` hasta que se guarde el borrador o se envíe a revisión.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearPonderacionEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearPonderacionEvaluacionView`

**Responsabilidades:**
- presenta el formulario de creación: selector `SistemaEvaluacion`, `descripcion` y `ponderacion`, todos obligatorios.
- presenta el aviso de rechazo cuando el `<<choice>>` sale rojo: la ponderación introducida supera el máximo del sistema elegido.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:PONDERACIONES_EVALUACION_ABIERTO` -- el `Profesor` solicita crear una ponderación para la `Guia` que tiene abierta.
- **Control:** `PonderacionEvaluacionController`.
- **Salida:** `:Collaboration EditarPonderacionEvaluacion` vía `<<include>> editarPonderacionEvaluacion()` (éxito); `:PONDERACIONES_EVALUACION_ABIERTO` (fallo, sin crear).

## Clases de controlador

### `PonderacionEvaluacionController`

**Responsabilidades:**
- carga los `SistemaEvaluacion` ofrecidos: los de la `Materia` de la `AsignaturaGrado` de la `Guia` -- el selector aplica la regla de consistencia del dominio.
- valida los obligatorios (`sistemaEvaluacion`, `descripcion`, `ponderacion`).
- aplica el `<<choice>>` del máximo puntual: `ponderacion <= ponderacionMaxima` del sistema elegido -> crea directamente en `PonderacionEvaluacionRepository`; por encima -> no crea nada.

**Colaboraciones:**
- **Entrada:** `CrearPonderacionEvaluacionView`.
- **Salida:** `Materia`, `SistemaEvaluacion`, `PonderacionEvaluacionRepository`.

## Clases de modelo

### `PonderacionEvaluacion`

**Responsabilidades:**
- porta `descripcion`, `ponderacion`, el enlace a su `SistemaEvaluacion` y `guiaId` -- pertenece a una `Guia` desde su creación, aunque todavía no esté vinculada a su colección oficial.

**Colaboraciones:**
- **Entrada:** creada por `PonderacionEvaluacionRepository`.
- **Salida:** apunta a un `SistemaEvaluacion`.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- crea la `PonderacionEvaluacion` (`crear(guiaId, sistemaEvaluacion, descripcion, ponderacion)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** gestiona `PonderacionEvaluacion`.

### `SistemaEvaluacion`

**Responsabilidades:**
- conoce su `ponderacionMaxima` y responde si un valor puntual la supera (`validarMaximo(ponderacion)`) -- validación individual, no agregada.
- porta `tipo` (enum: "Evaluación continua" / "Evaluación final") y `descripcion`.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** objetivo de `PonderacionEvaluacion`; definido por `Materia`.

### `Materia`

**Responsabilidades:**
- ofrece sus `SistemaEvaluacion` oficiales (`Materia *-- SistemaEvaluacion`), universo de opciones del selector.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** define los `SistemaEvaluacion` ofertados.

## Hallazgo: posible hueco en el wireframe de Requisitos

El wireframe de Requisitos (`crearPonderacionEvaluacion-wireframe-formulario`) todavía muestra un panel "Ya asignado en esta Guía... / Margen disponible..." -- un cálculo agregado contra las hermanas de la `Guia`. Con la validación reducida al máximo puntual, ese panel ya no tiene de dónde sacar el dato en este caso de uso (la suma agregada ahora solo se calcula en `enviarGuiaARevision()`, y ahí no hay formulario que mostrarlo). No se ha tocado el wireframe de Requisitos -- señalado para que el usuario decida si se retira el panel o se sustituye por algo que sí es calculable aquí (p.ej. solo el rango, sin "ya asignado").

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearPonderacionEvaluacion/wireframes.puml) -- fuente de verdad del `<<choice>>` (ver hallazgo arriba sobre el panel de margen).
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACIONES_EVALUACION_ABIERTO --> PONDERACION_EVALUACION_ABIERTO : crearPonderacionEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-d- PonderacionEvaluacion`, `PonderacionEvaluacion -> SistemaEvaluacion`, `Materia *-- SistemaEvaluacion`.
- [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) -- misma validación de máximo puntual; [`crearReferenciaBibliografica()`](../crearReferenciaBibliografica/README.md) -- mismo patrón de CRUD independiente, sin `<<choice>>`.
- [`abrirGuia()`](../abrirGuia/README.md) -- quien fusiona lo vinculado con lo pendiente-sin-vincular para presentarlo.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- quienes vinculan esta fila a la `Guia` y validan el rango agregado por `SistemaEvaluacion` y la suma total = 100%.
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre original de dónde y cómo se valida el rango (revisado por esta corrección arquitectónica).

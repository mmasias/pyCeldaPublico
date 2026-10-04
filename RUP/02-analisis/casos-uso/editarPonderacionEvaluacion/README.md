<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarPonderacionEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/README.md): CRUD real e inmediato contra `PonderacionEvaluacionRepository`, sin ninguna interacción con `Guia`. Misma validación de máximo puntual que [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) -- sin exclusión del valor anterior, porque ya no hay suma de hermanas de la que excluirlo: el máximo se comprueba sobre el valor nuevo, en solitario.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarPonderacionEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarPonderacionEvaluacionView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la ponderación (`SistemaEvaluacion`, `descripcion`, `ponderacion`).
- presenta el aviso de rechazo cuando el `<<choice>>` sale rojo.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:PONDERACION_EVALUACION_ABIERTO` -- el `Profesor` solicita editar la ponderación abierta.
- **Control:** `PonderacionEvaluacionController`.
- **Salida:** `:PONDERACION_EVALUACION_ABIERTO` en ambos casos -- self-loop con "datos actualizados" (verde) o "sin cambios" (rojo).

## Clases de controlador

### `PonderacionEvaluacionController`

**Responsabilidades:**
- recupera la `PonderacionEvaluacion` a editar (`PonderacionEvaluacionRepository.obtener(ponderacionId)`).
- carga los `SistemaEvaluacion` ofertados: los de la `Materia` de la `AsignaturaPrograma` de la `Guia`.
- valida los obligatorios (`sistemaEvaluacion`, `descripcion`, `ponderacion`).
- aplica el `<<choice>>` del máximo puntual: dentro -> la `PonderacionEvaluacion` se actualiza a sí misma y se persiste; por encima -> no se toca nada.

**Colaboraciones:**
- **Entrada:** `EditarPonderacionEvaluacionView`.
- **Salida:** `PonderacionEvaluacion`, `PonderacionEvaluacionRepository`, `Materia`, `SistemaEvaluacion`.

## Clases de modelo

### `PonderacionEvaluacion`

**Responsabilidades:**
- porta `descripcion`, `ponderacion` y el enlace a su `SistemaEvaluacion` -- los tres editables.
- se actualiza a sí misma (`actualizar(sistemaEvaluacion, descripcion, ponderacion)`) en la rama verde.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** apunta a un `SistemaEvaluacion`; persistida por `PonderacionEvaluacionRepository`.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- recupera la `PonderacionEvaluacion` por identificador (`obtener(ponderacionId)`).
- persiste la actualización, solo en la rama verde (`actualizar(ponderacion)`).

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** gestiona `PonderacionEvaluacion`.

### `SistemaEvaluacion`

**Responsabilidades:**
- conoce su `ponderacionMaxima` y responde si un valor puntual la supera (`validarMaximo(ponderacion)`).
- porta `tipo` y `descripcion`.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** objetivo de `PonderacionEvaluacion`; definido por `Materia`.

### `Materia`

**Responsabilidades:**
- ofrece sus `SistemaEvaluacion` oficiales, universo de opciones del selector editable.

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** define los `SistemaEvaluacion` ofertados.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/wireframes.puml) -- fuente de verdad del `<<choice>>` (mismo hallazgo del panel de margen que [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md), ver su README).
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACION_EVALUACION_ABIERTO --> PONDERACION_EVALUACION_ABIERTO : editarPonderacionEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PonderacionEvaluacion{descripcion, ponderacion}`, `PonderacionEvaluacion -> SistemaEvaluacion`.
- [`crearPonderacionEvaluacion()`](../crearPonderacionEvaluacion/README.md) -- misma validación de máximo puntual.
- [`guardarBorradorGuia()`](../guardarBorradorGuia/README.md) / [`enviarGuiaARevision()`](../enviarGuiaARevision/README.md) -- quienes validan el rango agregado por `SistemaEvaluacion` y la suma total.
- [Discussion #38](https://github.com/mmasias/pyCelda/discussions/38) -- cierre original de dónde y cómo se valida el rango (revisado por esta corrección arquitectónica).

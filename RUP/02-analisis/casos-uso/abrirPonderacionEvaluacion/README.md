<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPonderacionEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirPonderacionEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirPonderacionEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionEvaluacion/README.md): un solo paso, sin `<<choice>>`, de solo lectura -- muestra el detalle de una `PonderacionEvaluacion` concreta (`SistemaEvaluacion`, `descripcion`, `ponderacion`). Reutiliza el mismo método de carga que ya usa [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) para recuperar la fila.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirPonderacionEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirPonderacionEvaluacionView`

**Responsabilidades:**
- presenta `SistemaEvaluacion` (en forma legible), `descripcion` y `ponderacion` de la `PonderacionEvaluacion` abierta.
- ofrece la navegación a editar la ponderación o volver al listado.

**Colaboraciones:**
- **Entrada:** `:PONDERACIONES_EVALUACION_ABIERTO` -- el `Profesor` solicita abrir una `PonderacionEvaluacion` desde su fila en el listado.
- **Control:** `PonderacionEvaluacionController`.
- **Salida:** `:PONDERACION_EVALUACION_ABIERTO`.

## Clases de controlador

### `PonderacionEvaluacionController`

**Responsabilidades:**
- recupera la `PonderacionEvaluacion` a mostrar (`cargarPonderacionEvaluacion(ponderacionId)`) -- mismo método que reutiliza `editarPonderacionEvaluacion()`, no uno nuevo.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirPonderacionEvaluacionView`.
- **Salida:** `PonderacionEvaluacionRepository`.

## Clases de modelo

### `PonderacionEvaluacion`

**Responsabilidades:**
- porta `descripcion`, `ponderacion` y el enlace a su `SistemaEvaluacion` -- los datos mostrados, sin edición en este caso de uso.

**Colaboraciones:**
- **Entrada:** recuperada por `PonderacionEvaluacionRepository`.
- **Salida:** apunta a un `SistemaEvaluacion`.

### `PonderacionEvaluacionRepository`

**Responsabilidades:**
- recupera la `PonderacionEvaluacion` por identificador (`obtener(ponderacionId)`).

**Colaboraciones:**
- **Entrada:** `PonderacionEvaluacionController`.
- **Salida:** gestiona `PonderacionEvaluacion`.

### `SistemaEvaluacion`

**Responsabilidades:**
- porta `tipo` y `descripcion`, mostrados en forma legible junto a la ponderación.

**Colaboraciones:**
- **Entrada:** enlazado desde `PonderacionEvaluacion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirPonderacionEvaluacion/wireframes.puml) -- fuente de verdad del detalle de solo lectura.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `PONDERACIONES_EVALUACION_ABIERTO --> PONDERACION_EVALUACION_ABIERTO : abrirPonderacionEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `PonderacionEvaluacion{descripcion, ponderacion}`, `PonderacionEvaluacion -> SistemaEvaluacion`.
- [`editarPonderacionEvaluacion()`](../editarPonderacionEvaluacion/README.md) -- mismo `cargarPonderacionEvaluacion(ponderacionId)`, reutilizado aquí.
- [`abrirPonderacionesEvaluacion()`](../abrirPonderacionesEvaluacion/README.md) -- listado del que procede esta fila.

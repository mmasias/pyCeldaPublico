<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemaEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirSistemaEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemaEvaluacion/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el detalle de un `SistemaEvaluacion` concreto: `tipo`, `descripcion`, `ponderacionMinima` y `ponderacionMaxima`. También es el destino del alta de [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md) -- desde aquí se alcanza `editarSistemaEvaluacion()` y se vuelve al listado de la `Materia`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirSistemaEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirSistemaEvaluacionView`

**Responsabilidades:**
- presenta `tipo`, `descripcion`, `ponderacionMinima` y `ponderacionMaxima` del `SistemaEvaluacion`.
- ofrece la navegación a editarlo y a volver al listado de la `Materia` que lo contiene.

**Colaboraciones:**
- **Entrada:** `:SISTEMAS_EVALUACION_ABIERTO` -- el `Admin` solicita abrir un `SistemaEvaluacion`.
- **Control:** `SistemaEvaluacionController`.
- **Salida:** `:SISTEMA_EVALUACION_ABIERTO`.

## Clases de controlador

### `SistemaEvaluacionController`

**Responsabilidades:**
- recupera el `SistemaEvaluacion` (`cargarSistemaEvaluacion(sistemaEvaluacionId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirSistemaEvaluacionView`.
- **Salida:** `SistemaEvaluacionRepository`.

## Clases de modelo

### `SistemaEvaluacion`

**Responsabilidades:**
- porta `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima`.

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`, vía `SistemaEvaluacionRepository`.

### `SistemaEvaluacionRepository`

**Responsabilidades:**
- recupera el `SistemaEvaluacion` por identificador (`obtener(sistemaEvaluacionId)`) -- ya existía para el picker de `crearPonderacionEvaluacion()`; aquí gana sus primeros usos de catálogo propio.

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`.
- **Salida:** gestiona `SistemaEvaluacion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemaEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemaEvaluacion/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMAS_EVALUACION_ABIERTO --> SISTEMA_EVALUACION_ABIERTO : abrirSistemaEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `SistemaEvaluacion{tipo, descripcion, ponderacionMinima, ponderacionMaxima}`.
- [`abrirSistemasEvaluacion()`](../abrirSistemasEvaluacion/README.md) -- listado del que se alcanza este caso de uso.
- [`abrirResultadoAprendizaje()`](../abrirResultadoAprendizaje/README.md) -- mismo patrón de lectura simple por identificador bajo un padre.

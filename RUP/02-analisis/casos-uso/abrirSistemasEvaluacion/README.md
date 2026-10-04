<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirSistemasEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirSistemasEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirSistemasEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el listado de `SistemaEvaluacion` de una `Materia` concreta -- composición real (`Materia *-- SistemaEvaluacion`), no catálogo institucional: se navega desde dentro de una `Materia` ya abierta, mismo patrón que `abrirResultadosAprendizaje()` desde el `Programa`. Cada fila muestra `tipo`, `descripcion` y el rango `ponderacionMinima`--`ponderacionMaxima`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirSistemasEvaluacion/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirSistemasEvaluacionView`

**Responsabilidades:**
- presenta el listado de `SistemaEvaluacion` de la `Materia`: `tipo`, `descripcion`, rango de ponderación mínima--máxima.
- ofrece la navegación a abrir/eliminar cada uno y a crear uno nuevo (`[+ Crear Sistema de Evaluación]`), y la vuelta a la `Materia` (`abrirMateria()`).

**Colaboraciones:**
- **Entrada:** `:MATERIA_ABIERTO` -- el `Admin` solicita abrir los sistemas de evaluación de la `Materia`.
- **Control:** `SistemaEvaluacionController`.
- **Salida:** `:SISTEMAS_EVALUACION_ABIERTO`.

## Clases de controlador

### `SistemaEvaluacionController`

**Responsabilidades:**
- lista los `SistemaEvaluacion` de una `Materia` (`listarSistemasEvaluacionDeMateria(materiaId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirSistemasEvaluacionView`.
- **Salida:** `SistemaEvaluacionRepository`.

## Clases de modelo

### `SistemaEvaluacion`

**Responsabilidades:**
- porta `tipo`, `descripcion`, `ponderacionMinima`, `ponderacionMaxima` -- los datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listado por `SistemaEvaluacionRepository`.

### `SistemaEvaluacionRepository`

**Responsabilidades:**
- lista los `SistemaEvaluacion` de una `Materia` (`listarDeMateria(materiaId)`).

**Colaboraciones:**
- **Entrada:** `SistemaEvaluacionController`.
- **Salida:** gestiona `SistemaEvaluacion`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIA_ABIERTO --> SISTEMAS_EVALUACION_ABIERTO : abrirSistemasEvaluacion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia *-- SistemaEvaluacion`.
- [`abrirResultadosAprendizaje()`](../abrirResultadosAprendizaje/README.md) -- mismo patrón de listado de composición bajo un padre, allí `Programa *-d- ResultadoAprendizaje`.
- [`abrirSistemaEvaluacion()`](../abrirSistemaEvaluacion/README.md) / [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md) / [`eliminarSistemaEvaluacion()`](../eliminarSistemaEvaluacion/README.md) -- casos de uso alcanzados desde el listado.

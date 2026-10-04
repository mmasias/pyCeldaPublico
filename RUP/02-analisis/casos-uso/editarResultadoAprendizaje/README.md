<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarResultadoAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarResultadoAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/README.md): sin `<<choice>>` -- edita `codigo`, `tipo` y `descripcion`, los tres campos, precargados. A diferencia de `editarMetodologiaDocente()`, `codigo` es editable aquí (no fijo desde el alta).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarResultadoAprendizaje/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarResultadoAprendizajeView`

**Responsabilidades:**
- presenta `codigo`, `tipo`, `descripcion` con sus valores actuales.
- ofrece la navegación a solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:RESULTADO_APRENDIZAJE_ABIERTO` -- el actor (`Admin` o `DirectorPrograma`) solicita editar el `ResultadoAprendizaje`, o lo alcanza vía `<<include>>` desde [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md).
- **Control:** `ResultadoAprendizajeController`.
- **Salida:** `:RESULTADO_APRENDIZAJE_ABIERTO`.

## Clases de controlador

### `ResultadoAprendizajeController`

**Responsabilidades:**
- recupera el `ResultadoAprendizaje` y aplica los cambios (`guardarCambios(resultadoAprendizajeId, codigo, tipo, descripcion)`).

**Colaboraciones:**
- **Entrada:** `EditarResultadoAprendizajeView`.
- **Salida:** `ResultadoAprendizaje`, `ResultadoAprendizajeRepository`.

## Clases de modelo

### `ResultadoAprendizaje`

**Responsabilidades:**
- actualiza `codigo`, `tipo`, `descripcion` (`actualizar(codigo, tipo, descripcion)`).

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`, vía `ResultadoAprendizajeRepository`.

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- recupera el `ResultadoAprendizaje` por identificador (`obtener(resultadoAprendizajeId)`).
- persiste los cambios (`actualizar(resultadoAprendizaje)`).

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `RESULTADO_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : editarResultadoAprendizaje()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ResultadoAprendizaje{codigo, tipo, descripcion}`, `tipo` enum cerrado de 4 valores.
- [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md) -- caso de uso que abre el `<<include>>` hacia este mismo formulario.

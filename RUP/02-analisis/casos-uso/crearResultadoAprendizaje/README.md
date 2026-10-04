<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearResultadoAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/README.md): **sin patrón C→U**, a diferencia del resto de `crearX()` del catálogo -- `ResultadoAprendizaje{codigo, tipo, descripcion}` es demasiado minimalista para que deferir campos aporte algo, así que pide los tres a la vez. Crea real e inmediato en el catálogo del `Programa`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearResultadoAprendizaje/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearResultadoAprendizajeView`

**Responsabilidades:**
- presenta el formulario con `codigo`, `tipo`, `descripcion`, los tres obligatorios.
- ofrece la navegación a solicitar crear.

**Colaboraciones:**
- **Entrada:** `:RESULTADOS_APRENDIZAJE_ABIERTO` -- el actor (`Admin` o `DirectorPrograma`) solicita crear un `ResultadoAprendizaje`.
- **Control:** `ResultadoAprendizajeController`.
- **Salida:** `<<include>>` hacia [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md) -- mismo mecanismo que `crearPonderacionEvaluacion()`, la nota `editarX()` obligatoria en la transición de salida (regla de Requisitos). `:RESULTADO_APRENDIZAJE_ABIERTO`.

## Clases de controlador

### `ResultadoAprendizajeController`

**Responsabilidades:**
- crea real e inmediato el `ResultadoAprendizaje` en el catálogo del `Programa` (`crearResultadoAprendizaje(programaId, codigo, tipo, descripcion)`).

**Colaboraciones:**
- **Entrada:** `CrearResultadoAprendizajeView`.
- **Salida:** `ResultadoAprendizajeRepository`.

## Clases de modelo

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo`, `descripcion` desde el momento de crearse.

**Colaboraciones:**
- **Entrada:** creado por `ResultadoAprendizajeRepository`.

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- crea real e inmediato el `ResultadoAprendizaje` (`crear(programaId, codigo, tipo, descripcion)`).

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/wireframes.puml) -- fuente de verdad, incluida la corrección sobre C→U ([issue #24](https://github.com/mmasias/pyCelda/issues/24)).
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : crearResultadoAprendizaje()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-d- ResultadoAprendizaje`, `ResultadoAprendizaje{codigo, tipo, descripcion}`.
- [`editarResultadoAprendizaje()`](../editarResultadoAprendizaje/README.md) -- `<<include>>` de salida, mismo formulario que este caso de uso.

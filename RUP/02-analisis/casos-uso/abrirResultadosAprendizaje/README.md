<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirResultadosAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirResultadosAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirResultadosAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el catálogo de `ResultadoAprendizaje` propio del `Programa` -- catálogo del `Programa`, no institucional (`Programa *-d- ResultadoAprendizaje`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirResultadosAprendizaje/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirResultadosAprendizajeView`

**Responsabilidades:**
- presenta el catálogo de `ResultadoAprendizaje` del `Programa`: `codigo`, `tipo`, `descripcion`.
- ofrece la navegación a abrir/eliminar cada uno y a crear uno nuevo.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el actor (`Admin` o `DirectorPrograma`) solicita abrir el catálogo de ResultadosAprendizaje.
- **Control:** `ResultadoAprendizajeController`.
- **Salida:** `:RESULTADOS_APRENDIZAJE_ABIERTO`.

## Clases de controlador

### `ResultadoAprendizajeController`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` de un `Programa` (`listarResultadosAprendizajeDelPrograma(programaId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirResultadosAprendizajeView`.
- **Salida:** `ResultadoAprendizajeRepository`.

## Clases de modelo

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo`, `descripcion` -- los datos mostrados en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listado por `ResultadoAprendizajeRepository`.

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` de un `Programa` (`listarDelPrograma(programaId)`).

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> RESULTADOS_APRENDIZAJE_ABIERTO : abrirResultadosAprendizaje()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-d- ResultadoAprendizaje`.
- [`abrirResultadoAprendizaje()`](../abrirResultadoAprendizaje/README.md) -- caso de uso alcanzado desde cada fila de este listado.

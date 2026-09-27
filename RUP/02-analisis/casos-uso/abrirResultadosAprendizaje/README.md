<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirResultadosAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirResultadosAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirResultadosAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el catálogo de `ResultadoAprendizaje` propio del `Grado` -- catálogo del `Grado`, no institucional (`Grado *-d- ResultadoAprendizaje`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirResultadosAprendizaje/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirResultadosAprendizajeView`

**Responsabilidades:**
- presenta el catálogo de `ResultadoAprendizaje` del `Grado`: `codigo`, `tipo`, `descripcion`.
- ofrece la navegación a abrir/eliminar cada uno y a crear uno nuevo.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `DirectorGrado` solicita abrir el catálogo de ResultadosAprendizaje.
- **Control:** `ResultadoAprendizajeController`.
- **Salida:** `:RESULTADOS_APRENDIZAJE_ABIERTO`.

## Clases de controlador

### `ResultadoAprendizajeController`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` de un `Grado` (`listarResultadosAprendizajeDelGrado(gradoId)`).
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
- lista los `ResultadoAprendizaje` de un `Grado` (`listarDelGrado(gradoId)`).

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadosAprendizaje/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> RESULTADOS_APRENDIZAJE_ABIERTO : abrirResultadosAprendizaje()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado *-d- ResultadoAprendizaje`.
- [`abrirResultadoAprendizaje()`](../abrirResultadoAprendizaje/README.md) -- caso de uso alcanzado desde cada fila de este listado.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirResultadoAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirResultadoAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/README.md): un solo paso, sin `<<choice>>`, de solo lectura. Presenta el detalle de un `ResultadoAprendizaje` concreto.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirResultadoAprendizaje/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirResultadoAprendizajeView`

**Responsabilidades:**
- presenta `codigo`, `tipo`, `descripcion` del `ResultadoAprendizaje`.
- ofrece la navegación a editarlo y a volver al listado.

**Colaboraciones:**
- **Entrada:** `:RESULTADOS_APRENDIZAJE_ABIERTO` -- el `DirectorGrado` solicita abrir un `ResultadoAprendizaje`.
- **Control:** `ResultadoAprendizajeController`.
- **Salida:** `:RESULTADO_APRENDIZAJE_ABIERTO`.

## Clases de controlador

### `ResultadoAprendizajeController`

**Responsabilidades:**
- recupera el `ResultadoAprendizaje` (`cargarResultadoAprendizaje(resultadoAprendizajeId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirResultadoAprendizajeView`.
- **Salida:** `ResultadoAprendizajeRepository`.

## Clases de modelo

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo`, `descripcion`.

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`, vía `ResultadoAprendizajeRepository`.

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- recupera el `ResultadoAprendizaje` por identificador (`obtener(resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/wireframes.puml) -- fuente de verdad del contenido presentado.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : abrirResultadoAprendizaje()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ResultadoAprendizaje{codigo, tipo, descripcion}`.
- [`abrirResultadosAprendizaje()`](../abrirResultadosAprendizaje/README.md) -- listado del que se alcanza este caso de uso.

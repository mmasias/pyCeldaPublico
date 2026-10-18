<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarModulo()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarModulo/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`eliminarModulo()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/README.md) (issue [#762](https://github.com/mmasias/pyCelda/issues/762)): el `<<choice>>` depende de las materias del módulo; el controlador lo comprueba al borrar y devuelve sus nombres si las hay.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarModulo/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarModuloView`

**Responsabilidades:**
- presenta el bloqueo con las materias del módulo, o la confirmación.

**Colaboraciones:**
- **Entrada:** `:MODULOS_ABIERTO`.
- **Control:** `ModuloController`.
- **Salida:** `:MODULOS_ABIERTO` (tres ramas).

## Clases de controlador

### `ModuloController`

**Responsabilidades:**
- rechaza el borrado si el módulo tiene materias (409 con los nombres); si no, lo borra.

**Colaboraciones:**
- **Entrada:** `EliminarModuloView`.
- **Salida:** `Modulo`, `ModuloRepository`.

## Clases de modelo

### `Modulo`

**Responsabilidades:**
- porta `codigo`, `nombre`, `descripcion` (opcional) y conoce sus `Materia`.

**Colaboraciones:**
- **Entrada:** gestionado por `ModuloRepository`.

### `ModuloRepository`

**Responsabilidades:**
- gestiona `Modulo` y cuenta las materias de cada uno.

**Colaboraciones:**
- **Entrada:** `ModuloController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarModulo/wireframes.puml) -- fuente de verdad

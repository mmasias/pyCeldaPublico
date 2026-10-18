<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarModulo()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarModulo/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarModulo/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`editarModulo()`](/RUP/01-requisitos/03-detalle-casos-uso/editarModulo/README.md) (issue [#762](https://github.com/mmasias/pyCelda/issues/762)): formulario de `codigo`, `nombre` (obligatorios) y `descripcion` (opcional), con el `<<choice>>` de código repetido en el `Programa` resuelto por el controlador. Sin ficha del módulo: la salida es el listado.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarModulo/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarModuloView`

**Responsabilidades:**
- presenta el formulario con los datos actuales.
- presenta el mensaje de código repetido sin perder lo escrito.

**Colaboraciones:**
- **Entrada:** `:MODULOS_ABIERTO`.
- **Control:** `ModuloController`.
- **Salida:** `:MODULOS_ABIERTO`.

## Clases de controlador

### `ModuloController`

**Responsabilidades:**
- valida que el `codigo` no lo use otro módulo del `Programa`.
- aplica los cambios con `Modulo.actualizar()`.

**Colaboraciones:**
- **Entrada:** `EditarModuloView`.
- **Salida:** `ModuloRepository`.

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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarModulo/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarModulo/wireframes.puml) -- fuente de verdad

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirModulos()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirModulos/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis de [`abrirModulos()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/README.md) (issue [#762](https://github.com/mmasias/pyCelda/issues/762)): listado de los `Modulo` del `Programa` con su número de materias. Es también el punto de gestión (crear, editar, eliminar desde la fila).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirModulos/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirModulosView`

**Responsabilidades:**
- presenta código, nombre, descripción y nº de materias, con entrada a crear, editar y eliminar.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` (`Admin`).
- **Control:** `ModuloController`.
- **Salida:** `:MODULOS_ABIERTO`.

## Clases de controlador

### `ModuloController`

**Responsabilidades:**
- compone el listado con el conteo de materias.

**Colaboraciones:**
- **Entrada:** `AbrirModulosView`.
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

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirModulos/wireframes.puml) -- fuente de verdad
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Modulo`, `Modulo o-- Materia`

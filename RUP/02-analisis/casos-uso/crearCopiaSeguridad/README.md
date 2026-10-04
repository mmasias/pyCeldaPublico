<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearCopiaSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearCopiaSeguridad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearCopiaSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearCopiaSeguridad()`](/RUP/01-requisitos/03-detalle-casos-uso/crearCopiaSeguridad/README.md) (issues [#632](https://github.com/mmasias/pyCelda/issues/632) y [#633](https://github.com/mmasias/pyCelda/issues/633)): un solo paso, sin `<<choice>>`. Parte de `COPIAS_SEGURIDAD_ABIERTO` (autotransición), guarda una copia de la base de datos actual, la anota en el manifiesto y vuelve al listado. Sin entidad del modelo del dominio: la copia vive en el manifiesto, como en [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearCopiaSeguridad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearCopiaSeguridadView`

**Responsabilidades:**
- ofrece un panel con un motivo opcional y las acciones Crear y Cancelar.
- con Cancelar no se crea nada; con Crear, tras guardar la copia, presenta el listado actualizado.
- ante un fallo técnico muestra el mensaje de error en el panel y no crea la copia.

**Colaboraciones:**
- **Entrada:** `:COPIAS_SEGURIDAD_ABIERTO`.
- **Control:** `CopiaSeguridadController`.
- **Salida:** `:COPIAS_SEGURIDAD_ABIERTO`.

## Clases de controlador

### `CopiaSeguridadController`

**Responsabilidades:**
- crea la copia (`crearCopia()`) de la base de datos actual, de familia puntual y con la versión de esquema actual.
- solo lee la base de datos viva; deja registro de quién la pidió y qué archivo se creó.

**Colaboraciones:**
- **Entrada:** `CrearCopiaSeguridadView`.
- **Salida:** `ManifiestoCopiasSeguridad`.

## Clases de modelo

### `ManifiestoCopiasSeguridad`

**Responsabilidades:**
- anota la copia nueva (`anotarCopia()`): fecha, familia, archivo, tamaño, motivo y versión de esquema.

**Colaboraciones:**
- **Entrada:** `CopiaSeguridadController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearCopiaSeguridad/README.md).
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- caso de uso hermano.

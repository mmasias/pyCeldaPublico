<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > comprobarCopiasSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/comprobarCopiasSeguridad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/comprobarCopiasSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`comprobarCopiasSeguridad()`](/RUP/01-requisitos/03-detalle-casos-uso/comprobarCopiasSeguridad/README.md) (issue [#683](https://github.com/mmasias/pyCelda/issues/683)): un solo paso, sin `<<choice>>`, de solo lectura, bajo demanda y sin estado. Parte de `COPIAS_SEGURIDAD_ABIERTO` (autotransición) y presenta la salud de cada copia del manifiesto. Misma fuente que [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md): sin entidad del modelo del dominio, solo el manifiesto.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/comprobarCopiasSeguridad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ComprobarCopiasSeguridadView`

**Responsabilidades:**
- presenta la salud de cada copia en la propia tabla (correcta, dañada con su detalle, ilegible, no disponible) y un resumen de una línea.
- el resultado vive en la pantalla hasta que se recarga; no se persiste.
- cubre todas las copias, incluidas las ocultas por el filtro de restaurables; el resumen cuenta también las ocultas dañadas o ilegibles.

**Colaboraciones:**
- **Entrada:** `:COPIAS_SEGURIDAD_ABIERTO`.
- **Control:** `CopiaSeguridadController`.
- **Salida:** `:COPIAS_SEGURIDAD_ABIERTO`.

## Clases de controlador

### `CopiaSeguridadController`

**Responsabilidades:**
- comprueba la integridad de cada copia (`comprobarCopias()`), en el mismo orden que el listado, con la misma comprobación que la restauración.
- un fallo en una copia no interrumpe las demás; no borra, mueve ni marca nada.

**Colaboraciones:**
- **Entrada:** `ComprobarCopiasSeguridadView`.
- **Salida:** `ManifiestoCopiasSeguridad`.

## Clases de modelo

### `ManifiestoCopiasSeguridad`

**Responsabilidades:**
- lee las copias (`leerCopias()`) igual que en [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md); aquí solo se lee, nunca se escribe.

**Colaboraciones:**
- **Entrada:** `CopiaSeguridadController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/comprobarCopiasSeguridad/README.md).
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- caso de uso hermano.

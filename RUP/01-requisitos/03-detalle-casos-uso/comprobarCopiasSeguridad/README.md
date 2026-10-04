<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/comprobarCopiasSeguridad/README.md) / [Diseño](/RUP/03-diseño/casos-uso/comprobarCopiasSeguridad/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > comprobarCopiasSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/comprobarCopiasSeguridad/README.md)|[Diseño](/RUP/03-diseño/casos-uso/comprobarCopiasSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/comprobarCopiasSeguridad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/comprobarCopiasSeguridad/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Comprobar en cualquier momento si las copias de seguridad del volumen están sanas, antes de una emergencia|
|**Tipo**|Primario, de apoyo (soporte a la operación)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issue [#683](https://github.com/mmasias/pyCelda/issues/683)). El impedimento de restaurar una copia dañada (#681) avisa justo cuando se necesita la copia; este caso de uso adelanta ese aviso. Desde `COPIAS_SEGURIDAD_ABIERTO` el `Admin` solicita comprobar las copias y el `Sistema` presenta, en la propia tabla, la salud de cada una (correcta, dañada, ilegible o no disponible) y un resumen de una línea.

**Reglas**: bajo demanda, nunca al cargar la pantalla (el listado de [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) no cambia); solo lectura (no borra, no mueve, no marca y no escribe en el manifiesto); sin estado (el resultado vive en la pantalla hasta que se recarga); misma verdad que restaurar (misma comprobación de integridad que la restauración); cubre todas las copias, incluidas las ocultas por el filtro de #634.

**Sin `<<choice>>`**: ninguna precondición puede rechazar la comprobación; el fallo de una copia es un resultado, no un error, y no interrumpe la comprobación de las demás. Autotransición de `COPIAS_SEGURIDAD_ABIERTO`, no de `SISTEMA_DISPONIBLE`: la acción se pide desde la pantalla de copias.

## Notas de diseño y trazabilidad

- Presentación (issue [#683](https://github.com/mmasias/pyCelda/issues/683)): la columna Salud está vacía hasta pulsar el botón; el resultado es solo lectura (no borra, no marca, no persiste) y comprueba todas las copias, también las ocultas por el filtro (#634). El texto de resumen del wireframe ("28 correctas, 1 dañadas, ...") es el resumen de una línea.

- Modelado: autotransición de `COPIAS_SEGURIDAD_ABIERTO` (issue #683), bajo demanda, solo lectura y sin estado. Ninguna precondición puede rechazarla: un fallo en una copia es un resultado (dañada, ilegible, no disponible), no un error, por eso no hay `<<choice>>`.

- El "deploy 307" del motivo en el wireframe (y en el de [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md)) es un ejemplo de motivo de copia; referencia a issue #307 solo como origen del ejemplo.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `COPIAS_SEGURIDAD_ABIERTO --> COPIAS_SEGURIDAD_ABIERTO : comprobarCopiasSeguridad()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- package "Copias de seguridad"
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- pantalla desde la que se pide
- Issue [#683](https://github.com/mmasias/pyCelda/issues/683) -- origen del caso de uso

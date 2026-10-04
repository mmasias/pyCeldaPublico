<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > restaurarCopiaSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/restaurarCopiaSeguridad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/restaurarCopiaSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`restaurarCopiaSeguridad()`](/RUP/01-requisitos/03-detalle-casos-uso/restaurarCopiaSeguridad/README.md) (issues [#629](https://github.com/mmasias/pyCelda/issues/629) y [#631](https://github.com/mmasias/pyCelda/issues/631)): parte de `COPIAS_SEGURIDAD_ABIERTO`, valida la copia elegida (listado, existencia, integridad, esquema) con un único `<<choice>>` de rechazos, guarda una copia previa y sobrescribe la base de datos, tras lo cual el sistema se reinicia. Sin entidad nueva del modelo del dominio: opera sobre el manifiesto de copias y sobre la base de datos viva.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/restaurarCopiaSeguridad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `RestaurarCopiaSeguridadView`

**Responsabilidades:**
- ofrece **Restaurar** por fila, deshabilitado con su motivo si la copia no es restaurable (no disponible, versión de esquema ilegible, esquema incompatible).
- solicita confirmación escribiendo el nombre exacto del archivo.
- presenta el aviso de restauración en curso (recargar en 30 segundos) o el mensaje de rechazo.

**Colaboraciones:**
- **Entrada:** `:COPIAS_SEGURIDAD_ABIERTO`.
- **Control:** `CopiaSeguridadController`.
- **Salida:** `:COPIAS_SEGURIDAD_ABIERTO`.

## Clases de controlador

### `CopiaSeguridadController`

**Responsabilidades:**
- valida la copia en orden: figura en el manifiesto y existe; abre y pasa la integridad; esquema igual al de la base de datos viva. Cualquier fallo rechaza sin escribir nada.
- si es restaurable, registra una copia previa de la base de datos actual y ordena la sobrescritura una vez enviada la respuesta.

**Colaboraciones:**
- **Entrada:** `RestaurarCopiaSeguridadView`.
- **Salida:** `ManifiestoCopiasSeguridad`, `BaseDatosViva`.

## Clases de modelo

### `ManifiestoCopiasSeguridad`

**Responsabilidades:**
- lee las copias (`leerCopias()`) y registra la copia previa (`registrarCopiaPrevia()`, familia `pre_restauracion`, motivo "antes de restaurar X").

**Colaboraciones:**
- **Entrada:** `CopiaSeguridadController`.

### `BaseDatosViva`

**Responsabilidades:**
- informa de su versión de esquema (`versionEsquema()`) y se sobrescribe con la copia elegida (`sobrescribir()`), tras lo cual el sistema se reinicia.

**Colaboraciones:**
- **Entrada:** `CopiaSeguridadController`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/restaurarCopiaSeguridad/README.md).
- [`comprobarCopiasSeguridad()`](../comprobarCopiasSeguridad/README.md) -- misma comprobación de integridad.

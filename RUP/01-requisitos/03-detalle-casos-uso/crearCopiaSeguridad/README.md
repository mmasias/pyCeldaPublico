<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearCopiaSeguridad/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearCopiaSeguridad/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearCopiaSeguridad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearCopiaSeguridad/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearCopiaSeguridad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearCopiaSeguridad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearCopiaSeguridad/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Hacer, cuando lo necesite, una copia de seguridad de la base de datos actual, con un motivo opcional que la identifique|
|**Tipo**|Primario, de apoyo (soporte a la operación)|
|**Nivel**|Objetivo de usuario|

</div>

**Caso de uso nuevo** (issues [#632](https://github.com/mmasias/pyCelda/issues/632) y [#633](https://github.com/mmasias/pyCelda/issues/633), sobre la base de [#629](https://github.com/mmasias/pyCelda/issues/629)). Desde `COPIAS_SEGURIDAD_ABIERTO` el `Admin` pulsa "Hacer copia de seguridad ahora"; el `Sistema` le ofrece un campo de motivo opcional, con Crear y Cancelar. Al crear, el `Sistema` guarda la copia, la anota en el manifiesto y recarga el listado, donde la copia nueva aparece como la más reciente. Con Cancelar no se crea nada y se vuelve al listado.

**Reglas**: la copia es de familia `puntual` y nace con la versión de esquema de la base de datos actual, de modo que es restaurable desde el primer momento; el nombre es `pyCelda-puntual-YYYYMMDD-HHMMSS.db` (con sufijo `-N` si ya existe uno igual); solo lee la base de datos viva, no la modifica; el motivo es texto libre y opcional (vacío equivale a sin motivo); queda registro en el log con el `Admin` y el archivo.

**Sin `<<choice>>`**: ninguna regla de negocio puede rechazar la creación (el motivo es libre y sin validación). Un fallo técnico (p. ej. disco lleno) se muestra como mensaje de error en el panel, sin crear la copia. Autotransición de `COPIAS_SEGURIDAD_ABIERTO`, no de `SISTEMA_DISPONIBLE`: la acción se pide desde la pantalla de copias.

## Notas de diseño y trazabilidad

- **Origen**: issues [#632](https://github.com/mmasias/pyCelda/issues/632) y [#633](https://github.com/mmasias/pyCelda/issues/633); reutiliza la función de copia puntual de [#629](https://github.com/mmasias/pyCelda/issues/629), que también usa la restauración para su copia previa.
- **Panel en la propia pantalla**: no hay pantalla nueva; el panel con el motivo aparece sobre el listado, con el botón de creación deshabilitado mientras esté abierto.
- **Presentación**: el botón lleva el icono 📦 en pantalla ("📦 Hacer copia de seguridad ahora"); el campo de motivo muestra el texto de ayuda "Motivo (opcional)".

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `COPIAS_SEGURIDAD_ABIERTO --> COPIAS_SEGURIDAD_ABIERTO : crearCopiaSeguridad()`
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- pantalla desde la que se pide
- Issues [#632](https://github.com/mmasias/pyCelda/issues/632), [#633](https://github.com/mmasias/pyCelda/issues/633) y [#629](https://github.com/mmasias/pyCelda/issues/629) -- origen del caso de uso

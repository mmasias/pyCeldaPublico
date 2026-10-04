<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirUniversidad/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirUniversidad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirUniversidad/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirUniversidad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidad/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el detalle de una `Universidad` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Retocado el wireframe al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496)), sin tocar la especificación**: el listado de `Facultad` gana la columna "Programas" -- contador derivado del número de `Programa` de cada `Facultad`, issue [#487](https://github.com/mmasias/pyCelda/issues/487). De paso se corrige una divergencia previa entre el wireframe y `Universidad.tsx`: el código real ya mostraba la tabla de Facultades en línea en esta misma pantalla (sin pasar por un botón `[Ver Facultades]` hacia otra pantalla, que el wireframe anterior sí sugería) -- se actualiza el wireframe para reflejarlo, hallazgo incidental al tocar este fichero por #487, no un caso de uso nuevo.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `UNIVERSIDADES_ABIERTO --> UNIVERSIDAD_ABIERTO : abrirUniversidad()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Universidad`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad`, entidad raíz del catálogo institucional
- [Issue #487](https://github.com/mmasias/pyCelda/issues/487) -- origen de la columna "Programas"

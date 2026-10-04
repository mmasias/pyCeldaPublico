<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirUniversidades/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirUniversidades/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirUniversidades()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirUniversidades/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirUniversidades/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirUniversidades/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `Universidad` del catálogo institucional|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

**Retocado el wireframe al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496)), sin tocar la especificación**: el listado gana la columna "Facultades" -- contador derivado (`COUNT` agregado, sin N+1) del número de `Facultad` de cada `Universidad`, issue [#487](https://github.com/mmasias/pyCelda/issues/487). Mismo patrón de campo calculado ya usado en `elegible_para_activar`/`tiene_guia_asociada`/`num_asignaturas_programa`, sin columna nueva en el modelo de dominio.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> UNIVERSIDADES_ABIERTO : abrirUniversidades()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Universidad`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad`, entidad raíz del catálogo institucional
- [Issue #487](https://github.com/mmasias/pyCelda/issues/487) -- origen de la columna "Facultades"

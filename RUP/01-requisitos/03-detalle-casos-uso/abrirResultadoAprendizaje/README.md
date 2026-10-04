<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirResultadoAprendizaje/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirResultadoAprendizaje/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirResultadoAprendizaje/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirResultadoAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirResultadoAprendizaje/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el detalle de un `ResultadoAprendizaje` concreto|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

RAK1 es dato real del plan de estudios de GII, aportado por el usuario en la [issue #23](https://github.com/mmasias/pyCelda/issues/23).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : abrirResultadoAprendizaje()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : abrirResultadoAprendizaje()` (compartido con `Admin` desde el issue [#642](https://github.com/mmasias/pyCelda/issues/642); pantalla propia en `/admin/...`, `*Admin.tsx`)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `ResultadoAprendizaje`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` (incluye este caso de uso desde el issue [#642](https://github.com/mmasias/pyCelda/issues/642))
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ResultadoAprendizaje{codigo, tipo, descripcion}`

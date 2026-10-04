<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadFormativa()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarActividadFormativa/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarActividadFormativa/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Editar la nombre de una `ActividadFormativa` del catálogo institucional|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Solo `nombre` es editable -- `código` es el identificador institucional fijo (`AF1`-`AF7`, ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)) y se fija en `crearActividadFormativa()`, no se toca después.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ACTIVIDAD_FORMATIVA_ABIERTO --> ACTIVIDAD_FORMATIVA_ABIERTO : editarActividadFormativa()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `ActividadFormativa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `ActividadFormativa { codigo, nombre }`; las horas por `Materia`/`AsignaturaPrograma` (`ActividadFormativaMateria`, `ActividadFormativaAsignaturaPrograma`) son otro caso de uso (`DirectorPrograma`), fuera del alcance de este

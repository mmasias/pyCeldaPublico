<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin`|
|**Objetivo**|Asociar una `MetodologiaDocente` del catálogo institucional a un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Solo elige una `MetodologiaDocente` del catálogo -- sin campos propios, `Programa o-- MetodologiaDocente` no tiene atributos de asociación. El selector solo ofrece las todavía no asociadas al `Programa`. El conjunto asociado al `Programa` es el universo del que luego eligen sus `Materia` (ver [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md)).

**Hueco de documentación hallado en la auditoría del issue [#605](https://github.com/mmasias/pyCelda/issues/605)**: el endpoint (`POST /programas/{programa_id}/metodologias-docentes`), la ruta (`/admin/programas/:id/metodologias-docentes/asociar`) y la pantalla (`AsociarMetodologiaDocentePrograma`) ya existían sin reflejo en el diagrama de contexto ni en el catálogo. Se documenta lo construido, sin cambiar comportamiento.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : asociarMetodologiaDocenteAPrograma()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : asociarMetodologiaDocenteAPrograma()` (estado distinto del catálogo institucional `METODOLOGIAS_DOCENTES_ABIERTO`)
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Programa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o-- MetodologiaDocente`
- [Issue #605](https://github.com/mmasias/pyCelda/issues/605) -- auditoría de vigencia de diagramas de contexto y catálogos

**Actualización (issue [#636](https://github.com/mmasias/pyCelda/issues/636), resuelve [#607](https://github.com/mmasias/pyCelda/issues/607))**: caso de uso compartido `DirectorPrograma` + `Admin`. El Director lo ejecuta desde la vista del Programa (`/programas/:id/metodologias-docentes/...`, componentes sin sufijo); Admin conserva `/admin/programas/:id/metodologias-docentes/...` (componentes `...Admin`). Misma pantalla conceptual: el wireframe sigue siendo válido para ambos.

**Actualización (issue [#638](https://github.com/mmasias/pyCelda/issues/638))**: el Director ejecuta este caso de uso desde su pantalla propia [`abrirMetodologiasDocentesPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/README.md) (`/programas/:id/metodologias-docentes`) y vuelve a ella; ya no está embebido en `abrirPrograma()`.

**Actualización (issue [#640](https://github.com/mmasias/pyCelda/issues/640))**: Admin también lo ejecuta desde esa pantalla (`/admin/programas/:id/metodologias-docentes`, `MetodologiasDocentesProgramaAdmin`) y vuelve a ella; ya no está embebido en `ProgramaAdmin`.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocentePrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocentePrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocentePrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocentePrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocentePrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin`|
|**Objetivo**|Desasociar una `MetodologiaDocente` de un `Programa`, siempre que ninguna `Materia` del programa la tenga asociada|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

No es un borrado de entidad (la `MetodologiaDocente` sigue en el catálogo institucional) -- es romper el vínculo `Programa o-- MetodologiaDocente`, con `<<choice>>` bloqueante: si alguna `Materia` del `Programa` la tiene asociada, el sistema rechaza (409) y nombra las `Materia` en uso (`En uso en: Materia 'X'`), mismo patrón que [`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md) un nivel más abajo. La comprobación previa (`GET .../puede-desasociarse`) devuelve la lista de `Materia` en uso; vacía significa que se puede.

**Hueco de documentación hallado en la auditoría del issue [#605](https://github.com/mmasias/pyCelda/issues/605)**: endpoint (`DELETE /programas/{programa_id}/metodologias-docentes/{metodologia_docente_id}`), ruta (`/admin/programas/:id/metodologias-docentes/:mdId/desasociar`) y pantalla (`DesasociarMetodologiaDocentePrograma`) ya existían sin reflejo en el diagrama de contexto ni en el catálogo. Mismo actor que [`asociarMetodologiaDocenteAPrograma()`](../asociarMetodologiaDocenteAPrograma/README.md).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : desasociarMetodologiaDocentePrograma()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : desasociarMetodologiaDocentePrograma()` (estado distinto del catálogo institucional `METODOLOGIAS_DOCENTES_ABIERTO`)
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Programa`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o-- MetodologiaDocente`
- [Issue #605](https://github.com/mmasias/pyCelda/issues/605) -- auditoría de vigencia de diagramas de contexto y catálogos

**Actualización (issue [#636](https://github.com/mmasias/pyCelda/issues/636), resuelve [#607](https://github.com/mmasias/pyCelda/issues/607))**: caso de uso compartido `DirectorPrograma` + `Admin`. El Director lo ejecuta desde la vista del Programa (`/programas/:id/metodologias-docentes/...`, componentes sin sufijo); Admin conserva `/admin/programas/:id/metodologias-docentes/...` (componentes `...Admin`). Misma pantalla conceptual: el wireframe sigue siendo válido para ambos.

**Actualización (issue [#638](https://github.com/mmasias/pyCelda/issues/638))**: el Director ejecuta este caso de uso desde su pantalla propia [`abrirMetodologiasDocentesPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMetodologiasDocentesPrograma/README.md) (`/programas/:id/metodologias-docentes`) y vuelve a ella; ya no está embebido en `abrirPrograma()`.

**Actualización (issue [#640](https://github.com/mmasias/pyCelda/issues/640))**: Admin también lo ejecuta desde esa pantalla (`/admin/programas/:id/metodologias-docentes`, `MetodologiasDocentesProgramaAdmin`) y vuelve a ella; ya no está embebido en `ProgramaAdmin`.

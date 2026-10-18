<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarCompetenciaAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/desasociarCompetenciaAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Desasociar una `Competencia` de una `AsignaturaPrograma`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Sin `<<choice>>`: `AsignaturaPrograma` es el último escalón, nada depende de este reparto. **Sin la advertencia de "último elemento"** que tiene [`desasociarResultadoAprendizajeAsignaturaPrograma()`](../desasociarResultadoAprendizajeAsignaturaPrograma/README.md): una asignatura sin competencias es el caso normal en los programas de formato nuevo (#761, punto 3), así que avisar sería ruido.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasociarCompetenciaAsignaturaPrograma()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasociarCompetenciaAsignaturaPrograma()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-- Competencia`
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761)

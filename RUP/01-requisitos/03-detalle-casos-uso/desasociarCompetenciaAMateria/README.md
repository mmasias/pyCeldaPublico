<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/desasociarCompetenciaAMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/desasociarCompetenciaAMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarCompetenciaAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/desasociarCompetenciaAMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/desasociarCompetenciaAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/desasociarCompetenciaAMateria/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Desasociar una `Competencia` de una `Materia`, siempre que ninguna `AsignaturaPrograma` de esa `Materia` la tenga asignada|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`<<choice>>` bloqueante por integridad de la cascada, mismo criterio que [`desasociarResultadoAprendizajeAMateria()`](../desasociarResultadoAprendizajeAMateria/README.md): las competencias de una `AsignaturaPrograma` son subconjunto de las de su `Materia`. El bloqueo nombra las `AsignaturaPrograma` en uso; el servidor lo vuelve a comprobar al desasociar (409). Códigos y textos de los wireframes ilustrativos: las competencias reales de cada programa se importarán de las memorias verificadas una vez implementado (#761, decisión 9), no están en el seed.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarCompetenciaAMateria()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : desasociarCompetenciaAMateria()` (misma pantalla conceptual, rutas `/admin/...`)
- [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- regla de consistencia de `Competencia` (subconjunto de la `Materia`)
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761)

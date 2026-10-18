<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarCompetenciaAAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarCompetenciaAAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarCompetenciaAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarCompetenciaAAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarCompetenciaAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Con competencias disponibles|Sin competencias disponibles|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAAsignaturaPrograma/wireframe-seleccion.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAAsignaturaPrograma/wireframe-sin-disponibles.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Asociar una `Competencia` (ya asignada a la `Materia`) a una `AsignaturaPrograma`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Segundo escalón de la cascada (#761, decisión 4): el selector solo ofrece las `Competencia` ya asignadas a la `Materia` de la asignatura y no asignadas aún a ella. **A diferencia del RA, el servidor también lo exige al asociar**: una competencia del programa que no esté en la materia se rechaza (404), no solo se omite de la lista. Una ya asociada da 409.

Si no queda ninguna disponible (la materia no tiene competencias, por ser un programa de formato nuevo o por no haberse hecho el reparto, o la asignatura ya las tiene todas), no se muestra el selector: la pantalla indica "No hay competencias disponibles para asociar. Solo se pueden elegir las de la materia X que aún no tenga esta asignatura." y solo ofrece **Volver**.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asociarCompetenciaAAsignaturaPrograma()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asociarCompetenciaAAsignaturaPrograma()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-- Competencia`; [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md), regla de subconjunto
- [`asociarCompetenciaAMateria()`](../asociarCompetenciaAMateria/README.md) -- primer escalón
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761)

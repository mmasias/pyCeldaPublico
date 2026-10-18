<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarCompetenciaAMateria/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarCompetenciaAMateria/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarCompetenciaAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarCompetenciaAMateria/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarCompetenciaAMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarCompetenciaAMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Asociar una `Competencia` del catálogo del `Programa` a una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primer escalón de la cascada `Programa`->`Materia`->`AsignaturaPrograma`, mismo patrón que [`asociarResultadoAprendizajeAMateria()`](../asociarResultadoAprendizajeAMateria/README.md): agregación simple, sin atributo propio, así que solo `asociar`/`desasociar`. El selector ofrece las `Competencia` del `Programa` aún no asociadas a esta `Materia`, con `código -- extracto` en cada opción y el texto completo de la elegida debajo (mismo `extractoResultado()` que el RA). El servidor rechaza una competencia de otro programa (404) y una ya asociada (409).

**Actores**: `DirectorPrograma` sobre las materias de los programas que dirige y `Admin` sobre cualquier materia, con la misma pantalla en las dos vistas (espejo desde el diseño, #761 decisión 7). Códigos y textos de los wireframes ilustrativos: las competencias reales de cada programa se importarán de las memorias verificadas una vez implementado (#761, decisión 9), no están en el seed.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarCompetenciaAMateria()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarCompetenciaAMateria()` (misma pantalla conceptual, rutas `/admin/...`)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) y [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- Competencia`
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761)

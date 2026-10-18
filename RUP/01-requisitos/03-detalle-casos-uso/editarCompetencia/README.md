<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarCompetencia/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarCompetencia/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarCompetencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarCompetencia/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarCompetencia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarCompetencia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Editar `codigo`, `tipo` y `descripcion` de una `Competencia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismo formulario que [`crearCompetencia()`](../crearCompetencia/README.md), con los datos precargados y el mismo `<<choice>>` de código repetido (el código propio de la competencia no cuenta como repetido). `codigo` y `tipo` son editables, como en el RA. La edición se refleja en vivo en todas las materias, asignaturas y guías que la tienen asignada: la asociación no copia el texto.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `COMPETENCIA_ABIERTO --> COMPETENCIA_ABIERTO : editarCompetencia()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `COMPETENCIA_ABIERTO --> COMPETENCIA_ABIERTO : editarCompetencia()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Competencia{codigo, tipo, descripcion}`
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761)

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearCompetencia/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearCompetencia/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearCompetencia()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearCompetencia/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearCompetencia/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearCompetencia/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearCompetencia/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Dar de alta una `Competencia` en el catálogo de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Sin patrón C→U, igual que [`crearResultadoAprendizaje()`](../crearResultadoAprendizaje/README.md): los tres campos se piden a la vez. Dos diferencias con el RA (issue [#761](https://github.com/mmasias/pyCelda/issues/761)):

- **`tipo` es una selección cerrada** (Básica, General, Transversal, Específica), validada en el servidor; en el RA es texto libre. Por eso la nota del actor dice `selecciona tipo`, no `introduce tipo`.
- **`<<choice>>` de código repetido**: `codigo` es único dentro del `Programa`. Si ya lo usa otra competencia del programa, el sistema presenta el mensaje y el formulario sigue con lo escrito. No se exige que el prefijo (CB/CG/CT/CE) case con el `tipo`.

La salida lleva a la ficha de la competencia creada (`<<include>>` de `editarCompetencia()`, nota obligatoria de la transición de salida).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `COMPETENCIAS_ABIERTO --> COMPETENCIA_ABIERTO : crearCompetencia()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `COMPETENCIAS_ABIERTO --> COMPETENCIA_ABIERTO : crearCompetencia()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Competencia`; [README del modelo del dominio](/RUP/00-modelo-del-dominio/README.md), enum de `tipo` y unicidad de `codigo`
- Issue [#761](https://github.com/mmasias/pyCelda/issues/761) -- decisiones 1 a 3

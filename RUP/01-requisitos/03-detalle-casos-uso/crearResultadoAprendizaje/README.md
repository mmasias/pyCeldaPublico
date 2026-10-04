<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearResultadoAprendizaje/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearResultadoAprendizaje/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearResultadoAprendizaje/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Dar de alta un `ResultadoAprendizaje` en el catálogo de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Sin patrón C→U, a diferencia del resto de `crearX()` del catálogo**: el diseño original (caso de calibración, discussion #9) pedía solo `descripcion` y diferia `codigo`/`tipo` a `editarResultadoAprendizaje()`. Corregido en la revisión del lote L3 ([issue #24](https://github.com/mmasias/pyCelda/issues/24)): `ResultadoAprendizaje{codigo, tipo, descripcion}` es demasiado minimalista para que deferir dos de sus tres campos aporte algo -- los tres son igual de triviales de introducir en el momento de la creación, a diferencia de `Asignatura` (`crearAsignatura()` sí difiere `ects`/`contenido`/`estado`, 4 campos más allá de `nombre`). `crearResultadoAprendizaje()` y `editarResultadoAprendizaje()` terminan pidiendo el mismo formulario.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : crearResultadoAprendizaje()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : crearResultadoAprendizaje()` (compartido con `Admin` desde el issue [#642](https://github.com/mmasias/pyCelda/issues/642); pantalla propia en `/admin/...`, `*Admin.tsx`)
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `ResultadoAprendizaje`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` (incluye este caso de uso desde el issue [#642](https://github.com/mmasias/pyCelda/issues/642))
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-d- ResultadoAprendizaje`, `ResultadoAprendizaje{codigo, tipo, descripcion}`
- [Issue #24](https://github.com/mmasias/pyCelda/issues/24) -- revisión del lote L3, origen de la corrección sobre C→U

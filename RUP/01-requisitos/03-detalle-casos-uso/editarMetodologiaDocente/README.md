<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarMetodologiaDocente()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Editar `codigo` y `descripcion` de una `MetodologiaDocente` del catálogo de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismo formulario que [`crearMetodologiaDocente()`](../crearMetodologiaDocente/README.md), con los datos precargados y el mismo `<<choice>>` de código repetido (el código propio de la metodología no cuenta como repetido). `codigo` es editable, como en [`editarCompetencia()`](../editarCompetencia/README.md). La edición se refleja en vivo en todas las materias, asignaturas y guías que la tienen asignada: la asociación no copia el texto (salvo la `descripcionPropia` de una `Materia`, que se gestiona en [`editarAsociacionMetodologiaDocenteMateria()`](../editarAsociacionMetodologiaDocenteMateria/README.md), fuera de este caso).

Hasta #772 solo `descripcion` era editable y `codigo` se tenía por identificador institucional fijo (`MD1`-`MD7`); la verificación contra las memorias mostró que cada programa da a sus códigos significados propios (ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)).

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIA_DOCENTE_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : editarMetodologiaDocente()`
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIA_DOCENTE_ABIERTO --> METODOLOGIA_DOCENTE_ABIERTO : editarMetodologiaDocente()` (misma pantalla conceptual, rutas `/admin/...`)
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `MetodologiaDocente{codigo, descripcion}`; `MetodologiaMateria.descripcionPropia` es el override por materia
- Issue [#772](https://github.com/mmasias/pyCelda/issues/772)

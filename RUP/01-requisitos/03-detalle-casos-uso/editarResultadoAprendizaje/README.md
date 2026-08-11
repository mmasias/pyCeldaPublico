<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarResultadoAprendizaje/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Editar `codigo`, `tipo` y `descripcion` de un `ResultadoAprendizaje`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

A diferencia de `editarMetodologiaDocente()` (`codigo` fijo desde el alta, catálogo institucional con códigos MD1-MD7 de significado estable), aquí `codigo` y `tipo` son editables. Mismo formulario que `crearResultadoAprendizaje()`: la entidad es demasiado minimalista para que el patrón C→U aporte algo (ver corrección en la revisión del lote, [issue #24](https://github.com/mmasias/pyCelda/issues/24), y el README de `crearResultadoAprendizaje()`), así que ambos casos de uso piden los mismos tres campos -- la diferencia real es que aquí llegan precargados. RAK1 es dato real del plan de estudios de GII, aportado por el usuario en la [issue #23](https://github.com/mmasias/pyCelda/issues/23).

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `RESULTADO_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : editarResultadoAprendizaje()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `ResultadoAprendizaje`
- Modelo del dominio -- `ResultadoAprendizaje{codigo, tipo, descripcion}`, `tipo` enum cerrado de 4 valores (Conocimientos/Habilidades/Competencias/General)
- [crearResultadoAprendizaje()](/RUP/01-requisitos/03-detalle-casos-uso/crearResultadoAprendizaje/README.md) -- caso de uso que abre el patrón C→U que este cierra

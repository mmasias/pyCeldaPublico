<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
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
|**Actor**|`DirectorGrado`|
|**Objetivo**|Dar de alta un `ResultadoAprendizaje` en el catálogo de un `Grado`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Sin patrón C→U, a diferencia del resto de `crearX()` del catálogo**: el diseño original (caso de calibración, discussion #9) pedía solo `descripcion` y diferia `codigo`/`tipo` a `editarResultadoAprendizaje()`. Corregido en la revisión del lote L3 ([issue #24](https://github.com/mmasias/pyCelda/issues/24)): `ResultadoAprendizaje{codigo, tipo, descripcion}` es demasiado minimalista para que deferir dos de sus tres campos aporte algo -- los tres son igual de triviales de introducir en el momento de la creación, a diferencia de `Asignatura` (`crearAsignatura()` sí difiere `ects`/`contenido`/`estado`, 4 campos más allá de `nombre`). `crearResultadoAprendizaje()` y `editarResultadoAprendizaje()` terminan pidiendo el mismo formulario.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADO_APRENDIZAJE_ABIERTO : crearResultadoAprendizaje()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `ResultadoAprendizaje`
- Modelo del dominio -- `Grado *-d- ResultadoAprendizaje`, `ResultadoAprendizaje{codigo, tipo, descripcion}`
- [Issue #24](https://github.com/mmasias/pyCelda/issues/24) -- revisión del lote L3, origen de la corrección sobre C→U

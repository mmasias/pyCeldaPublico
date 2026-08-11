<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Asociar una `MetodologiaDocente` del catálogo institucional a una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Solo elige una `MetodologiaDocente` del catálogo -- sin `descripcionPropia` en este formulario, mismo criterio C→U que `crearX()`: el alta de la asociación es mínima, y `descripcionPropia` (vacía por defecto) se gestiona aparte en [`editarAsociacionMetodologiaDocenteMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/editarAsociacionMetodologiaDocenteMateria/README.md). El selector solo ofrece `MetodologiaDocente` todavía no asociadas a esta `Materia`. Cierre del hueco de diseño de L4 en la discussion [#27](https://github.com/mmasias/pyCelda/discussions/27): el catálogo tenía un único verbo `asociarX()`, se completó con el trío (`asociar`/`desasociar`/`editarAsociacion`) al confirmarse que `descripcionPropia` sí justifica una edición propia, a diferencia de la asociación con `ResultadoAprendizaje`.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarMetodologiaDocenteAMateria()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- Modelo del dominio -- `Materia o-- MetodologiaDocente` vía `MetodologiaMateria{descripcionPropia}`
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Asociar un `ResultadoAprendizaje` del catálogo del `Grado` a una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primer escalón de la cascada `Grado`->`Materia`->`AsignaturaGrado`. A diferencia de `asociarMetodologiaDocenteAMateria()`, aquí no hace falta un `editarAsociacionX()`: `Materia o-u- ResultadoAprendizaje` es agregación simple, sin clase de asociación ni atributo propio que editar -- el trío se queda en par (`asociar`/`desasociar`), cerrado así en la discussion [#27](https://github.com/mmasias/pyCelda/discussions/27). El selector solo ofrece `ResultadoAprendizaje` del `Grado` todavía no asociados a esta `Materia`. RAK2 es dato real (issue [#23](https://github.com/mmasias/pyCelda/issues/23)); qué `ResultadoAprendizaje` concretos usa "Programación" es ilustrativo.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIA_ABIERTO --> MATERIA_ABIERTO : asociarResultadoAprendizajeAMateria()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `Materia`
- Modelo del dominio -- `Materia o-u- ResultadoAprendizaje`, README: "el director asigna primero a cada `Materia` un subconjunto del catálogo de `ResultadoAprendizaje` del `Grado`"
- [Discussion #27](https://github.com/mmasias/pyCelda/discussions/27) -- cierre del hueco de verbos de asociación a nivel de `Materia`

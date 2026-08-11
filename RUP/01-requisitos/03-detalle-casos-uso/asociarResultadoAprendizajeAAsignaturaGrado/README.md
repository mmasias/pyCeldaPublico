<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorGrado`|
|**Objetivo**|Asociar un `ResultadoAprendizaje` (ya asignado a la `Materia`) a una `AsignaturaGrado` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Segundo escalón de la cascada en dos pasos documentada en el modelo del dominio: el director reparte primero un subconjunto del catálogo de `ResultadoAprendizaje` del `Grado` a cada `Materia` (`asociarResultadoAprendizajeAMateria()`), y después, de ese subconjunto ya asignado a la `Materia`, reparte a cada `AsignaturaGrado` concreta dentro de ella. El selector solo ofrece los `ResultadoAprendizaje` que cumplen las dos condiciones -- ya asignados a la `Materia` y no asignados aún a esta `AsignaturaGrado` -- por la regla de consistencia del modelo de dominio: los RA de una `AsignaturaGrado` deben ser subconjunto de los ya asignados a su `Materia`.

Sin `<<choice>>`: asignación libre, mismo patrón que `asociarResultadoAprendizajeAMateria()`/`asociarMetodologiaDocenteAMateria()`.

## Referencias

- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : asociarResultadoAprendizajeAAsignaturaGrado()`
- [actoresCasosUsoDirectorGrado.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorGrado.puml) -- catálogo de casos de uso de `DirectorGrado` sobre `AsignaturaGrado`
- Modelo del dominio -- `AsignaturaGrado o- ResultadoAprendizaje`; README, cascada `Grado`->`Materia`->`AsignaturaGrado` y regla de consistencia (subconjunto de la `Materia`)
- [`asociarResultadoAprendizajeAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/README.md) -- primer escalón de la misma cascada
- [`desasociarResultadoAprendizajeAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md) -- caso de uso complementario (baja de la asociación)

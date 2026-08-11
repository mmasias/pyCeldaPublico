<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearSistemaEvaluacion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta un `SistemaEvaluacion` en una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`tipo` es un selector de lista fija (`"Evaluación continua"` / `"Evaluación final"`, issue [#14](https://github.com/mmasias/pyCelda/issues/14)), no texto libre -- las 63 variantes de `sistema_evaluacion` en el seed correspondían a este atributo, no a `descripcion`. `descripcion` sí sigue siendo texto libre y opcional: es el detalle que el `Admin` añade dentro de la propia `Materia`, no el nombre del sistema. `ponderacionMinima`/`ponderacionMaxima` son los rangos oficiales verificados ante ANECA que después acotan cada `PonderacionEvaluacion` de la Guía.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMAS_EVALUACION_ABIERTO --> SISTEMA_EVALUACION_ABIERTO : crearSistemaEvaluacion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `SistemaEvaluacion`
- Modelo del dominio -- `SistemaEvaluacion{tipo, descripcion, ponderacionMinima, ponderacionMaxima}`; README, "`SistemaEvaluacion.tipo`" y "`SistemaEvaluacion` define rangos oficiales por `Materia`"
- Issue [#14](https://github.com/mmasias/pyCelda/issues/14) -- origen de la decisión de `tipo` como lista fija

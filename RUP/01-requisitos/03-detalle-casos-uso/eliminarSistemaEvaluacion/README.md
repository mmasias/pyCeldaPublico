<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (en uso)|Confirmación (sin uso)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/wireframe-confirmacion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Eliminar un `SistemaEvaluacion` de una `Materia`, siempre que ninguna `PonderacionEvaluacion` lo use|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Borrado físico bloqueado relacionalmente, mismo patrón que `eliminarFacultad()`/`eliminarMetodologiaDocente()`/`eliminarMateria()`: `SistemaEvaluacion` no tiene `estado` propio -- vive y muere con la `Materia` que lo contiene, así que su borrado es siempre físico. El bloqueo usa `PonderacionEvaluacion` (`PonderacionEvaluacion --> SistemaEvaluacion`), no `AsignaturaGrado` como `eliminarMateria()`: es la relación real que referencia a `SistemaEvaluacion`, desde la Guía. "Evaluación continua"/"Evaluación final" para bloqueada/confirmación son los dos valores reales de `tipo`; qué `PonderacionEvaluacion` concretas lo usan no está en el seed (`Guia`/`PonderacionEvaluacion` son L7/L8, todavía sin construir).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMAS_EVALUACION_ABIERTO --> SISTEMAS_EVALUACION_ABIERTO : eliminarSistemaEvaluacion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `SistemaEvaluacion`
- Modelo del dominio -- `PonderacionEvaluacion -> SistemaEvaluacion` (origen de la regla de bloqueo)

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirSistemasEvaluacion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirSistemasEvaluacion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirSistemasEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirSistemasEvaluacion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirSistemasEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirSistemasEvaluacion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `SistemaEvaluacion` de una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Composición real de `Materia` (`Materia *-- SistemaEvaluacion`), mismo patrón que `AsignaturaPrograma`: se navega desde dentro de una `Materia` concreta ya abierta, sin reutilización cruzada. "Evaluación continua"/"Evaluación final" son los dos valores reales de `tipo` (issue [#14](https://github.com/mmasias/pyCelda/issues/14)); descripción y rangos de ponderación son ilustrativos -- no hay datos reales de `SistemaEvaluacion` por `Materia` en el seed extraído.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIA_ABIERTO --> SISTEMAS_EVALUACION_ABIERTO : abrirSistemasEvaluacion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `SistemaEvaluacion`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia *-- SistemaEvaluacion`; README, entrada sobre `SistemaEvaluacion.tipo`

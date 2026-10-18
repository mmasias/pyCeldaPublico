<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/crearSistemaEvaluacion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/crearSistemaEvaluacion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/crearSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
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
|**Actor**|`Admin`, `DirectorPrograma` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))|
|**Objetivo**|Dar de alta un `SistemaEvaluacion` en una `Materia`|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

`tipo` es un selector de lista fija (`"Evaluación continua"` / `"Evaluación final"`, issue [#14](https://github.com/mmasias/pyCelda/issues/14)), no texto libre -- las 63 variantes de `sistema_evaluacion` en el seed correspondían a este atributo, no a `descripcion`. `descripcion` sigue siendo texto opcional, pero desde el issue [#772](https://github.com/mmasias/pyCelda/issues/772) es la denominación del sistema en la memoria, no un detalle libre (ver abajo). `ponderacionMinima`/`ponderacionMaxima` son los rangos oficiales verificados ante ANECA que después acotan cada `PonderacionEvaluacion` de la Guía.

**Actor `DirectorPrograma` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: el `DirectorPrograma` gana esta transición sobre las materias de sus programas, espejo de `Admin`. Mismo formulario y mismas reglas; es un self-loop de `MATERIA_ABIERTO` en [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml), que vuelve a la ficha de la materia.

**Guarda de rango (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: crear un sistema o cambiar su rango se rechaza (409) si alguna `Guia` del curso activo En revisión o Aprobada de la `Materia` dejaría de cumplir la regla de `Guia.bloqueo_ponderaciones()` para ese sistema -- suma de sus `PonderacionEvaluacion` vinculadas en [mínima, máxima]; un sistema nuevo cuenta como 0 %. Las guías en Borrador o Rechazada no cuentan: se revalidan en `enviarGuiaARevision()`. Sin esta guarda, estrechar un rango invalidaba en silencio guías ya validadas.

**`codigo` y `descripcion` de la memoria (issue [#772](https://github.com/mmasias/pyCelda/issues/772))**: `codigo` es el código del sistema en la memoria verificada (p. ej. `E1`), opcional y de hasta 20 caracteres; vacío se guarda como nulo. `descripcion` deja de ser un detalle libre de la `Materia` y pasa a ser la denominación literal de la memoria (p. ej. "Prueba Parcial"), porque ANECA exige que la Guía nombre la herramienta de evaluación tal como figura en ella. `tipo` se mantiene como clasificación. No hay catálogo de sistemas de evaluación por `Programa`: la importación desde el RUCT carga en cada `Materia` los sistemas de su memoria.


## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMAS_EVALUACION_ABIERTO --> SISTEMA_EVALUACION_ABIERTO : crearSistemaEvaluacion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `SistemaEvaluacion`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `SistemaEvaluacion{codigo, tipo, descripcion, ponderacionMinima, ponderacionMaxima}`; README, "`SistemaEvaluacion.codigo` y el significado de `descripcion`"; README, "`SistemaEvaluacion.tipo`" y "`SistemaEvaluacion` define rangos oficiales por `Materia`"
- Issue [#14](https://github.com/mmasias/pyCelda/issues/14) -- origen de la decisión de `tipo` como lista fija

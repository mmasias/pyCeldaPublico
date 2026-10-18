<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/editarSistemaEvaluacion/README.md) / [Diseño](/RUP/03-diseño/casos-uso/editarSistemaEvaluacion/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarSistemaEvaluacion()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/editarSistemaEvaluacion/README.md)|[Diseño](/RUP/03-diseño/casos-uso/editarSistemaEvaluacion/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarSistemaEvaluacion/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))|
|**Objetivo**|Editar `codigo`, `tipo`, `descripcion`, `ponderacionMinima` y `ponderacionMaxima` de un `SistemaEvaluacion` existente|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Mismos campos editables que `crearSistemaEvaluacion()`, sin campo fijo desde el alta (a diferencia de `editarMetodologiaDocente()`, donde `codigo` no se toca). **Actualización (issue [#772](https://github.com/mmasias/pyCelda/issues/772))**: el formulario gana `codigo`, el de la memoria (p. ej. `E1`), opcional y editable -- no es identificador interno, puede faltar hasta que la importación del RUCT lo cargue, y por eso no se fija desde el alta. `descripcion` pasa a ser la denominación literal de la memoria (ver [`crearSistemaEvaluacion()`](../crearSistemaEvaluacion/README.md)).

**Actor `DirectorPrograma` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: el `DirectorPrograma` gana esta transición sobre las materias de sus programas, espejo de `Admin`. Mismo formulario y mismas reglas; es un self-loop de `MATERIA_ABIERTO` en [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml), que vuelve a la ficha de la materia.

**Guarda de rango (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: crear un sistema o cambiar su rango se rechaza (409) si alguna `Guia` del curso activo En revisión o Aprobada de la `Materia` dejaría de cumplir la regla de `Guia.bloqueo_ponderaciones()` para ese sistema -- suma de sus `PonderacionEvaluacion` vinculadas en [mínima, máxima]; un sistema nuevo cuenta como 0 %. Las guías en Borrador o Rechazada no cuentan: se revalidan en `enviarGuiaARevision()`. Sin esta guarda, estrechar un rango invalidaba en silencio guías ya validadas.


## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_EVALUACION_ABIERTO --> SISTEMA_EVALUACION_ABIERTO : editarSistemaEvaluacion()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `SistemaEvaluacion`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `SistemaEvaluacion{codigo, tipo, descripcion, ponderacionMinima, ponderacionMaxima}`

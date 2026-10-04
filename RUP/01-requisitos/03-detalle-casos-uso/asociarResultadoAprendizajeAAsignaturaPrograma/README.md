<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md) / [Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|[Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaPrograma/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`DirectorPrograma`, `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))|
|**Objetivo**|Asociar un `ResultadoAprendizaje` (ya asignado a la `Materia`) a una `AsignaturaPrograma` concreta|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Segundo escalón de la cascada en dos pasos documentada en el [modelo del dominio](/RUP/00-modelo-del-dominio/README.md): el director reparte primero un subconjunto del catálogo de `ResultadoAprendizaje` del `Programa` a cada `Materia` (`asociarResultadoAprendizajeAMateria()`), y después, de ese subconjunto ya asignado a la `Materia`, reparte a cada `AsignaturaPrograma` concreta dentro de ella. El selector solo ofrece los `ResultadoAprendizaje` que cumplen las dos condiciones -- ya asignados a la `Materia` y no asignados aún a esta `AsignaturaPrograma` -- por la regla de consistencia del modelo de dominio: los RA de una `AsignaturaPrograma` deben ser subconjunto de los ya asignados a su `Materia`.

Sin `<<choice>>`: asignación libre, mismo patrón que `asociarResultadoAprendizajeAMateria()`/`asociarMetodologiaDocenteAMateria()`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: `Admin` gana esta transición como vía de corrección excepcional, con paridad completa respecto a `DirectorPrograma` -- no sustituye su flujo normal, lo complementa. Misma ficha, mismo wireframe y mismas reglas; es un self-loop de `ASIGNATURA_PROGRAMA_ABIERTO` también en [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml). Sin alcance por programa: `Admin` actúa sobre cualquier `AsignaturaPrograma`.

## Referencias

- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asociarResultadoAprendizajeAAsignaturaPrograma()`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- catálogo de casos de uso de `DirectorPrograma` sobre `AsignaturaPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o- ResultadoAprendizaje`; README, cascada `Programa`->`Materia`->`AsignaturaPrograma` y regla de consistencia (subconjunto de la `Materia`)
- [`asociarResultadoAprendizajeAMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAMateria/README.md) -- primer escalón de la misma cascada
- [`desasociarResultadoAprendizajeAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md) -- caso de uso complementario (baja de la asociación)

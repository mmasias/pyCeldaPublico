<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/casos-uso/abrirMaterias/README.md) / [Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirMaterias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|[Análisis](/RUP/02-analisis/casos-uso/abrirMaterias/README.md)|[Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`, `DirectorPrograma`|
|**Objetivo**|Consultar el listado de `Materia` de un `Programa`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Caso de uso reutilizado por `DirectorPrograma` (`DirectorPrograma --|> Profesor`), misma ficha -- ver [diagramaContextoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml). El CRUD de `Materia` es de `Admin`; `DirectorPrograma` solo navega este listado para llegar a sus casos de asociación (`asociarMetodologiaDocenteAMateria()`, `asociarResultadoAprendizajeAMateria()`, L4, sin empezar).

**Retocado el wireframe al cerrar la tanda #486/#487/#488/#492 (issue [#496](https://github.com/mmasias/pyCelda/issues/496)), sin tocar la especificación**: el listado gana la columna "Asignaturas" -- contador derivado del número de `AsignaturaPrograma` de cada `Materia`, issue [#487](https://github.com/mmasias/pyCelda/issues/487).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> MATERIAS_ABIERTO : abrirMaterias()`
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> MATERIAS_ABIERTO : abrirMaterias()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `Materia`
- [actoresCasosUsoDirectorPrograma.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoDirectorPrograma.puml) -- reutilización del caso de uso por `DirectorPrograma`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa *-- Materia`: composición real, se navega desde dentro del Programa abierto, no es catálogo institucional plano
- [Issue #487](https://github.com/mmasias/pyCelda/issues/487) -- origen de la columna "Asignaturas"

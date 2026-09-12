<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > crearAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Formulario|Error (código ya existente)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/wireframe.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/wireframe-error.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Dar de alta una `Asignatura` en el catálogo institucional|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Retocado (issue #181, 2026-09-05)**: `codigo` pasa de no pedirse en la creación a obligatorio, único y fijo desde el alta -- mismo criterio que `Grado.codigo` tras el issue #148 (`editarAsignatura()` sigue sin incluirlo, ver [Análisis](/RUP/02-analisis/casos-uso/editarAsignatura/README.md)). Se añade una rama de rechazo: si el `codigo` introducido ya existe en el catálogo, `crearAsignatura()` no crea la `Asignatura` y presenta un mensaje de error, mismo patrón `<<choice>>` que [`crearGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/crearGrado/README.md).

**Motivo**: `Asignatura.codigo` es el identificador real del catálogo institucional (IYA025, CSJ038, etc.) que hasta ahora vivía solo en los JSON del seed, sin llegar nunca a la base de datos ni a este formulario (issue #181 -- `AsignaturaGrado` no estaba enlazada a `Asignatura` pese a estar especificado en el modelo de dominio). Al enlazarla de verdad (`AsignaturaGrado.asignatura_id`, ver [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md)), `codigo` deja de ser opcional: sin él, dos `Asignatura` que representen la misma materia real en catálogos distintos (o una creada dos veces por error) no serían distinguibles.

**Divergencia histórica cerrada**: la nota de [`crearGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/crearGrado/README.md) ("`Asignatura`/`MetodologiaDocente` también lo tienen, pero sus `crearX()` no lo piden -- divergencia histórica de L0/L1, sin corregir retroactivamente") queda desactualizada para `Asignatura` por este cambio -- `MetodologiaDocente` sigue la divergencia (fuera de alcance de #181, sin encargo).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURAS_ABIERTO --> ASIGNATURA_ABIERTO : crearAsignatura()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Asignatura`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (codigo, nombre, ects, contenido, estado); `estado` nace `Vigente` por defecto, sin pedirlo -- patrón C→U, igual que `crearResultadoAprendizaje()`
- [`crearGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/crearGrado/README.md) -- precedente del patrón `<<choice>>` con rama de rechazo por código duplicado (issue #148), reutilizado aquí.
- [`editarPonderacionEvaluacion()`](/RUP/01-requisitos/03-detalle-casos-uso/editarPonderacionEvaluacion/especificacion.puml) -- precedente original del patrón `<<choice>>` con rango superado.

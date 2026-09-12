<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [**Detalle**](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Editar nombre, ECTS y contenido de una `Asignatura` del catálogo institucional (el `codigo` es fijo desde el alta)|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

**Retocado (issue #181, 2026-09-05)**: `codigo` (obligatorio y único desde `crearAsignatura()`, ver [Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md)) se muestra pero no se ofrece como campo editable -- mismo criterio que `editarGrado()`/`editarMetodologiaDocente()`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_ABIERTO --> ASIGNATURA_ABIERTO : editarAsignatura()`
- [actoresCasosUsoAdminCatalogos.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminCatalogos.puml) -- catálogo de casos de uso de `Admin` sobre `Asignatura`
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (codigo, nombre, ects, contenido, estado); `estado` queda fuera de este formulario -- se gestiona en exclusiva desde `eliminarAsignatura()` (Vigente/Extinguido), mismo criterio que `CursoAcademico.estado` con `activarCursoAcademico()`
- [`crearAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md) -- origen de `codigo`, obligatorio y único desde el alta (issue #181).
- [`editarGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/editarGrado/README.md) -- mismo criterio de `codigo` fijo, mostrado solo lectura.

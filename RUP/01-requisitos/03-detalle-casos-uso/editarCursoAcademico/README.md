<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > editarCursoAcademico()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (tiene Guías)|Edición (sin Guías)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/editarCursoAcademico/wireframe-edicion.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Corregir `inicio`/`fin` de un `CursoAcademico`, siempre que no tenga ninguna `Guia` asociada|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Primera vez que el patrón `<<choice>>` bloqueante (hasta ahora exclusivo de `eliminarX()`) se aplica a **editar**: cerrado en la [discussion #15](https://github.com/mmasias/pyCelda/discussions/15) junto con el resto de `CursoAcademico`. No existe `eliminarCursoAcademico()` en el catálogo -- corregir un error de fecha es editar, no borrar y recrear. `2026-2027` (Activo, con `Guia` clonadas) ilustra el bloqueo; `2027-2028` (recién creado, nunca activado, sin `Guia`) ilustra la edición libre -- mismos dos cursos usados en [`abrirCursosAcademicos()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md).

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSO_ACADEMICO_ABIERTO --> CURSO_ACADEMICO_ABIERTO : editarCursoAcademico()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `CursoAcademico`
- Modelo del dominio -- `CursoAcademico.estado`: "corregir un dato mal introducido al crear (inicio/fin) es editarCursoAcademico(), bloqueado si el curso tiene alguna Guia asociada -- mismo criterio relacional que bloquea eliminarProfesor()/eliminarFacultad(), aplicado aquí a editar en vez de a borrar"

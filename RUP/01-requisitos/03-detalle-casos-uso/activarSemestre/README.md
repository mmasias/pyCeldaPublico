<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > activarSemestre()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/activarSemestre/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Fijar cuál de los dos semestres del `CursoAcademico` Activo está vivo|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Edición simple de un atributo (`semestreActivo`), sin `<<choice>>` ni confirmación -- mismo molde que `editarUniversidad()`, no el de `activarCursoAcademico()`: aquí no hay ninguna precondición que bloquee, solo sustituir el valor. Sin evento simétrico de "desactivar semestre": el nuevo valor ya sustituye al anterior en la misma fila. Nunca inferido de la fecha de hoy -- evento explícito del admin, mismo criterio que `CursoAcademico.estado`.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSO_ACADEMICO_ABIERTO --> CURSO_ACADEMICO_ABIERTO : activarSemestre()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `CursoAcademico`
- Modelo del dominio -- `CursoAcademico.semestreActivo`: "las notificaciones dirigidas al profesor se filtran por Guia.semestre == CursoAcademico.semestreActivo -- no es una relación estructural, es una condición de filtrado en el envío"

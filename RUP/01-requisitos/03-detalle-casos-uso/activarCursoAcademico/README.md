<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > activarCursoAcademico()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|Bloqueada (no elegible)|Activado (efecto colateral)|
|:-:|:-:|
|![](/images/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/wireframe-bloqueada.svg)|![](/images/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/wireframe-activado.svg)|
||<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Activar un `CursoAcademico`, desactivando automáticamente el que estaba Activo|
|**Tipo**|Primario, esencial|
|**Nivel**|Objetivo de usuario|

</div>

Acción de conjunto sobre el listado (self-loop en `CURSOS_ACADEMICOS_ABIERTO`), no sobre un curso ya abierto -- no requiere el paso previo de `abrirCursoAcademico()`, mismo molde que `eliminarFacultad()`. Sin pantalla de confirmación intermedia: la elegibilidad ya la resuelve el `<<choice>>` (cerrado en la [discussion #15](https://github.com/mmasias/pyCelda/discussions/15)), no hay una segunda pregunta que hacer después. En cualquier momento hay como mucho dos candidatos activables -- el último creado (siempre permitido) o el penúltimo (solo si el último no tiene actividad registrada, entendida como alguna fila en `HistorialCambio` asociada a sus `Guia`); cualquier candidato anterior al penúltimo queda bloqueado siempre.

El botón `[Activar]` en el listado ya refleja esto (ver [`abrirCursosAcademicos()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md)): no aparece en cursos anteriores al penúltimo, siempre bloqueados, así que el `<<choice>>` de este caso de uso solo se dispara desde dos puntos de entrada reales. El wireframe de "activado" ilustra el caso simple (activar el último, `2027-2028`, desactiva automáticamente `2026-2027`, que pasa a ser el nuevo penúltimo Inactivo). El wireframe de "bloqueada" ilustra el otro punto de entrada real -- reactivar `2026-2027` (el penúltimo) después de que `2027-2028` (el último) ya acumuló actividad registrada -- en vez de un intento sobre un curso anterior al penúltimo, que ya no tiene botón que pulsar. No existe `desactivarCursoAcademico()` suelto: activar siempre implica desactivar el otro.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `CURSOS_ACADEMICOS_ABIERTO --> CURSOS_ACADEMICOS_ABIERTO : activarCursoAcademico()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `CursoAcademico`
- Modelo del dominio -- `CursoAcademico.estado`: regla de elegibilidad de activación completa, `<<choice>>` al inicio del caso de uso

<div align=right>

<sub>[Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / **Detalle** / [Mockups navegables](/docs/PROPUESTA_WIREFRAME/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- no incluye modelo de dominio, análisis/diseño ni dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirCursosAcademicos()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|**Detalle**|Análisis|Diseño|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/especificacion.svg)|
|-|
|<div align=right><sup>Código fuente: [especificacion.puml](especificacion.puml)</sup></div>|

</div>

<div align=center>

|![](/images/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/wireframe.svg)|
|-|
|<div align=right><sup>Código fuente: [wireframes.puml](wireframes.puml)</sup></div>|

</div>

## Información del caso de uso

<div align=center>

|Atributo|Valor|
|-|-|
|**Actor**|`Admin`|
|**Objetivo**|Consultar el listado de `CursoAcademico` de la `Universidad`|
|**Tipo**|Primario, esencial|
|**Nivel**|Subfunción|

</div>

Cuatro filas ilustran de un vistazo el resto del lote: `2026-2027` es el `CursoAcademico` canónico (Activo, semestre 1, ver [discussion #8](https://github.com/mmasias/pyCelda/discussions/8)); `2024-2025`/`2025-2026` son cursos anteriores ya desactivados (con `Guia` clonadas en su momento, de ahí que `editarCursoAcademico()` los bloquee); `2027-2028` está recién creado y nunca activado, sin `Guia` asociadas -- es el que ilustra edición libre en `editarCursoAcademico()` y el candidato "último" en `activarCursoAcademico()`.

El botón `[Activar]` **no** aparece en toda fila Inactiva por igual: `2024-2025`/`2025-2026` son anteriores al penúltimo, bloqueados siempre sin excepción, así que el listado ya no les ofrece el botón -- mostrarlo sería un clic desperdiciado, mismo criterio de "validar antes de presentar" que ya aplica `eliminarFacultad()`. Solo lo llevan el último creado (`2027-2028`, siempre elegible mientras esté Inactivo) y, cuando corresponda, el penúltimo -- ver [`activarCursoAcademico()`](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/README.md) para el caso en que el penúltimo sí está Inactivo y su elegibilidad depende de si el último tiene actividad registrada, algo que el `<<choice>>` resuelve al solicitarlo porque cambia en tiempo real.

## Referencias

- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> CURSOS_ACADEMICOS_ABIERTO : abrirCursosAcademicos()`
- [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml) -- catálogo de casos de uso de `Admin` sobre `CursoAcademico`
- Modelo del dominio -- `Universidad -- CursoAcademico`; regla de `estado`/elegibilidad de activación documentada en el README de esa fase

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocentePrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocentePrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarMetodologiaDocentePrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/README.md): `<<choice>>` bloqueante -- rompe el vínculo `Programa o-- MetodologiaDocente` siempre que ninguna `Materia` del `Programa` la tenga asociada. Es el primer nivel de la cadena `Programa` -> `Materia` -> `AsignaturaPrograma`: el bloqueo se apoya en el nivel inmediatamente inferior ([`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md) hace lo propio respecto de `AsignaturaPrograma`).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarMetodologiaDocentePrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarMetodologiaDocenteProgramaView`

**Responsabilidades:**
- en la rama verde, presenta la asociación y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo con las `Materia` concretas en uso.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita desasociar una `MetodologiaDocente` desde la pantalla de las metodologías docentes de su `Programa` ([`abrirMetodologiasDocentesPrograma()`](../abrirMetodologiasDocentesPrograma/README.md)).
- **Control:** `ProgramaController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO` en los tres casos -- self-loop, con "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ProgramaController`

**Responsabilidades:**
- aplica el `<<choice>>`: recupera las `Materia` del `Programa` que usan la `MetodologiaDocente` (`materiasConMetodologiaDocente(programaId, metodologiaDocenteId)`) -- lista vacía = no bloqueada.
- si no está bloqueada y el `DirectorPrograma` confirma, elimina real e inmediata la asociación (`desasociarMetodologiaDocente(programaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarMetodologiaDocenteProgramaView`.
- **Salida:** `Programa`, `ProgramaRepository`.

## Clases de modelo

### `Programa`

**Responsabilidades:**
- lista los nombres de sus `Materia` que usan una `MetodologiaDocente` dada (`materiasConMetodologiaDocente(metodologiaDocenteId)`) -- origen de la regla de bloqueo.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.

### `ProgramaRepository`

**Responsabilidades:**
- elimina real e inmediata la asociación (`desasociarMetodologiaDocente(programaId, metodologiaDocenteId)`) -- no es un borrado de `MetodologiaDocente`, que sigue en el catálogo institucional.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

**Actor `Admin`**: mismo caso de uso compartido (issues [#636](https://github.com/mmasias/pyCelda/issues/636)/[#640](https://github.com/mmasias/pyCelda/issues/640)); en el diagrama de contexto de `Admin` el estado es `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO` (distinto del catálogo institucional `METODOLOGIAS_DOCENTES_ABIERTO`). La colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante (variantes bloqueada/confirmación).
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : desasociarMetodologiaDocentePrograma()`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : desasociarMetodologiaDocentePrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o-- MetodologiaDocente`, `Materia` con `MetodologiaMateria` (origen de la regla de bloqueo).
- [`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md) -- plantilla estructural: mismo `<<choice>>` bloqueante un nivel más abajo.
- [`asociarMetodologiaDocenteAPrograma()`](../asociarMetodologiaDocenteAPrograma/README.md) -- caso de uso complementario (alta de la asociación).

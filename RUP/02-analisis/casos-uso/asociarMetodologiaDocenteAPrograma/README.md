<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarMetodologiaDocenteAPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/README.md): sin `<<choice>>` -- primer nivel de la cadena `MetodologiaDocente` (`Programa` -> `Materia` -> `AsignaturaPrograma`). Asocia una `MetodologiaDocente` del catálogo institucional a un `Programa`, sin clase de asociación (agregación simple, `Programa o-- MetodologiaDocente`). El conjunto asociado al `Programa` es el universo del que luego eligen sus `Materia` ([`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md)).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarMetodologiaDocenteAProgramaView`

**Responsabilidades:**
- presenta la selección de `MetodologiaDocente` del catálogo aún no asociadas al `Programa`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita asociar una `MetodologiaDocente` desde la pantalla de las metodologías docentes de su `Programa` ([`abrirMetodologiasDocentesPrograma()`](../abrirMetodologiasDocentesPrograma/README.md)).
- **Control:** `ProgramaController`.
- **Salida:** `:METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO`.

## Clases de controlador

### `ProgramaController`

**Responsabilidades:**
- lista las `MetodologiaDocente` aún no asociadas al `Programa` (`cargarMetodologiasDocentesDisponibles(programaId)`).
- asocia real e inmediato (`asociarMetodologiaDocente(programaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `AsociarMetodologiaDocenteAProgramaView`.
- **Salida:** `MetodologiaDocenteRepository`, `ProgramaRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- el elemento del catálogo institucional que se elige.

**Colaboraciones:**
- **Entrada:** listada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- lista las `MetodologiaDocente` del catálogo aún no asociadas al `Programa` (`listarDisponiblesParaPrograma(programaId)`).

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `MetodologiaDocente`.

### `Programa`

**Responsabilidades:**
- gana una `MetodologiaDocente` en su colección asociada.

**Colaboraciones:**
- **Entrada:** `ProgramaController`, vía `ProgramaRepository`.
- **Salida:** agrega `MetodologiaDocente` asociadas.

### `ProgramaRepository`

**Responsabilidades:**
- persiste la nueva asociación (`asociarMetodologiaDocente(programaId, metodologiaDocenteId)`) -- agregación simple, sin clase de asociación que crear.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

**Actor `Admin`**: mismo caso de uso compartido (issues [#636](https://github.com/mmasias/pyCelda/issues/636)/[#640](https://github.com/mmasias/pyCelda/issues/640)); en el diagrama de contexto de `Admin` el estado es `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO` (distinto del catálogo institucional `METODOLOGIAS_DOCENTES_ABIERTO`). La colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAPrograma/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : asociarMetodologiaDocenteAPrograma()`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO --> METODOLOGIAS_DOCENTES_PROGRAMA_ABIERTO : asociarMetodologiaDocenteAPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o-- MetodologiaDocente`.
- [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md) -- siguiente nivel de la cadena, que elige del subconjunto asociado al `Programa`.
- [`asociarMetodologiaDocenteAAsignaturaPrograma()`](../asociarMetodologiaDocenteAAsignaturaPrograma/README.md) -- plantilla estructural (misma relación, otro padre).
- [`desasociarMetodologiaDocentePrograma()`](../desasociarMetodologiaDocentePrograma/README.md) -- caso de uso complementario (baja de la asociación).

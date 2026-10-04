<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarMetodologiaDocenteAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/README.md): **sin `<<choice>>` bloqueante**, a diferencia de [`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md) -- `AsignaturaPrograma` es el último escalón de la cascada, sin nivel inferior que dependa del reparto. Confirmación con advertencia condicional si la `MetodologiaDocente` que se desasocia es la única de esa `AsignaturaPrograma`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarMetodologiaDocenteAsignaturaProgramaView`

**Responsabilidades:**
- presenta la asociación y, si es la única `MetodologiaDocente` de la `AsignaturaPrograma`, la advertencia de que quedaría sin ninguna.
- pide confirmar/cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita desasociar una `MetodologiaDocente`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO` en ambos casos -- "confirmada, lista actualizada" (verde) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- pregunta si la `AsignaturaPrograma` quedaría sin ninguna `MetodologiaDocente` tras la desasociación (`quedaSinMetodologiasDocentesTrasDesasociar(asignaturaProgramaId, metodologiaDocenteId)`), para que la Vista decida si muestra la advertencia -- no bloquea, solo informa.
- si el `DirectorPrograma` confirma, desasocia real e inmediata (`desasociarMetodologiaDocente(asignaturaProgramaId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarMetodologiaDocenteAsignaturaProgramaView`.
- **Salida:** `AsignaturaProgramaRepository`.

## Clases de modelo

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- responde si quedaría sin `MetodologiaDocente` tras desasociar una dada (`quedaSinMetodologiasDocentesTrasDesasociar(asignaturaProgramaId, metodologiaDocenteId)`).
- elimina real e inmediata la asociación (`desasociarMetodologiaDocente(asignaturaProgramaId, metodologiaDocenteId)`) -- no es un borrado de `MetodologiaDocente`, que sigue en el catálogo institucional y en la `Materia` si lo estaba.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaPrograma/wireframes.puml) -- fuente de verdad de las dos variantes (normal/advertencia).
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasociarMetodologiaDocenteAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o-r- MetodologiaDocente`.
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional).
- [`asociarMetodologiaDocenteAAsignaturaPrograma()`](../asociarMetodologiaDocenteAAsignaturaPrograma/README.md) -- caso de uso complementario (alta de la asociación).

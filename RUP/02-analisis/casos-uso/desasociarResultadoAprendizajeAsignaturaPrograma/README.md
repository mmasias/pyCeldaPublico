<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarResultadoAprendizajeAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/README.md): **sin `<<choice>>` bloqueante**, a diferencia de [`desasociarResultadoAprendizajeAMateria()`](../desasociarResultadoAprendizajeAMateria/README.md) -- `AsignaturaPrograma` es el último escalón de la cascada. Confirmación con advertencia condicional si el `ResultadoAprendizaje` que se desasocia es el único de esa `AsignaturaPrograma`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarResultadoAprendizajeAsignaturaProgramaView`

**Responsabilidades:**
- presenta la asociación y, si es el único `ResultadoAprendizaje` de la `AsignaturaPrograma`, la advertencia de que quedaría sin ninguno.
- pide confirmar/cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita desasociar un `ResultadoAprendizaje`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO` en ambos casos.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- pregunta si la `AsignaturaPrograma` quedaría sin ningún `ResultadoAprendizaje` tras la desasociación (`quedaSinResultadosAprendizajeTrasDesasociar(asignaturaProgramaId, resultadoAprendizajeId)`) -- no bloquea, solo informa.
- si el `DirectorPrograma` confirma, desasocia real e inmediata (`desasociarResultadoAprendizaje(asignaturaProgramaId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarResultadoAprendizajeAsignaturaProgramaView`.
- **Salida:** `AsignaturaProgramaRepository`.

## Clases de modelo

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- responde si quedaría sin `ResultadoAprendizaje` tras desasociar uno dado (`quedaSinResultadosAprendizajeTrasDesasociar(asignaturaProgramaId, resultadoAprendizajeId)`).
- elimina real e inmediata la asociación (`desasociarResultadoAprendizaje(asignaturaProgramaId, resultadoAprendizajeId)`) -- no es un borrado del `ResultadoAprendizaje`, que sigue en el catálogo del `Programa` y en la `Materia` si lo estaba.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: la colaboración es la misma con `Admin` como iniciador; la única diferencia es que no se comprueba que el `Programa` sea del actor (`Admin` no tiene programa propio).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaPrograma/wireframes.puml) -- fuente de verdad de las dos variantes (normal/advertencia).
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasociarResultadoAprendizajeAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma o- ResultadoAprendizaje`.
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional) y retiro de `editarAsociacionResultadoAprendizajeAsignaturaPrograma()` del catálogo.
- [`asociarResultadoAprendizajeAAsignaturaPrograma()`](../asociarResultadoAprendizajeAAsignaturaPrograma/README.md) -- caso de uso complementario (alta de la asociación).

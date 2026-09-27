<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > desasociarResultadoAprendizajeAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarResultadoAprendizajeAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/README.md): **sin `<<choice>>` bloqueante**, a diferencia de [`desasociarResultadoAprendizajeAMateria()`](../desasociarResultadoAprendizajeAMateria/README.md) -- `AsignaturaGrado` es el último escalón de la cascada. Confirmación con advertencia condicional si el `ResultadoAprendizaje` que se desasocia es el único de esa `AsignaturaGrado`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarResultadoAprendizajeAsignaturaGradoView`

**Responsabilidades:**
- presenta la asociación y, si es el único `ResultadoAprendizaje` de la `AsignaturaGrado`, la advertencia de que quedaría sin ninguno.
- pide confirmar/cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `DirectorGrado` solicita desasociar un `ResultadoAprendizaje`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO` en ambos casos.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- pregunta si la `AsignaturaGrado` quedaría sin ningún `ResultadoAprendizaje` tras la desasociación (`quedaSinResultadosAprendizajeTrasDesasociar(asignaturaGradoId, resultadoAprendizajeId)`) -- no bloquea, solo informa.
- si el `DirectorGrado` confirma, desasocia real e inmediata (`desasociarResultadoAprendizaje(asignaturaGradoId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarResultadoAprendizajeAsignaturaGradoView`.
- **Salida:** `AsignaturaGradoRepository`.

## Clases de modelo

### `AsignaturaGradoRepository`

**Responsabilidades:**
- responde si quedaría sin `ResultadoAprendizaje` tras desasociar uno dado (`quedaSinResultadosAprendizajeTrasDesasociar(asignaturaGradoId, resultadoAprendizajeId)`).
- elimina real e inmediata la asociación (`desasociarResultadoAprendizaje(asignaturaGradoId, resultadoAprendizajeId)`) -- no es un borrado del `ResultadoAprendizaje`, que sigue en el catálogo del `Grado` y en la `Materia` si lo estaba.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarResultadoAprendizajeAsignaturaGrado/wireframes.puml) -- fuente de verdad de las dos variantes (normal/advertencia).
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasociarResultadoAprendizajeAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado o- ResultadoAprendizaje`.
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional) y retiro de `editarAsociacionResultadoAprendizajeAsignaturaGrado()` del catálogo.
- [`asociarResultadoAprendizajeAAsignaturaGrado()`](../asociarResultadoAprendizajeAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asociación).

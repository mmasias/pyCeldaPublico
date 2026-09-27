<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > asociarResultadoAprendizajeAAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarResultadoAprendizajeAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/README.md): sin `<<choice>>` -- segundo escalón de la cascada `ResultadoAprendizaje`. Asocia un `ResultadoAprendizaje` ya asignado a la `Materia` a una `AsignaturaGrado` concreta de esa `Materia`, mismo patrón que [`asociarMetodologiaDocenteAAsignaturaGrado()`](../asociarMetodologiaDocenteAAsignaturaGrado/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarResultadoAprendizajeAAsignaturaGradoView`

**Responsabilidades:**
- presenta la selección de `ResultadoAprendizaje` ya asignados a la `Materia` y no asignados aún a esta `AsignaturaGrado`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `DirectorGrado` solicita asociar un `ResultadoAprendizaje`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` que cumplen las dos condiciones -- ya asignados a la `Materia`, no asignados aún a esta `AsignaturaGrado` (`cargarResultadosAprendizajeDisponibles(asignaturaGradoId)`).
- asocia real e inmediato (`asociarResultadoAprendizaje(asignaturaGradoId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `AsociarResultadoAprendizajeAAsignaturaGradoView`.
- **Salida:** `ResultadoAprendizajeRepository`, `AsignaturaGradoRepository`.

## Clases de modelo

### `ResultadoAprendizaje`

**Responsabilidades:**
- porta `codigo`, `tipo` -- el subconjunto ya asignado a la `Materia`, del que se elige.

**Colaboraciones:**
- **Entrada:** listado por `ResultadoAprendizajeRepository`.

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- lista los `ResultadoAprendizaje` ya asignados a la `Materia` y no aún a esta `AsignaturaGrado` (`listarDisponiblesParaAsignaturaGrado(asignaturaGradoId)`) -- aplica la regla de consistencia del modelo de dominio.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

### `AsignaturaGrado`

**Responsabilidades:**
- gana un `ResultadoAprendizaje` en su colección asociada.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `AsignaturaGradoRepository`.
- **Salida:** compone `ResultadoAprendizaje` asociados.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- persiste la nueva asociación (`asociarResultadoAprendizaje(asignaturaGradoId, resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarResultadoAprendizajeAAsignaturaGrado/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : asociarResultadoAprendizajeAAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado o- ResultadoAprendizaje`; regla de consistencia, subconjunto de la `Materia`.
- [`asociarResultadoAprendizajeAMateria()`](../asociarResultadoAprendizajeAMateria/README.md) -- primer escalón de la misma cascada.
- [`desasociarResultadoAprendizajeAsignaturaGrado()`](../desasociarResultadoAprendizajeAsignaturaGrado/README.md) -- caso de uso complementario (baja de la asociación).

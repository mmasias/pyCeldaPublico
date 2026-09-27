<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > asociarMetodologiaDocenteAAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asociarMetodologiaDocenteAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/README.md): sin `<<choice>>` -- segundo escalón de la cascada `MetodologiaDocente` en dos pasos. Asocia una `MetodologiaDocente` ya asociada a la `Materia` a una `AsignaturaGrado` concreta de esa `Materia`, sin clase de asociación (agregación simple).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsociarMetodologiaDocenteAAsignaturaGradoView`

**Responsabilidades:**
- presenta la selección de `MetodologiaDocente` ya asociadas a la `Materia` y no asociadas aún a esta `AsignaturaGrado`.
- ofrece la navegación a solicitar la asociación.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `DirectorGrado` solicita asociar una `MetodologiaDocente`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- lista las `MetodologiaDocente` que cumplen las dos condiciones -- ya asociadas a la `Materia`, no asociadas aún a esta `AsignaturaGrado` (`cargarMetodologiasDocentesDisponibles(asignaturaGradoId)`).
- asocia real e inmediato (`asociarMetodologiaDocente(asignaturaGradoId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `AsociarMetodologiaDocenteAAsignaturaGradoView`.
- **Salida:** `MetodologiaDocenteRepository`, `AsignaturaGradoRepository`.

## Clases de modelo

### `MetodologiaDocente`

**Responsabilidades:**
- porta `codigo`, `descripcion` -- el subconjunto ya asociado a la `Materia`, del que se elige.

**Colaboraciones:**
- **Entrada:** listada por `MetodologiaDocenteRepository`.

### `MetodologiaDocenteRepository`

**Responsabilidades:**
- lista las `MetodologiaDocente` ya asociadas a la `Materia` y no aún a esta `AsignaturaGrado` (`listarDisponiblesParaAsignaturaGrado(asignaturaGradoId)`) -- aplica la regla de consistencia del modelo de dominio.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `MetodologiaDocente`.

### `AsignaturaGrado`

**Responsabilidades:**
- gana una `MetodologiaDocente` en su colección asociada.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `AsignaturaGradoRepository`.
- **Salida:** compone `MetodologiaDocente` asociadas.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- persiste la nueva asociación (`asociarMetodologiaDocente(asignaturaGradoId, metodologiaDocenteId)`) -- agregación simple, sin clase de asociación que crear (a diferencia de `MetodologiaMateria`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/asociarMetodologiaDocenteAAsignaturaGrado/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : asociarMetodologiaDocenteAAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado o-r- MetodologiaDocente`; regla de consistencia, subconjunto de la `Materia`.
- [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md) -- primer escalón de la misma cascada.
- [`desasociarMetodologiaDocenteAsignaturaGrado()`](../desasociarMetodologiaDocenteAsignaturaGrado/README.md) -- caso de uso complementario (baja de la asociación).

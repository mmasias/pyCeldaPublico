<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasociarMetodologiaDocenteAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md): **sin `<<choice>>` bloqueante**, a diferencia de [`desasociarMetodologiaDocenteMateria()`](../desasociarMetodologiaDocenteMateria/README.md) -- `AsignaturaGrado` es el último escalón de la cascada, sin nivel inferior que dependa del reparto. Confirmación con advertencia condicional si la `MetodologiaDocente` que se desasocia es la única de esa `AsignaturaGrado`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasociarMetodologiaDocenteAsignaturaGradoView`

**Responsabilidades:**
- presenta la asociación y, si es la única `MetodologiaDocente` de la `AsignaturaGrado`, la advertencia de que quedaría sin ninguna.
- pide confirmar/cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `DirectorGrado` solicita desasociar una `MetodologiaDocente`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO` en ambos casos -- "confirmada, lista actualizada" (verde) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- pregunta si la `AsignaturaGrado` quedaría sin ninguna `MetodologiaDocente` tras la desasociación (`quedaSinMetodologiasDocentesTrasDesasociar(asignaturaGradoId, metodologiaDocenteId)`), para que la Vista decida si muestra la advertencia -- no bloquea, solo informa.
- si el `DirectorGrado` confirma, desasocia real e inmediata (`desasociarMetodologiaDocente(asignaturaGradoId, metodologiaDocenteId)`).

**Colaboraciones:**
- **Entrada:** `DesasociarMetodologiaDocenteAsignaturaGradoView`.
- **Salida:** `AsignaturaGradoRepository`.

## Clases de modelo

### `AsignaturaGradoRepository`

**Responsabilidades:**
- responde si quedaría sin `MetodologiaDocente` tras desasociar una dada (`quedaSinMetodologiasDocentesTrasDesasociar(asignaturaGradoId, metodologiaDocenteId)`).
- elimina real e inmediata la asociación (`desasociarMetodologiaDocente(asignaturaGradoId, metodologiaDocenteId)`) -- no es un borrado de `MetodologiaDocente`, que sigue en el catálogo institucional y en la `Materia` si lo estaba.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/wireframes.puml) -- fuente de verdad de las dos variantes (normal/advertencia).
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasociarMetodologiaDocenteAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado o-r- MetodologiaDocente`.
- [Discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del `<<choice>>` (sin bloqueo, con advertencia condicional).
- [`asociarMetodologiaDocenteAAsignaturaGrado()`](../asociarMetodologiaDocenteAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asociación).

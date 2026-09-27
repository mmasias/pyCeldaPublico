<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > asignarProfesorAAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asignarProfesorAAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md): sin `<<choice>>`, asignación libre -- exclusivo de `Admin`, no de `DirectorGrado`. Cierra el hueco original que motivó este pipeline: hasta ahora no existía forma de completar `AsignaturaGrado -- Profesor` desde la UI, así que un `Grado` nuevo no se podía configurar al 100% sin scripts CLI.

**Efecto colateral sobre el ciclo de vida de `Guia` (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: este caso de uso **ya no toca `Guia -- Profesor` directamente**. Si la asignación cambia de verdad la plantilla y la `Guia` activa de esa `AsignaturaGrado` está `Aprobada`, el controlador la manda a `EnRevision` (`Guia.enviarARevision()`, sin re-ejecutar `c1`/`c2`/`c3`) y registra una fila de `HistorialCambio` (`campo="estado"`, `autor` centinela `0`, `comentario` fijo). En cualquier otro estado, nada más: la copia se sincroniza sola en la próxima aprobación (`Guia.aprobar()` re-deriva de la plantilla). Sustituye al viejo efecto de "rellenar `Guia.profesorado` si estaba vacío" (discussion #47).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsignarProfesorAAsignaturaGradoView`

**Responsabilidades:**
- presenta la selección de `Profesor` todavía no asignados a esta `AsignaturaGrado`.
- ofrece la navegación a solicitar la asignación.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `Admin` solicita asignar un `Profesor`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- lista los `Profesor` no asignados aún a esta `AsignaturaGrado` (`cargarProfesoresDisponibles(asignaturaGradoId)`).
- asigna real e inmediato (`asignarProfesor(asignaturaGradoId, profesorId)`). Si la plantilla cambió y la `Guia` activa está `Aprobada`, dispara `Guia.enviarARevision()` + fila de `HistorialCambio` -- nunca toca `Guia.profesorado` directamente (issue #254).

**Colaboraciones:**
- **Entrada:** `AsignarProfesorAAsignaturaGradoView`.
- **Salida:** `ProfesorRepository`, `AsignaturaGradoRepository`, `GuiaRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre`, `email` -- el subconjunto no asignado aún a esta `AsignaturaGrado`, del que se elige.

**Colaboraciones:**
- **Entrada:** listado por `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- lista los `Profesor` no asignados todavía a esta `AsignaturaGrado` (`listarDisponiblesParaAsignaturaGrado(asignaturaGradoId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Profesor`.

### `AsignaturaGrado`

**Responsabilidades:**
- gana un `Profesor` en su colección asociada (`AsignaturaGrado -- Profesor`, plantilla estable).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `AsignaturaGradoRepository`.
- **Salida:** compone `Profesor` asignados.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- persiste la nueva asignación (`asignarProfesor(asignaturaGradoId, profesorId)`) -- agregación simple, sin clase de asociación (discussion #33: mismo criterio que `MetodologiaDocente`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

### `Guia` / `GuiaRepository`

**Responsabilidades:**
- `GuiaRepository.obtenerPorAsignaturaGrado(asignaturaGradoId)` localiza la `Guia` activa (hoy exactamente una por `AsignaturaGrado`, sin `CursoAcademico` todavía) para el efecto colateral.
- `Guia.enviarARevision()` (Fat Model) la pasa de `Aprobada` a `EnRevision` cuando la plantilla cambió; el controlador añade la fila de `HistorialCambio`. `Guia.aprobar()`/`Guia.escalarAAprobada()` son las que después re-derivan `Guia -- Profesor` de la plantilla (ver [`aprobarGuia()`](../aprobarGuia/README.md)).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaGrado/README.md) -- el efecto colateral `Aprobada -> EnRevision` (issue #254).
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- `Guia -- Profesor` se re-deriva al aprobar; este CU deja de tocarlo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : asignarProfesorAAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado -- Profesor` (plantilla estable), `Guia -- Profesor` (re-derivada al aprobar, issue #254).
- [`desasignarProfesorAsignaturaGrado()`](../desasignarProfesorAsignaturaGrado/README.md) -- caso de uso complementario (baja de la asignación).

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > asignarProfesorAAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`asignarProfesorAAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/README.md): sin `<<choice>>`, asignación libre -- exclusivo de `Admin`, no de `DirectorPrograma`. Cierra el hueco original que motivó este pipeline: hasta ahora no existía forma de completar `AsignaturaPrograma -- Profesor` desde la UI, así que un `Programa` nuevo no se podía configurar al 100% sin scripts CLI.

**Efecto colateral sobre el ciclo de vida de `Guia` (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: este caso de uso **ya no toca `Guia -- Profesor` directamente**. Si la asignación cambia de verdad la plantilla y la `Guia` activa de esa `AsignaturaPrograma` está `Aprobada`, el controlador la manda a `EnRevision` (`Guia.enviarARevision()`, sin re-ejecutar `c1`/`c2`/`c3`) y registra una fila de `HistorialCambio` (`campo="estado"`, `autor` centinela `0`, `comentario` fijo). En cualquier otro estado, nada más: la copia se sincroniza sola en la próxima aprobación (`Guia.aprobar()` re-deriva de la plantilla). Sustituye al viejo efecto de "rellenar `Guia.profesorado` si estaba vacío" (discussion #47).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/asignarProfesorAAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AsignarProfesorAAsignaturaProgramaView`

**Responsabilidades:**
- presenta la selección de `Profesor` todavía no asignados a esta `AsignaturaPrograma`.
- ofrece la navegación a solicitar la asignación.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `Admin` solicita asignar un `Profesor`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- lista los `Profesor` no asignados aún a esta `AsignaturaPrograma` (`cargarProfesoresDisponibles(asignaturaProgramaId)`).
- asigna real e inmediato (`asignarProfesor(asignaturaProgramaId, profesorId)`). Si la plantilla cambió y la `Guia` activa está `Aprobada`, dispara `Guia.enviarARevision()` + fila de `HistorialCambio` -- nunca toca `Guia.profesorado` directamente (issue #254).

**Colaboraciones:**
- **Entrada:** `AsignarProfesorAAsignaturaProgramaView`.
- **Salida:** `ProfesorRepository`, `AsignaturaProgramaRepository`, `GuiaRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre`, `email` -- el subconjunto no asignado aún a esta `AsignaturaPrograma`, del que se elige.

**Colaboraciones:**
- **Entrada:** listado por `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- lista los `Profesor` no asignados todavía a esta `AsignaturaPrograma` (`listarDisponiblesParaAsignaturaPrograma(asignaturaProgramaId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Profesor`.

### `AsignaturaPrograma`

**Responsabilidades:**
- gana un `Profesor` en su colección asociada (`AsignaturaPrograma -- Profesor`, plantilla estable).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `AsignaturaProgramaRepository`.
- **Salida:** compone `Profesor` asignados.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- persiste la nueva asignación (`asignarProfesor(asignaturaProgramaId, profesorId)`) -- agregación simple, sin clase de asociación (discussion #33: mismo criterio que `MetodologiaDocente`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `Guia` / `GuiaRepository`

**Responsabilidades:**
- `GuiaRepository.obtenerPorAsignaturaPrograma(asignaturaProgramaId)` localiza la `Guia` activa (hoy exactamente una por `AsignaturaPrograma`, sin `CursoAcademico` todavía) para el efecto colateral.
- `Guia.enviarARevision()` (Fat Model) la pasa de `Aprobada` a `EnRevision` cuando la plantilla cambió; el controlador añade la fila de `HistorialCambio`. `Guia.aprobar()`/`Guia.escalarAAprobada()` son las que después re-derivan `Guia -- Profesor` de la plantilla (ver [`aprobarGuia()`](../aprobarGuia/README.md)).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/asignarProfesorAAsignaturaPrograma/README.md) -- el efecto colateral `Aprobada -> EnRevision` (issue #254).
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- `Guia -- Profesor` se re-deriva al aprobar; este CU deja de tocarlo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : asignarProfesorAAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma -- Profesor` (plantilla estable), `Guia -- Profesor` (re-derivada al aprobar, issue #254).
- [`desasignarProfesorAsignaturaPrograma()`](../desasignarProfesorAsignaturaPrograma/README.md) -- caso de uso complementario (baja de la asignación).

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirAsignaturasPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturasPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirAsignaturasPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasPrograma/README.md), en su variante invocada por `DirectorPrograma`: listado agregado por `Programa`, sin `<<choice>>`, de solo lectura -- fusiona las `AsignaturaPrograma` del `Programa` con el estado de su `Guia` del curso activo, reutilizando `GuiaRepository.listarDelPrograma(programaId)` (ya introducido por [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md)).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirAsignaturasPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirAsignaturasProgramaView`

**Responsabilidades:**
- presenta el listado de `AsignaturaPrograma` del `Programa`: asignatura, materia, curso, carácter, profesorado y estado de su `Guia`.
- ofrece la navegación a abrir cada `AsignaturaPrograma`.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el `DirectorPrograma` solicita abrir las AsignaturasPrograma de su Programa.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURAS_PROGRAMA_ABIERTO`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- lista las `AsignaturaPrograma` del `Programa` (`listarAsignaturasProgramaDelPrograma(programaId)`).
- lista las `Guia` del `Programa` (reutiliza `GuiaRepository.listarDelPrograma(programaId)`, ya existente) y fusiona cada `AsignaturaPrograma` con el `estado` de su `Guia` del `CursoAcademico` activo -- agregación de lectura, sin regla de negocio.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirAsignaturasProgramaView`.
- **Salida:** `AsignaturaProgramaRepository`, `GuiaRepository`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter` y su profesorado -- los datos mostrados en cada fila del listado, antes de fusionar con el estado de su `Guia`.

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaProgramaRepository`.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- lista las `AsignaturaPrograma` de un `Programa` (`listarDelPrograma(programaId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `Guia`

**Responsabilidades:**
- porta `estado`, ya usado por [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- aquí se reutiliza para colorear cada fila del listado de `AsignaturaPrograma`.

**Colaboraciones:**
- **Entrada:** listada por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- lista las `Guia` del `Programa` (`listarDelPrograma(programaId)`, método ya existente desde [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), reutilizado tal cual).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Guia`.

## Simplificación fuera de alcance de esta rebanada

**Sin botón `+ Crear`**: `crearAsignaturaPrograma()` es exclusivo de `Admin`, no de `DirectorPrograma` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), fuera de alcance de esta rebanada (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)) -- mismo criterio que [`abrirMaterias()`](../abrirMaterias/README.md).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasPrograma/wireframes.puml) -- fuente de verdad, incluida la variante `wireframe-porProfesor`.
- [Diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml) -- `PROGRAMA_ABIERTO --> ASIGNATURAS_PROGRAMA_ABIERTO : abrirAsignaturasPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa, Asignatura .. AsignaturaPrograma`, `AsignaturaPrograma -- Profesor`, `(AsignaturaPrograma, CursoAcademico) .. Guia`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- origen de `GuiaRepository.listarDelPrograma(programaId)`, reutilizado aquí sin cambios.
- [`abrirAsignaturaPrograma()`](../abrirAsignaturaPrograma/README.md) -- caso de uso alcanzado desde cada fila de este listado.

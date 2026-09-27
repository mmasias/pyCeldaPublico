<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirAsignaturasGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturasGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirAsignaturasGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/README.md), en su variante invocada por `DirectorGrado`: listado agregado por `Grado`, sin `<<choice>>`, de solo lectura -- fusiona las `AsignaturaGrado` del `Grado` con el estado de su `Guia` del curso activo, reutilizando `GuiaRepository.listarDelGrado(gradoId)` (ya introducido por [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md)).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/abrirAsignaturasGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `AbrirAsignaturasGradoView`

**Responsabilidades:**
- presenta el listado de `AsignaturaGrado` del `Grado`: asignatura, materia, curso, carácter, profesorado y estado de su `Guia`.
- ofrece la navegación a abrir cada `AsignaturaGrado`.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `DirectorGrado` solicita abrir las AsignaturasGrado de su Grado.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURAS_GRADO_ABIERTO`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- lista las `AsignaturaGrado` del `Grado` (`listarAsignaturasGradoDelGrado(gradoId)`).
- lista las `Guia` del `Grado` (reutiliza `GuiaRepository.listarDelGrado(gradoId)`, ya existente) y fusiona cada `AsignaturaGrado` con el `estado` de su `Guia` del `CursoAcademico` activo -- agregación de lectura, sin regla de negocio.
- no valida ni muta nada -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `AbrirAsignaturasGradoView`.
- **Salida:** `AsignaturaGradoRepository`, `GuiaRepository`.

## Clases de modelo

### `AsignaturaGrado`

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter` y su profesorado -- los datos mostrados en cada fila del listado, antes de fusionar con el estado de su `Guia`.

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaGradoRepository`.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- lista las `AsignaturaGrado` de un `Grado` (`listarDelGrado(gradoId)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

### `Guia`

**Responsabilidades:**
- porta `estado`, ya usado por [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- aquí se reutiliza para colorear cada fila del listado de `AsignaturaGrado`.

**Colaboraciones:**
- **Entrada:** listada por `GuiaRepository`.

### `GuiaRepository`

**Responsabilidades:**
- lista las `Guia` del `Grado` (`listarDelGrado(gradoId)`, método ya existente desde [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md), reutilizado tal cual).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Guia`.

## Simplificación fuera de alcance de esta rebanada

**Sin botón `+ Crear`**: `crearAsignaturaGrado()` es exclusivo de `Admin`, no de `DirectorGrado` (ver [actoresCasosUsoAdminOperativa.puml](/RUP/01-requisitos/01-actores-casos-uso/actoresCasosUsoAdminOperativa.puml)), fuera de alcance de esta rebanada (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)) -- mismo criterio que [`abrirMaterias()`](../abrirMaterias/README.md).

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirAsignaturasGrado/wireframes.puml) -- fuente de verdad, incluida la variante `wireframe-porProfesor`.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> ASIGNATURAS_GRADO_ABIERTO : abrirAsignaturasGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado, Asignatura .. AsignaturaGrado`, `AsignaturaGrado -- Profesor`, `(AsignaturaGrado, CursoAcademico) .. Guia`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- origen de `GuiaRepository.listarDelGrado(gradoId)`, reutilizado aquí sin cambios.
- [`abrirAsignaturaGrado()`](../abrirAsignaturaGrado/README.md) -- caso de uso alcanzado desde cada fila de este listado.

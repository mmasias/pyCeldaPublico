<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/crearAsignatura/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`crearAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md): CRUD real e inmediato contra `AsignaturaRepository`. `ECTS`, `contenido` y `estado` se completan al editar (`estado` nace `Vigente` por defecto, sin pedirlo -- patrón C->U, igual que `crearResultadoAprendizaje()`). La salida es única, sin rama de rechazo *sobre el `<<include>>`*: `<<include>> editarAsignatura()`, mismo patrón que [`crearUniversidad()`](../crearUniversidad/README.md) -- la transición de salida lleva la nota `editarAsignatura()` (regla de Requisitos).

**Retocado (issue #181, 2026-09-05)**: `<<choice>>` de rechazo por `codigo` duplicado, mismo patrón que [`crearPrograma()`](../crearPrograma/README.md) (issue #148) -- antes la salida era única sin ninguna rama.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/crearAsignatura/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `CrearAsignaturaView`

**Responsabilidades:**
- presenta el formulario de creación: `codigo` y `nombre`, ambos obligatorios.
- presenta el aviso de rechazo cuando el `<<choice>>` sale rojo.
- permite solicitar crear.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURAS_ABIERTO` -- el `Admin` solicita crear una `Asignatura` desde el listado.
- **Control:** `AsignaturaController`.
- **Salida:** `:Collaboration EditarAsignatura` vía `<<include>> editarAsignatura()` (verde) o `:ASIGNATURAS_ABIERTO` sin crear (rojo, código ya existente).

## Clases de controlador

### `AsignaturaController`

**Responsabilidades:**
- valida que `codigo` y `nombre` estén presentes (`validarDatosObligatorios(codigo, nombre)`).
- aplica el `<<choice>>` de unicidad: comprueba si el `codigo` ya existe (`AsignaturaRepository.existeCodigo(codigo)`) antes de crear -- dentro -> crea; ya existente -> no crea nada.
- crea la `Asignatura` directamente en `AsignaturaRepository`, real e inmediato (`crearAsignatura(codigo, nombre)`).

**Colaboraciones:**
- **Entrada:** `CrearAsignaturaView`.
- **Salida:** `AsignaturaRepository`.

## Clases de modelo

### `Asignatura`

**Responsabilidades:**
- porta `codigo` y `nombre` desde el momento de crearse; `estado` nace `Vigente` sin pedirlo.

**Colaboraciones:**
- **Entrada:** creada por `AsignaturaRepository`.

### `AsignaturaRepository`

**Responsabilidades:**
- comprueba si ya existe una `Asignatura` con ese `codigo` (`existeCodigo(codigo)`) -- global al catálogo institucional.
- crea la `Asignatura` (`crear(codigo, nombre)`) -- persistencia real e inmediata, no una mutación de sesión.

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** gestiona `Asignatura`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/wireframes.puml) -- fuente de verdad del formulario, con rama de rechazo por código duplicado.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURAS_ABIERTO --> ASIGNATURA_ABIERTO : crearAsignatura()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (codigo, nombre, ects, contenido, estado).
- [`editarAsignatura()`](../editarAsignatura/README.md) -- `<<include>>` de salida, mismo formulario que este caso de uso.
- [`crearUniversidad()`](../crearUniversidad/README.md) -- mismo patrón de creación con salida única vía `<<include>>`.
- [`crearPrograma()`](../crearPrograma/README.md) -- precedente del `<<choice>>` de unicidad de código (issue #148), reutilizado aquí.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > editarAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/README.md): CRUD real e inmediato contra `AsignaturaRepository`. Sin `<<choice>>` -- `Asignatura` no tiene ninguna regla de validación cruzada documentada en el modelo de dominio, solo los obligatorios `nombre` y `ects`; `contenido` es opcional. `estado` queda fuera del formulario: se gestiona en exclusiva desde [`eliminarAsignatura()`](../eliminarAsignatura/README.md) (Vigente/Extinguido). `Asignatura` gana aquí su método `actualizar(nombre, ects, contenido)`, mismo patrón que `Universidad.actualizar(nombre)`. Es también el destino del `<<include>>` de [`crearAsignatura()`](../crearAsignatura/README.md): tras crear, el `Admin` queda editando la `Asignatura` recién creada, completando `ECTS` y `contenido`.

**Retocado (issue #181, 2026-09-05)**: `codigo` (obligatorio y único desde `crearAsignatura()`) se muestra pero no viaja en `guardarCambios(...)` -- mismo criterio que `editarGrado()`: `codigo` no se puede mutar aquí.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarAsignatura/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarAsignaturaView`

**Responsabilidades:**
- presenta el formulario con los datos actuales de la `Asignatura`: `codigo` mostrado como solo lectura, `nombre`/`ects`/`contenido` editables -- sin `estado`.
- permite solicitar guardar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_ABIERTO` -- el `Admin` solicita editar la `Asignatura` abierta; también alcanzado como `<<include>>` de `crearAsignatura()`.
- **Control:** `AsignaturaController`.
- **Salida:** `:ASIGNATURA_ABIERTO`.

## Clases de controlador

### `AsignaturaController`

**Responsabilidades:**
- recupera la `Asignatura` a editar (`cargarAsignatura(asignaturaId)`, mismo método introducido por [`abrirAsignatura()`](../abrirAsignatura/README.md)).
- valida los obligatorios (`validarDatosObligatorios(nombre, ects)` -- el mismo método ya usado en crear con solo `nombre`; Análisis no distingue firmas por fase, mismo criterio que `UniversidadController`).
- guarda los cambios (`guardarCambios(asignaturaId, nombre, ects, contenido)`): sin `<<choice>>` de negocio que aplicar -- pide directamente a la `Asignatura` que se actualice y persiste.

**Colaboraciones:**
- **Entrada:** `EditarAsignaturaView`.
- **Salida:** `Asignatura`, `AsignaturaRepository`.

## Clases de modelo

### `Asignatura`

**Responsabilidades:**
- porta `codigo`, `nombre`, `ects` y `contenido`; solo `nombre`/`ects`/`contenido` son editables.
- se actualiza a sí misma (`actualizar(nombre, ects, contenido)`) -- mismo patrón que `Universidad.actualizar(nombre)`.

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** persistida por `AsignaturaRepository`.

### `AsignaturaRepository`

**Responsabilidades:**
- recupera la `Asignatura` por identificador (`obtener(asignaturaId)`).
- persiste la actualización (`actualizar(asignatura)`).

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** gestiona `Asignatura`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/wireframes.puml) -- fuente de verdad del formulario, sin rama de rechazo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_ABIERTO --> ASIGNATURA_ABIERTO : editarAsignatura()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Asignatura` (codigo, nombre, ects, contenido, estado); `estado` fuera del formulario.
- [`crearAsignatura()`](../crearAsignatura/README.md) -- `<<include>>` de origen, ya cerrado apuntando aquí; origen de `codigo` (issue #181).
- [`abrirAsignatura()`](../abrirAsignatura/README.md) -- mismo `AsignaturaController.cargarAsignatura(asignaturaId)`, reutilizado.
- [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- único gestor del `estado`, fuera de este formulario.
- [`editarUniversidad()`](../editarUniversidad/README.md) -- mismo patrón de edición sin `<<choice>>` de negocio.
- [`editarGrado()`](../editarGrado/README.md) -- mismo criterio de `codigo` fijo, mostrado solo lectura.

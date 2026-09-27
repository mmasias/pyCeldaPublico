<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirMaterias()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirMaterias()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/README.md), en sus dos variantes: la `DirectorGrado` (un solo paso, sin `<<choice>>`, de solo lectura -- punto de partida para que navegue hasta sus propios casos de asociación) y la `Admin` (mismo listado, alcanzada desde el enlace "Ver Materias" de la ficha del `Grado`, con `[Abrir]` por fila, `[Eliminar]` y `+ Crear Materia`). La estructura de clases es idéntica en ambas -- mismo `MateriaController.listarMateriasDelGrado(gradoId)` --; cambian el actor, la entrada (el `GRADO_ABIERTO` de cada diagrama de contexto) y las acciones que la Vista ofrece. `Admin` no tiene listado propio sin filtro: `Grado *-- Materia` es composición, se navega siempre desde dentro de un `Grado` concreto.

Este `colaboracion.puml` contiene **dos diagramas**: el primero (`abrirMaterias-analisis`) es la variante `DirectorGrado`; el segundo (`abrirMaterias-admin-analisis`) es la variante `Admin`, construida en el lote de Materia/AsignaturaGrado junto a [`crearMateria()`](../crearMateria/README.md) -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirGrados()`](../abrirGrados/README.md).

<div align=center>

|`DirectorGrado`|`Admin`|
|:-:|:-:|
|![](/images/RUP/02-analisis/casos-uso/abrirMaterias/colaboracion.svg)|![](/images/RUP/02-analisis/casos-uso/abrirMaterias/colaboracion-admin.svg)|
|<sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Clases de vista

### `AbrirMateriasView`

**Responsabilidades (variante DirectorGrado):**
- presenta el listado de `Materia` del `Grado`: `nombre`.
- ofrece la navegación a abrir cada `Materia` y a volver al `Grado`.

**Responsabilidades (variante Admin):**
- mismo listado de `nombre` con `[Abrir]` por fila (navega a la variante Admin de [`abrirMateria()`](../abrirMateria/README.md)).
- ofrece `+ Crear Materia` (navega a [`crearMateria()`](../crearMateria/README.md)) y `[Eliminar]` por fila -- este último deshabilitado en esta rebanada: `eliminarMateria()` no se construye aquí (el wireframe lo muestra, la rebanada no lo cubre).
- ofrece volver a la ficha del `Grado` (variante Admin de [`abrirGrado()`](../abrirGrado/README.md)).

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `DirectorGrado` o el `Admin` solicita abrir las Materias del `Grado` abierto.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIAS_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades:**
- lista las `Materia` de un `Grado` (`listarMateriasDelGrado(gradoId)`).
- no valida ni muta nada -- caso de uso de solo lectura en ambas variantes.

**Colaboraciones:**
- **Entrada:** `AbrirMateriasView`.
- **Salida:** `MateriaRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- porta `nombre` -- el dato mostrado en cada fila del listado.

**Colaboraciones:**
- **Entrada:** listada por `MateriaRepository`.

### `MateriaRepository`

**Responsabilidades:**
- lista las `Materia` de un `Grado` (`listarDelGrado(gradoId)`) -- `Grado *-- Materia`, composición: se navega desde dentro del `Grado` abierto, no es catálogo institucional plano.

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

## Simplificación fuera de alcance de esta rebanada

**`[Eliminar]` en la variante Admin**: `eliminarMateria()` es caso de uso de `Admin` pero no forma parte de esta rebanada -- el botón se muestra deshabilitado en la Vista. La rebanada original de `DirectorGrado` (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)) tampoco cubría el CRUD, solo la navegación (`[Abrir]`) hacia los casos de asociación.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMaterias/wireframes.puml) -- fuente de verdad del contenido presentado, compartidas por ambos actores.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `GRADO_ABIERTO --> MATERIAS_ABIERTO : abrirMaterias()`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> MATERIAS_ABIERTO : abrirMaterias()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado *-- Materia`.
- [`abrirMateria()`](../abrirMateria/README.md) -- caso de uso alcanzado desde cada fila de este listado, en ambas variantes.
- [`crearMateria()`](../crearMateria/README.md) -- acción `+ Crear Materia` de la variante Admin, construida en este mismo lote.

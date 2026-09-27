<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > abrirMateria()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/abrirMateria/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`abrirMateria()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/README.md), en sus dos variantes. La `DirectorGrado` (un solo paso, sin `<<choice>>`, de solo lectura) presenta el detalle de la `Materia` fusionando tres colecciones asociadas -- `MetodologiaDocente` (vía `MetodologiaMateria`), `ResultadoAprendizaje` y `AsignaturaGrado` -- mismo mecanismo de agregación de lectura que [`abrirGuia()`](../abrirGuia/README.md). La `Admin` es deliberadamente **reducida**: solo `nombre` y la tabla "Asignaturas de esta materia" (`AsignaturaGrado`) -- las secciones "Metodologías docentes asociadas" y "Resultados de aprendizaje asociadas" del wireframe existen para alojar los botones de asociación de `DirectorGrado` (ver [diagramaContextoAdmin.puml](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml)), que `Admin` no tiene; sin colecciones que fusionar, la variante queda en dos lecturas.

Este `colaboracion.puml` contiene **dos diagramas**: el primero (`abrirMateria-analisis`) es la variante `DirectorGrado`; el segundo (`abrirMateria-admin-analisis`) es la variante `Admin`, construida en el lote de Materia/AsignaturaGrado -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirGrados()`](../abrirGrados/README.md).

<div align=center>

|`DirectorGrado`|`Admin` (reducida)|
|:-:|:-:|
|![](/images/RUP/02-analisis/casos-uso/abrirMateria/colaboracion.svg)|![](/images/RUP/02-analisis/casos-uso/abrirMateria/colaboracion-admin.svg)|
|<sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Clases de vista

### `AbrirMateriaView`

**Responsabilidades (variante DirectorGrado):**
- presenta `nombre` de la `Materia`.
- presenta las `MetodologiaDocente` asociadas (`codigo`, `descripcion`, `descripcionPropia`), con navegación a editar/quitar cada una.
- presenta los `ResultadoAprendizaje` asociados (`codigo`, `tipo`), con navegación a quitar cada uno.
- presenta las `AsignaturaGrado` de la `Materia` (asignatura, curso, carácter), con navegación a abrir cada una.
- ofrece la navegación a asociar nuevas `MetodologiaDocente`/`ResultadoAprendizaje`, editar la `Materia` y volver al listado.

**Responsabilidades (variante Admin, reducida):**
- presenta `nombre` de la `Materia`.
- presenta la tabla "Asignaturas de esta materia" (asignatura, curso, carácter) -- sin navegación por fila en esta rebanada: el `[Abrir]` de cada fila queda deshabilitado (la variante Admin de `abrirAsignaturaGrado()` no se construye aquí).
- ofrece la navegación a editar la `Materia` ([`editarMateria()`](../editarMateria/README.md)) y a volver al listado (variante Admin de [`abrirMaterias()`](../abrirMaterias/README.md)).

**Colaboraciones:**
- **Entrada:** `:MATERIAS_ABIERTO` -- el `DirectorGrado` o el `Admin` solicita abrir una `Materia`.
- **Control:** `MateriaController`.
- **Salida:** `:MATERIA_ABIERTO`.

## Clases de controlador

### `MateriaController`

**Responsabilidades (variante DirectorGrado):**
- recupera la `Materia` (`cargarMateria(materiaId)`) para su dato propio.
- lista las `MetodologiaDocente` asociadas vía `MetodologiaMateria` (`listarMetodologiasDocentesAsociadas(materiaId)`).
- lista los `ResultadoAprendizaje` asociados (`listarResultadosAprendizajeAsociados(materiaId)`).
- lista las `AsignaturaGrado` de la `Materia` (`listarAsignaturasGrado(materiaId)`).
- no valida ni muta nada -- caso de uso de solo lectura.

**Responsabilidades (variante Admin, reducida):**
- recupera la `Materia` (`cargarMateria(materiaId)`).
- lista las `AsignaturaGrado` de la `Materia` (`listarAsignaturasGrado(materiaId)`) -- las dos colecciones de asociación no se piden: `Admin` no las usa.

**Colaboraciones:**
- **Entrada:** `AbrirMateriaView`.
- **Salida:** `MateriaRepository`, `MetodologiaMateriaRepository` (solo DirectorGrado), `AsignaturaGradoRepository`.

## Clases de modelo

### `Materia`

**Responsabilidades:**
- porta `nombre` y compone sus tres colecciones asociadas (`MetodologiaDocente` vía `MetodologiaMateria`, `ResultadoAprendizaje`, `AsignaturaGrado`); la variante Admin solo consume la última.

**Colaboraciones:**
- **Entrada:** `MateriaController`, vía `MateriaRepository`.

### `MateriaRepository`

**Responsabilidades:**
- recupera la `Materia` por identificador (`obtener(materiaId)`).
- lista los `ResultadoAprendizaje` asociados a una `Materia` (`listarResultadosAprendizajeDe(materiaId)`) -- solo variante DirectorGrado.

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `Materia`.

### `MetodologiaMateria`

**Responsabilidades:**
- porta `descripcionPropia` -- el override que la Vista muestra junto a `codigo`/`descripcion` de su `MetodologiaDocente` (solo variante DirectorGrado).

**Colaboraciones:**
- **Entrada:** listada por `MetodologiaMateriaRepository`.

### `MetodologiaMateriaRepository`

**Responsabilidades:**
- lista las asociaciones `MetodologiaMateria` de una `Materia` (`listarDe(materiaId)`) (solo variante DirectorGrado).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `MetodologiaMateria`.

### `AsignaturaGrado`

**Responsabilidades:**
- porta `nombre`, `curso`, `caracter` -- mostrados en la mini-tabla de la `Materia` en ambas variantes.

**Colaboraciones:**
- **Entrada:** listada por `AsignaturaGradoRepository`.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- lista las `AsignaturaGrado` de una `Materia` (`listarDeLaMateria(materiaId)`).

**Colaboraciones:**
- **Entrada:** `MateriaController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Simplificación fuera de alcance de esta rebanada

**Sin botón hacia `SistemasEvaluacion`**: la `Materia` también compone `SistemaEvaluacion` (usado por el hilo de `Guia`, ya construido), pero `abrirSistemasEvaluacion()` lleva a un estado hijo propio (`SISTEMAS_EVALUACION_ABIERTO`) -- no aparece aquí, mismo criterio documentado en Requisitos por el que `abrirGrado()` tampoco muestra botones hacia sus estados hijos.

**Sin `[Abrir]` activo por fila de `AsignaturaGrado` en la variante Admin**: `abrirAsignaturaGrado()` existe como CU de `DirectorGrado` (endpoint `/api/v1/asignaturas-grado/{id}` con guard de ese actor); su variante Admin no se construye en esta rebanada -- el botón se muestra deshabilitado.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/abrirMateria/wireframes.puml) -- fuente de verdad del contenido presentado; las secciones de asociación son de `DirectorGrado`, la variante Admin solo consume la tabla de `AsignaturaGrado`.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : abrirMateria()`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `MATERIAS_ABIERTO --> MATERIA_ABIERTO : abrirMateria()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- MetodologiaDocente` vía `MetodologiaMateria{descripcionPropia}`, `Materia o-u- ResultadoAprendizaje`, `Materia *-- AsignaturaGrado`.
- [`asociarMetodologiaDocenteAMateria()`](../asociarMetodologiaDocenteAMateria/README.md) / [`asociarResultadoAprendizajeAMateria()`](../asociarResultadoAprendizajeAMateria/README.md) -- quienes pueblan las dos listas de asociación que la variante DirectorGrado fusiona.
- [`editarMateria()`](../editarMateria/README.md) -- acción `[Editar]` de la variante Admin, construida en este mismo lote.
- [`editarActividadesFormativasMateria()`](../editarActividadesFormativasMateria/README.md) / [`consultarEstadoActividadesFormativasMateria()`](../consultarEstadoActividadesFormativasMateria/README.md) -- el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) añade una cuarta colección a la variante `DirectorGrado` (las 10 `ActividadFormativaMateria` + el medidor); la fusión de esa colección en `abrirMateria()` y el cambio de `MateriaDetalleResponse` se detallan al construir el clúster (audit del agregado `Materia`).

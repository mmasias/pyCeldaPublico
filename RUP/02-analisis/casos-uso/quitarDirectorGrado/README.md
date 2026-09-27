<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > quitarDirectorGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/quitarDirectorGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`quitarDirectorGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/README.md): `<<choice>>` bloqueante aplicado a quitar un rol, no a borrar una entidad -- mismo patrón que [`eliminarFacultad()`](../eliminarFacultad/README.md)/[`eliminarProfesor()`](../eliminarProfesor/README.md). Un `Grado` no puede quedarse sin ningún `DirectorGrado`: si el `Profesor` es el único director de ese `Grado`, el caso de uso bloquea sin llegar a pedir confirmación. El `<<choice>>` valida al inicio, antes de la pantalla de confirmación.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/quitarDirectorGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `QuitarDirectorGradoView`

**Responsabilidades:**
- en la rama verde, presenta la información del `Grado` y la advertencia de pérdida del rol, y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo por ser el único `DirectorGrado` del `Grado`.

**Colaboraciones:**
- **Entrada:** `:PROFESOR_ABIERTO` -- el `Admin` solicita quitar el rol sobre un `Grado` de la sección "Grados que dirige" del detalle.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO` (self-loop) en los tres casos -- "rol quitado, lista actualizada" (verde), "bloqueado, sin cambios" (rojo) o "cancelado, sin cambios" (azul).

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- aplica el `<<choice>>`: comprueba si el `Profesor` (rol resuelto por email) es el único `DirectorGrado` de ese `Grado` (`esUnicoDirectorDelGrado(profesorId, gradoId)`) -- dirige el `Grado` y el conteo de directores es exactamente 1.
- si no está bloqueado y el `Admin` confirma, retira la asociación (`quitarDirectorGrado(profesorId, gradoId)`).

**Colaboraciones:**
- **Entrada:** `QuitarDirectorGradoView`.
- **Salida:** `ProfesorRepository`, `DirectorGradoRepository`, `GradoRepository`.

## Clases de modelo

### `DirectorGrado`

**Responsabilidades:**
- porta el rol que se retira; la fila no desaparece -- un `DirectorGrado` sin `Grado` a su cargo deja de ser bloqueo en `eliminarProfesor()` pero sigue resolviendo el email en el inicio de sesión.

**Nota cruzada (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274))**: "sigue resolviendo el email en el inicio de sesión" ya no significa "enruta a `/grados`". La composición de esta frase con la regla de prioridad de [`iniciarSesion()`](../iniciarSesion/README.md) ("prioriza `DirectorGrado`", issue #93/#103) dejaba a un ex-director que además imparte enrutado de forma permanente a un listado de grados vacío. Corregido: el rol `director_grado` requiere ahora dirigir `>= 1` `Grado`; la fila huérfana resuelve `profesor` y aterriza en [`abrirInicio()`](../abrirInicio/README.md), que presenta "Mis grados" vacío (honesto) en vez de un callejón sin salida. La fila sigue sin borrarse -- el `<<choice>>` bloqueante del único director de un `Grado` no cambia. **Ni este caso de uso ni `eliminarProfesor()` tienen camino de limpieza de la fila de `directores_grado`: las filas huérfanas se acumulan** ([issue #275](https://github.com/mmasias/pyCelda/issues/275), deuda de datos, ya no bug funcional tras el guard de rol).

**Colaboraciones:**
- **Entrada:** resuelto por `DirectorGradoRepository`; desasociado de `Grado`.

### `Grado`

**Responsabilidades:**
- pierde al `DirectorGrado` de su colección `directores` -- nunca hasta quedarse vacía (la invariante del `<<choice>>`).

**Colaboraciones:**
- **Entrada:** recuperado por `GradoRepository`; mutado por `ProfesorController`.

### `ProfesorRepository` / `DirectorGradoRepository` / `GradoRepository`

**Responsabilidades:**
- `ProfesorRepository.obtener(profesorId)` -- el Profesor sobre el que recae el rol.
- `DirectorGradoRepository.obtenerPorEmail(email)` -- resolución del rol.
- `GradoRepository.dirige(gradoId, directorGradoId)` / `.contarDirectores(gradoId)` -- los dos datos del `<<choice>>`: que lo dirige y cuántos directores quedan.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestionan `Profesor` / `DirectorGrado` / `Grado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorGrado/wireframes.puml) -- fuente de verdad del `<<choice>>` del único director.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : quitarDirectorGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Grado o- DirectorGrado` (agregación, muchos a muchos).
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre del `<<choice>>` bloqueante.
- [`definirDirectorGrado()`](../definirDirectorGrado/README.md) -- caso de uso complementario (alta del rol, sin `<<choice>>`).
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- mismo patrón de `<<choice>>` bloqueante, allí sobre borrado de entidad.

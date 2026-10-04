<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > quitarDirectorPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/quitarDirectorPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`quitarDirectorPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/README.md): `<<choice>>` bloqueante aplicado a quitar un rol, no a borrar una entidad -- mismo patrón que [`eliminarFacultad()`](../eliminarFacultad/README.md)/[`eliminarProfesor()`](../eliminarProfesor/README.md). Un `Programa` no puede quedarse sin ningún `DirectorPrograma`: si el `Profesor` es el único director de ese `Programa`, el caso de uso bloquea sin llegar a pedir confirmación. El `<<choice>>` valida al inicio, antes de la pantalla de confirmación.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/quitarDirectorPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `QuitarDirectorProgramaView`

**Responsabilidades:**
- en la rama verde, presenta la información del `Programa` y la advertencia de pérdida del rol, y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo por ser el único `DirectorPrograma` del `Programa`.

**Colaboraciones:**
- **Entrada:** `:PROFESOR_ABIERTO` -- el `Admin` solicita quitar el rol sobre un `Programa` de la sección "Programas que dirige" del detalle.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESOR_ABIERTO` (self-loop) en los tres casos -- "rol quitado, lista actualizada" (verde), "bloqueado, sin cambios" (rojo) o "cancelado, sin cambios" (azul).

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- aplica el `<<choice>>`: comprueba si el `Profesor` (rol resuelto por email) es el único `DirectorPrograma` de ese `Programa` (`esUnicoDirectorDelPrograma(profesorId, programaId)`) -- dirige el `Programa` y el conteo de directores es exactamente 1.
- si no está bloqueado y el `Admin` confirma, retira la asociación (`quitarDirectorPrograma(profesorId, programaId)`).

**Colaboraciones:**
- **Entrada:** `QuitarDirectorProgramaView`.
- **Salida:** `ProfesorRepository`, `DirectorProgramaRepository`, `ProgramaRepository`.

## Clases de modelo

### `DirectorPrograma`

**Responsabilidades:**
- porta el rol que se retira; la fila no desaparece -- un `DirectorPrograma` sin `Programa` a su cargo deja de ser bloqueo en `eliminarProfesor()` pero sigue resolviendo el email en el inicio de sesión.

**Nota cruzada (discussion [#274](https://github.com/mmasias/pyCelda/discussions/274))**: "sigue resolviendo el email en el inicio de sesión" ya no significa "enruta a `/programas`". La composición de esta frase con la regla de prioridad de [`iniciarSesion()`](../iniciarSesion/README.md) ("prioriza `DirectorPrograma`", issue #93/#103) dejaba a un ex-director que además imparte enrutado de forma permanente a un listado de programas vacío. Corregido: el rol `director_programa` requiere ahora dirigir `>= 1` `Programa`; la fila huérfana resuelve `profesor` y aterriza en [`abrirInicio()`](../abrirInicio/README.md), que presenta "Mis programas" vacío (honesto) en vez de un callejón sin salida. La fila sigue sin borrarse -- el `<<choice>>` bloqueante del único director de un `Programa` no cambia. **Ni este caso de uso ni `eliminarProfesor()` tienen camino de limpieza de la fila de `directores_programa`: las filas huérfanas se acumulan** ([issue #275](https://github.com/mmasias/pyCelda/issues/275), deuda de datos, ya no bug funcional tras el guard de rol).

**Colaboraciones:**
- **Entrada:** resuelto por `DirectorProgramaRepository`; desasociado de `Programa`.

### `Programa`

**Responsabilidades:**
- pierde al `DirectorPrograma` de su colección `directores` -- nunca hasta quedarse vacía (la invariante del `<<choice>>`).

**Colaboraciones:**
- **Entrada:** recuperado por `ProgramaRepository`; mutado por `ProfesorController`.

### `ProfesorRepository` / `DirectorProgramaRepository` / `ProgramaRepository`

**Responsabilidades:**
- `ProfesorRepository.obtener(profesorId)` -- el Profesor sobre el que recae el rol.
- `DirectorProgramaRepository.obtenerPorEmail(email)` -- resolución del rol.
- `ProgramaRepository.dirige(programaId, directorProgramaId)` / `.contarDirectores(programaId)` -- los dos datos del `<<choice>>`: que lo dirige y cuántos directores quedan.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestionan `Profesor` / `DirectorPrograma` / `Programa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/quitarDirectorPrograma/wireframes.puml) -- fuente de verdad del `<<choice>>` del único director.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESOR_ABIERTO --> PROFESOR_ABIERTO : quitarDirectorPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Programa o- DirectorPrograma` (agregación, muchos a muchos).
- [Discussion #18](https://github.com/mmasias/pyCelda/discussions/18) -- cierre del `<<choice>>` bloqueante.
- [`definirDirectorPrograma()`](../definirDirectorPrograma/README.md) -- caso de uso complementario (alta del rol, sin `<<choice>>`).
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- mismo patrón de `<<choice>>` bloqueante, allí sobre borrado de entidad.

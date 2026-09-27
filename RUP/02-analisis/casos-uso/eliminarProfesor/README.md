<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarProfesor()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarProfesor/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarProfesor()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo institucional. La especificación nombra tres motivos ("AsignaturaGrado asignadas, rol de DirectorGrado activo o Guias que lo referencian") -- las tres se comprueban por separado, como tres condiciones reales e independientes.

**Actualizado tras el pipeline de `asignarProfesorAAsignaturaGrado()`/`desasignarProfesorAsignaturaGrado()`** (posterior a esta pieza -- cierra el issue [#13](https://github.com/mmasias/pyCelda/issues/13) de verdad, ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)): al escribir esta pieza, `Guia.profesorado` era una `@property` derivada en vivo de `AsignaturaGrado.profesorado`, sin tabla propia -- comprobar `asignaturas_grado_profesores` una vez cubría el estado en vivo de los dos primeros motivos combinados, pero no protegía el historial (`desasignarProfesorAsignaturaGrado()` habría vaciado retroactivamente `Guia -- Profesor`). `Guia.profesorado` es ahora relación M2M propia (`guias_profesores`), copiada puntualmente al crear la `Guia` y nunca tocada al desasignar -- así que hoy son tres consultas reales: `AsignaturaGrado` asignadas, `Guia` que referencian (tabla propia, independiente), y rol de `DirectorGrado` activo.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarProfesor/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarProfesorView`

**Responsabilidades:**
- en la rama verde, presenta la información del `Profesor` y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo con los motivos presentes: los nombres de sus `AsignaturaGrado` asignadas, de las `Guia` que impartió, y/o de los `Grado` que dirige.

**Colaboraciones:**
- **Entrada:** `:PROFESORES_ABIERTO` -- el `Admin` solicita eliminar un `Profesor` del listado.
- **Control:** `ProfesorController`.
- **Salida:** `:PROFESORES_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- aplica el `<<choice>>`: pregunta si el `Profesor` tiene algo que lo referencia (`puedeEliminar(profesorId)`).
- si no está bloqueado y el `Admin` confirma, elimina real e inmediato (`eliminar(profesorId)`) -- borrado físico, sin `estado` propio que mutar.

**Colaboraciones:**
- **Entrada:** `EliminarProfesorView`.
- **Salida:** `ProfesorRepository`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre` y `email` -- la información presentada antes de confirmar.

**Colaboraciones:**
- **Entrada:** recuperada por `ProfesorRepository`.
- **Salida:** eliminado físicamente por `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- responde con los motivos de bloqueo presentes (`motivosBloqueoEliminacion(profesorId)`) -- una frase por motivo real, tres condiciones independientes: las `AsignaturaGrado` asignadas, las `Guia` que impartió (referencia histórica, propia, no derivada), y los `Grado` que dirige como `DirectorGrado` activo. Lista vacía significa que puede eliminarse; los nombres alimentan el mensaje de la rama roja.
- elimina el `Profesor` (`eliminar(profesorId)`) -- borrado físico.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `Profesor`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarProfesor/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROFESORES_ABIERTO --> PROFESORES_ABIERTO : eliminarProfesor()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado -- Profesor`, `Grado o- DirectorGrado`, `Guia -- Profesor` como relación propia (issue #13, cerrado de verdad).
- [`eliminarMetodologiaDocente()`](../eliminarMetodologiaDocente/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico y nombres en el mensaje; allí una sola tabla basta, aquí son tres consultas independientes.
- [`quitarDirectorGrado()`](../quitarDirectorGrado/README.md) / [`desasignarProfesorAsignaturaGrado()`](../desasignarProfesorAsignaturaGrado/README.md) -- deshacen dos de los tres motivos; el de `Guia` (historial) es permanente, no se puede deshacer.

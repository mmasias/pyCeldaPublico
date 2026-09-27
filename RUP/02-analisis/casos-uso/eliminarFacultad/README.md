<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarFacultad()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarFacultad/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarFacultad()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarFacultad/README.md): `<<choice>>` bloqueante -- borrado físico de la `Facultad`, bloqueado si tiene `Grado`s asociados (`Facultad *-d- Grado`, composición: primero se eliminan o reubican los Grados). `Facultad` se borra físicamente -- no tiene `estado` propio que mutar, a diferencia de `Grado`/`Asignatura`, cuyo borrado es lógico. Mismo patrón que `eliminarResultadoAprendizaje()`/`eliminarMateria()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarFacultad/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarFacultadView`

**Responsabilidades:**
- en la rama verde, presenta la información y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo por `Grado`s asociados.

**Colaboraciones:**
- **Entrada:** `:FACULTADES_ABIERTO` -- el `Admin` solicita eliminar una `Facultad`.
- **Control:** `FacultadController`.
- **Salida:** `:FACULTADES_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `FacultadController`

**Responsabilidades:**
- aplica el `<<choice>>`: pregunta si la `Facultad` tiene `Grado`s asociados (`puedeEliminar(facultadId)`).
- si no está bloqueada y el `Admin` confirma, elimina real e inmediato (`eliminar(facultadId)`).

**Colaboraciones:**
- **Entrada:** `EliminarFacultadView`.
- **Salida:** `FacultadRepository`.

## Clases de modelo

### `FacultadRepository`

**Responsabilidades:**
- responde si la `Facultad` tiene `Grado`s asociados (`tieneGradosAsociados(facultadId)`) -- origen de la regla de bloqueo: la composición `Facultad *-d- Grado` no deja Grados huérfanos.
- elimina la `Facultad` (`eliminar(facultadId)`) -- borrado físico, sin `estado` propio que mutar.

**Colaboraciones:**
- **Entrada:** `FacultadController`.
- **Salida:** gestiona `Facultad`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarFacultad/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarFacultad/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `FACULTADES_ABIERTO --> FACULTADES_ABIERTO : eliminarFacultad()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Universidad *-d- Facultad`, `Facultad *-d- Grado` (origen de la regla de bloqueo).
- [`abrirFacultades()`](../abrirFacultades/README.md) -- listado que ofrece `[Eliminar]` por fila, punto de invocación.
- [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarResultadoAprendizaje()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md)|[Desarrollo](/RUP/04-desarrollo/casos-uso/eliminarResultadoAprendizaje/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarResultadoAprendizaje()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo del `Grado`, bloqueado si el `ResultadoAprendizaje` está asignado a cualquier `Materia` o `AsignaturaGrado` (los dos niveles de la cascada). `ResultadoAprendizaje` no tiene `estado` propio, mismo patrón que `eliminarMateria()`.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarResultadoAprendizajeView`

**Responsabilidades:**
- en la rama verde, presenta la información y pide confirmar/cancelar.
- en la rama roja, presenta el mensaje de bloqueo por uso en `Materia`/`AsignaturaGrado`.

**Colaboraciones:**
- **Entrada:** `:RESULTADOS_APRENDIZAJE_ABIERTO` -- el `DirectorGrado` solicita eliminar un `ResultadoAprendizaje`.
- **Control:** `ResultadoAprendizajeController`.
- **Salida:** `:RESULTADOS_APRENDIZAJE_ABIERTO` en los tres casos -- "lista actualizada" (verde), "bloqueada, sin cambios" (rojo) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ResultadoAprendizajeController`

**Responsabilidades:**
- aplica el `<<choice>>`: pregunta si el `ResultadoAprendizaje` está asignado a alguna `Materia` o `AsignaturaGrado` (`puedeEliminar(resultadoAprendizajeId)`).
- si no está bloqueado y el `DirectorGrado` confirma, elimina real e inmediato (`eliminar(resultadoAprendizajeId)`).

**Colaboraciones:**
- **Entrada:** `EliminarResultadoAprendizajeView`.
- **Salida:** `ResultadoAprendizajeRepository`.

## Clases de modelo

### `ResultadoAprendizajeRepository`

**Responsabilidades:**
- responde si el `ResultadoAprendizaje` está asignado a cualquier `Materia` o `AsignaturaGrado` (`estaAsignado(resultadoAprendizajeId)`) -- cubre los dos niveles de la cascada en una sola consulta: ningún RA llega a una `AsignaturaGrado` sin pasar antes por su `Materia`.
- elimina el `ResultadoAprendizaje` (`eliminar(resultadoAprendizajeId)`) -- borrado físico, sin `estado` propio que mutar.

**Colaboraciones:**
- **Entrada:** `ResultadoAprendizajeController`.
- **Salida:** gestiona `ResultadoAprendizaje`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/wireframes.puml) -- fuente de verdad del `<<choice>>` bloqueante.
- [Diagrama de contexto de DirectorGrado](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.puml) -- `RESULTADOS_APRENDIZAJE_ABIERTO --> RESULTADOS_APRENDIZAJE_ABIERTO : eliminarResultadoAprendizaje()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Materia o-- ResultadoAprendizaje`, `AsignaturaGrado o- ResultadoAprendizaje` (origen de la regla de bloqueo, cascada en dos pasos).

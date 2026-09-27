<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarGrado/README.md): borrado lógico, sin `<<choice>>` bloqueante -- mismo patrón exacto que [`eliminarAsignatura()`](../eliminarAsignatura/README.md). El modelo de dominio cierra que `Grado` (junto con `Asignatura` y `AsignaturaGrado`) nunca se borra físicamente -- usa `estado` (Vigente/Extinguido): Extinguido bloquea altas nuevas (`Materia`, `AsignaturaGrado`...) pero preserva lo existente para no romper `Guia` históricas. Por eso confirmar aquí siempre tiene éxito y solo hay dos ramas: verde (confirma, `estado` pasa a `Extinguido`) y azul (cancela, sin cambios). No existe la rama roja de bloqueo por "tiene hijos" que sí necesita [`eliminarFacultad()`](../eliminarFacultad/README.md) -- allí `Facultad` sí se borra físicamente.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarGradoView`

**Responsabilidades:**
- presenta la información del `Grado` y pide confirmar/cancelar -- directamente, sin `<<choice>>` previo que decida qué mostrar (a diferencia de `EliminarFacultadView`, que primero consulta si hay `Grado` asociados).

**Colaboraciones:**
- **Entrada:** `:GRADOS_ABIERTO` -- el `Admin` solicita eliminar un `Grado`.
- **Control:** `GradoController`.
- **Salida:** `:GRADOS_ABIERTO` en los dos casos -- "lista actualizada" (verde, `estado` pasa a `Extinguido`) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `GradoController`

**Responsabilidades:**
- si el `Admin` confirma, extingue el `Grado` (`eliminar(gradoId)`) -- borrado lógico, no físico.
- sin `puedeEliminar()`: no hay `<<choice>>` que aplicar, a diferencia de `FacultadController`.

**Colaboraciones:**
- **Entrada:** `EliminarGradoView`.
- **Salida:** `Grado`, `GradoRepository`.

## Clases de modelo

### `Grado`

**Responsabilidades:**
- se extingue a sí misma (`extinguir()`) -- pasa `estado` a `Extinguido`; invocada solo por `GradoController.eliminar(gradoId)`, nunca desde la edición.

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** persistida por `GradoRepository`.

### `GradoRepository`

**Responsabilidades:**
- persiste el `Grado` con su nuevo `estado` (`actualizar(grado)`) -- la entidad sigue existiendo, ningún borrado físico.

**Colaboraciones:**
- **Entrada:** `GradoController`.
- **Salida:** gestiona `Grado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarGrado/wireframes.puml) -- fuente de verdad de las dos ramas, sin bloqueo; el aviso naranja explica qué implica `Extinguido`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADOS_ABIERTO --> GRADOS_ABIERTO : eliminarGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- README, "Nada del catálogo se borra físicamente (`Grado`, `Asignatura`, `AsignaturaGrado`): usan `estado` (Vigente/Extinguido)".
- [`editarGrado()`](../editarGrado/README.md) -- el otro caso de uso que muta `Grado`, siempre sin tocar `estado`.
- [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- mismo patrón exacto de borrado lógico sin `<<choice>>`.
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- contraste: borrado físico con `<<choice>>` bloqueante.

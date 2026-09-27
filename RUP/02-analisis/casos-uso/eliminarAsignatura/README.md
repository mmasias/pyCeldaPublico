<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarAsignatura()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarAsignatura/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarAsignatura()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/README.md): borrado lógico, sin `<<choice>>` bloqueante. El modelo de dominio cierra que `Asignatura` (junto con `Grado` y `AsignaturaGrado`) nunca se borra físicamente -- usa `estado` (Vigente/Extinguido): Extinguido bloquea altas nuevas pero preserva lo existente para no romper `Guia` históricas. Por eso confirmar aquí siempre tiene éxito y solo hay dos ramas: verde (confirma, `estado` pasa a `Extinguido`) y azul (cancela, sin cambios). No existe la rama roja de bloqueo por "tiene hijos" que sí necesita [`eliminarFacultad()`](../eliminarFacultad/README.md) -- allí `Facultad` sí se borra físicamente.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarAsignatura/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarAsignaturaView`

**Responsabilidades:**
- presenta la información de la `Asignatura` y pide confirmar/cancelar -- directamente, sin `<<choice>>` previo que decida qué mostrar (a diferencia de `EliminarFacultadView`, que primero consulta si hay `Grado` asociados).

**Colaboraciones:**
- **Entrada:** `:ASIGNATURAS_ABIERTO` -- el `Admin` solicita eliminar una `Asignatura`.
- **Control:** `AsignaturaController`.
- **Salida:** `:ASIGNATURAS_ABIERTO` en los dos casos -- "lista actualizada" (verde, `estado` pasa a `Extinguido`) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `AsignaturaController`

**Responsabilidades:**
- si el `Admin` confirma, extingue la `Asignatura` (`eliminar(asignaturaId)`) -- borrado lógico, no físico.
- sin `puedeEliminar()`: no hay `<<choice>>` que aplicar, a diferencia de `FacultadController`.

**Colaboraciones:**
- **Entrada:** `EliminarAsignaturaView`.
- **Salida:** `Asignatura`, `AsignaturaRepository`.

## Clases de modelo

### `Asignatura`

**Responsabilidades:**
- se extingue a sí misma (`extinguir()`) -- pasa `estado` a `Extinguido`; invocada solo por `AsignaturaController.eliminar(asignaturaId)`, nunca desde la edición.

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** persistida por `AsignaturaRepository`.

### `AsignaturaRepository`

**Responsabilidades:**
- persiste la `Asignatura` con su nuevo `estado` (`actualizar(asignatura)`) -- la entidad sigue existiendo, ningún borrado físico.

**Colaboraciones:**
- **Entrada:** `AsignaturaController`.
- **Salida:** gestiona `Asignatura`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/wireframes.puml) -- fuente de verdad de las dos ramas, sin bloqueo.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURAS_ABIERTO --> ASIGNATURAS_ABIERTO : eliminarAsignatura()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- README, "Nada del catálogo se borra físicamente (`Grado`, `Asignatura`, `AsignaturaGrado`): usan `estado` (Vigente/Extinguido)".
- [`editarAsignatura()`](../editarAsignatura/README.md) -- el otro caso de uso que muta `Asignatura`, siempre sin tocar `estado`.
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- contraste: borrado físico con `<<choice>>` bloqueante.
- [`eliminarResultadoAprendizaje()`](../eliminarResultadoAprendizaje/README.md) -- otro contraste de borrado físico con `<<choice>>`.

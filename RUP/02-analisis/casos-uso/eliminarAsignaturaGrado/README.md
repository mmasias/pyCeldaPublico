<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > eliminarAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaGrado/README.md): borrado lógico, sin `<<choice>>` bloqueante -- mismo patrón exacto que [`eliminarGrado()`](../eliminarGrado/README.md)/[`eliminarAsignatura()`](../eliminarAsignatura/README.md). El modelo de dominio cierra que `AsignaturaGrado` (junto con `Grado` y `Asignatura`) nunca se borra físicamente -- usa `estado` (Vigente/Extinguido): Extinguido bloquea altas nuevas apoyadas en ella pero preserva lo existente para no romper `Guia` históricas. Por eso confirmar aquí siempre tiene éxito y solo hay dos ramas: verde (confirma, `estado` pasa a `Extinguido`) y azul (cancela, sin cambios). No existe la rama roja de bloqueo por "tiene hijos" que sí necesita [`eliminarFacultad()`](../eliminarFacultad/README.md) -- allí `Facultad` sí se borra físicamente. `AsignaturaGrado` gana aquí su método `extinguir()`. Se dispara desde la tabla de `AsignaturaGrado` embebida en la ficha del `Grado` (variante Admin de [`abrirGrado()`](../abrirGrado/README.md)), con pantalla de confirmación dedicada, no acción inline.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarAsignaturaGradoView`

**Responsabilidades:**
- presenta la información de la `AsignaturaGrado` y la advertencia de extinción; pide confirmar/cancelar -- directamente, sin `<<choice>>` previo que decida qué mostrar.

**Colaboraciones:**
- **Entrada:** `:GRADO_ABIERTO` -- el `Admin` solicita eliminar una `AsignaturaGrado` desde la tabla embebida de la ficha del `Grado`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:GRADO_ABIERTO` en los dos casos -- "tabla actualizada" (verde, `estado` pasa a `Extinguido`) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- si el `Admin` confirma, extingue la `AsignaturaGrado` (`eliminar(asignaturaGradoId)`) -- borrado lógico, no físico.
- sin `puedeEliminar()`: no hay `<<choice>>` que aplicar.

**Colaboraciones:**
- **Entrada:** `EliminarAsignaturaGradoView`.
- **Salida:** `AsignaturaGrado`, `AsignaturaGradoRepository`.

## Clases de modelo

### `AsignaturaGrado`

**Responsabilidades:**
- se extingue a sí misma (`extinguir()`) -- pasa `estado` a `Extinguido`; invocada solo por `AsignaturaGradoController.eliminar(asignaturaGradoId)`, nunca desde la edición.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** persistida por `AsignaturaGradoRepository`.

### `AsignaturaGradoRepository`

**Responsabilidades:**
- persiste la `AsignaturaGrado` con su nuevo `estado` (`actualizar(asignaturaGrado)`) -- la entidad sigue existiendo, ningún borrado físico.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaGrado/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaGrado/wireframes.puml) -- fuente de verdad de las dos ramas, sin bloqueo; el aviso naranja explica qué implica `Extinguido`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `GRADO_ABIERTO --> GRADO_ABIERTO : eliminarAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- README, "Nada del catálogo se borra físicamente (`Grado`, `Asignatura`, `AsignaturaGrado`): usan `estado` (Vigente/Extinguido)".
- [`eliminarGrado()`](../eliminarGrado/README.md) -- mismo patrón exacto de borrado lógico sin `<<choice>>`.
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- contraste: borrado físico con `<<choice>>` bloqueante.
- [`crearAsignaturaGrado()`](../crearAsignaturaGrado/README.md) -- la otra acción sobre la misma tabla embebida, construida en este mismo lote.

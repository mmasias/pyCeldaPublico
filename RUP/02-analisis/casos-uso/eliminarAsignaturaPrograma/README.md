<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/README.md): borrado lógico, sin `<<choice>>` bloqueante -- mismo patrón exacto que [`eliminarPrograma()`](../eliminarPrograma/README.md)/[`eliminarAsignatura()`](../eliminarAsignatura/README.md). El modelo de dominio cierra que `AsignaturaPrograma` (junto con `Programa` y `Asignatura`) nunca se borra físicamente -- usa `estado` (Vigente/Extinguido): Extinguido bloquea altas nuevas apoyadas en ella pero preserva lo existente para no romper `Guia` históricas. Por eso confirmar aquí siempre tiene éxito y solo hay dos ramas: verde (confirma, `estado` pasa a `Extinguido`) y azul (cancela, sin cambios). No existe la rama roja de bloqueo por "tiene hijos" que sí necesita [`eliminarFacultad()`](../eliminarFacultad/README.md) -- allí `Facultad` sí se borra físicamente. `AsignaturaPrograma` gana aquí su método `extinguir()`. Se dispara desde la tabla de `AsignaturaPrograma` embebida en la ficha del `Programa` (variante Admin de [`abrirPrograma()`](../abrirPrograma/README.md)), con pantalla de confirmación dedicada, no acción inline.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarAsignaturaProgramaView`

**Responsabilidades:**
- presenta la información de la `AsignaturaPrograma` y la advertencia de extinción; pide confirmar/cancelar -- directamente, sin `<<choice>>` previo que decida qué mostrar.

**Colaboraciones:**
- **Entrada:** `:PROGRAMA_ABIERTO` -- el `Admin` solicita eliminar una `AsignaturaPrograma` desde la tabla embebida de la ficha del `Programa`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:PROGRAMA_ABIERTO` en los dos casos -- "tabla actualizada" (verde, `estado` pasa a `Extinguido`) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- si el `Admin` confirma, extingue la `AsignaturaPrograma` (`eliminar(asignaturaProgramaId)`) -- borrado lógico, no físico.
- sin `puedeEliminar()`: no hay `<<choice>>` que aplicar.

**Colaboraciones:**
- **Entrada:** `EliminarAsignaturaProgramaView`.
- **Salida:** `AsignaturaPrograma`, `AsignaturaProgramaRepository`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- se extingue a sí misma (`extinguir()`) -- pasa `estado` a `Extinguido`; invocada solo por `AsignaturaProgramaController.eliminar(asignaturaProgramaId)`, nunca desde la edición.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** persistida por `AsignaturaProgramaRepository`.

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- persiste la `AsignaturaPrograma` con su nuevo `estado` (`actualizar(asignaturaPrograma)`) -- la entidad sigue existiendo, ningún borrado físico.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/wireframes.puml) -- fuente de verdad de las dos ramas, sin bloqueo; el aviso naranja explica qué implica `Extinguido`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMA_ABIERTO --> PROGRAMA_ABIERTO : eliminarAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- README, "Nada del catálogo se borra físicamente (`Programa`, `Asignatura`, `AsignaturaPrograma`): usan `estado` (Vigente/Extinguido)".
- [`eliminarPrograma()`](../eliminarPrograma/README.md) -- mismo patrón exacto de borrado lógico sin `<<choice>>`.
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- contraste: borrado físico con `<<choice>>` bloqueante.
- [`crearAsignaturaPrograma()`](../crearAsignaturaPrograma/README.md) -- la otra acción sobre la misma tabla embebida, construida en este mismo lote.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/eliminarPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`eliminarPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/eliminarPrograma/README.md): borrado lógico, sin `<<choice>>` bloqueante -- mismo patrón exacto que [`eliminarAsignatura()`](../eliminarAsignatura/README.md). El modelo de dominio cierra que `Programa` (junto con `Asignatura` y `AsignaturaPrograma`) nunca se borra físicamente -- usa `estado` (Vigente/Extinguido): Extinguido bloquea altas nuevas (`Materia`, `AsignaturaPrograma`...) pero preserva lo existente para no romper `Guia` históricas. Por eso confirmar aquí siempre tiene éxito y solo hay dos ramas: verde (confirma, `estado` pasa a `Extinguido`) y azul (cancela, sin cambios). No existe la rama roja de bloqueo por "tiene hijos" que sí necesita [`eliminarFacultad()`](../eliminarFacultad/README.md) -- allí `Facultad` sí se borra físicamente.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/eliminarPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EliminarProgramaView`

**Responsabilidades:**
- presenta la información del `Programa` y pide confirmar/cancelar -- directamente, sin `<<choice>>` previo que decida qué mostrar (a diferencia de `EliminarFacultadView`, que primero consulta si hay `Programa` asociados).

**Colaboraciones:**
- **Entrada:** `:PROGRAMAS_ABIERTO` -- el `Admin` solicita eliminar un `Programa`.
- **Control:** `ProgramaController`.
- **Salida:** `:PROGRAMAS_ABIERTO` en los dos casos -- "lista actualizada" (verde, `estado` pasa a `Extinguido`) o "cancelada, sin cambios" (azul).

## Clases de controlador

### `ProgramaController`

**Responsabilidades:**
- si el `Admin` confirma, extingue el `Programa` (`eliminar(programaId)`) -- borrado lógico, no físico.
- sin `puedeEliminar()`: no hay `<<choice>>` que aplicar, a diferencia de `FacultadController`.

**Colaboraciones:**
- **Entrada:** `EliminarProgramaView`.
- **Salida:** `Programa`, `ProgramaRepository`.

## Clases de modelo

### `Programa`

**Responsabilidades:**
- se extingue a sí misma (`extinguir()`) -- pasa `estado` a `Extinguido`; invocada solo por `ProgramaController.eliminar(programaId)`, nunca desde la edición.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** persistida por `ProgramaRepository`.

### `ProgramaRepository`

**Responsabilidades:**
- persiste el `Programa` con su nuevo `estado` (`actualizar(programa)`) -- la entidad sigue existiendo, ningún borrado físico.

**Colaboraciones:**
- **Entrada:** `ProgramaController`.
- **Salida:** gestiona `Programa`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarPrograma/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/eliminarPrograma/wireframes.puml) -- fuente de verdad de las dos ramas, sin bloqueo; el aviso naranja explica qué implica `Extinguido`.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `PROGRAMAS_ABIERTO --> PROGRAMAS_ABIERTO : eliminarPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- README, "Nada del catálogo se borra físicamente (`Programa`, `Asignatura`, `AsignaturaPrograma`): usan `estado` (Vigente/Extinguido)".
- [`editarPrograma()`](../editarPrograma/README.md) -- el otro caso de uso que muta `Programa`, siempre sin tocar `estado`.
- [`eliminarAsignatura()`](../eliminarAsignatura/README.md) -- mismo patrón exacto de borrado lógico sin `<<choice>>`.
- [`eliminarFacultad()`](../eliminarFacultad/README.md) -- contraste: borrado físico con `<<choice>>` bloqueante.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# pyCelda > desasignarProfesorAsignaturaGrado()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaGrado/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasignarProfesorAsignaturaGrado()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md): sin `<<choice>>` bloqueante, confirmación con advertencia condicional si es el único `Profesor`. **No toca `Guia -- Profesor` directamente**; sí gana un efecto colateral sobre el ciclo de vida de la `Guia` activa (issue [#254](https://github.com/mmasias/pyCelda/issues/254)): si la desasignación cambia la plantilla y esa `Guia` está `Aprobada`, pasa a `EnRevision` para que el `DirectorGrado` re-apruebe -- al aprobar, `Guia.aprobar()` re-deriva `Guia -- Profesor` de la plantilla y el profesor desasignado sale de la copia. Espejo exacto de [`asignarProfesorAAsignaturaGrado()`](../asignarProfesorAAsignaturaGrado/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaGrado/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasignarProfesorAsignaturaGradoView`

**Responsabilidades:**
- presenta al `Profesor` que se desasigna y la `AsignaturaGrado`.
- calcula "quedaría sin profesorado" en el propio cliente (ya tiene el `profesorado` completo cargado desde el detalle de la `AsignaturaGrado`) -- sin llamada de backend nueva, a diferencia de `quedaSinMetodologiasDocentesTrasDesasociar()`/`quedaSinResultadosAprendizajeTrasDesasociar()`, que sí son consulta aparte.
- permite solicitar confirmar/cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_GRADO_ABIERTO` -- el `Admin` solicita desasignar un `Profesor`.
- **Control:** `AsignaturaGradoController`.
- **Salida:** `:ASIGNATURA_GRADO_ABIERTO`.

## Clases de controlador

### `AsignaturaGradoController`

**Responsabilidades:**
- desasigna real e inmediato, sin `<<choice>>` que resolver (`desasignarProfesor(asignaturaGradoId, profesorId)`).
- si la plantilla cambió y la `Guia` activa está `Aprobada`, dispara `Guia.enviarARevision()` + fila de `HistorialCambio` -- nunca toca `Guia.profesorado` (issue #254).

**Colaboraciones:**
- **Entrada:** `DesasignarProfesorAsignaturaGradoView`.
- **Salida:** `AsignaturaGradoRepository`, `GuiaRepository`, `Guia`.

## Clases de modelo

### `AsignaturaGrado`

**Responsabilidades:**
- pierde un `Profesor` de su colección asociada.

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`, vía `AsignaturaGradoRepository`.
- **Salida:** compone `Profesor` asignados (sin el retirado).

### `AsignaturaGradoRepository`

**Responsabilidades:**
- retira la asignación (`desasignarProfesor(asignaturaGradoId, profesorId)`) -- agregación simple, sin invariante de mínimo (a diferencia de `Grado`-`DirectorGrado`).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `AsignaturaGrado`.

### `Guia` / `GuiaRepository`

**Responsabilidades:**
- `GuiaRepository.obtenerPorAsignaturaGrado(asignaturaGradoId)` localiza la `Guia` activa; `Guia.enviarARevision()` (Fat Model) la pasa de `Aprobada` a `EnRevision` cuando la desasignación cambió la plantilla. La re-derivación de `Guia -- Profesor` ocurre después, en `Guia.aprobar()`/`escalarAAprobada()` (ver [`aprobarGuia()`](../aprobarGuia/README.md)).

**Colaboraciones:**
- **Entrada:** `AsignaturaGradoController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md) -- confirmación con advertencia condicional, sin bloqueo (discussion #33).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_GRADO_ABIERTO --> ASIGNATURA_GRADO_ABIERTO : desasignarProfesorAsignaturaGrado()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaGrado -- Profesor`; `Guia -- Profesor` re-derivada al aprobar (issue #254).
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- efecto colateral `Aprobada -> EnRevision`.
- [`asignarProfesorAAsignaturaGrado()`](../asignarProfesorAAsignaturaGrado/README.md) -- caso de uso complementario (alta de la asignación), mismo efecto.
- [`eliminarProfesor()` en Desarrollo](/RUP/04-desarrollo/casos-uso/eliminarProfesor/README.md) -- `motivosBloqueoEliminacion()` comprueba `Guia -- Profesor` aparte. Con #254 la copia sigue a la plantilla en la siguiente aprobación: matiz interino (ahora -> #222) -- un profesor desasignado de todo pasa a ser borrable en cuanto se re-aprueba la guía activa, todavía no hay acta archivada que proteger.

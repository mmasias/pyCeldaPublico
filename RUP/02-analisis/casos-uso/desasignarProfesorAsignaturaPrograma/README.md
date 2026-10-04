<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasignarProfesorAsignaturaPrograma()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaPrograma/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`desasignarProfesorAsignaturaPrograma()`](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md): sin `<<choice>>` bloqueante, confirmación con advertencia condicional si es el único `Profesor`. **No toca `Guia -- Profesor` directamente**; sí gana un efecto colateral sobre el ciclo de vida de la `Guia` activa (issue [#254](https://github.com/mmasias/pyCelda/issues/254)): si la desasignación cambia la plantilla y esa `Guia` está `Aprobada`, pasa a `EnRevision` para que el `DirectorPrograma` re-apruebe -- al aprobar, `Guia.aprobar()` re-deriva `Guia -- Profesor` de la plantilla y el profesor desasignado sale de la copia. Espejo exacto de [`asignarProfesorAAsignaturaPrograma()`](../asignarProfesorAAsignaturaPrograma/README.md).

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaPrograma/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `DesasignarProfesorAsignaturaProgramaView`

**Responsabilidades:**
- presenta al `Profesor` que se desasigna y la `AsignaturaPrograma`.
- calcula "quedaría sin profesorado" en el propio cliente (ya tiene el `profesorado` completo cargado desde el detalle de la `AsignaturaPrograma`) -- sin llamada de backend nueva, a diferencia de `quedaSinMetodologiasDocentesTrasDesasociar()`/`quedaSinResultadosAprendizajeTrasDesasociar()`, que sí son consulta aparte.
- permite solicitar confirmar/cancelar.

**Colaboraciones:**
- **Entrada:** `:ASIGNATURA_PROGRAMA_ABIERTO` -- el `Admin` solicita desasignar un `Profesor`.
- **Control:** `AsignaturaProgramaController`.
- **Salida:** `:ASIGNATURA_PROGRAMA_ABIERTO`.

## Clases de controlador

### `AsignaturaProgramaController`

**Responsabilidades:**
- desasigna real e inmediato, sin `<<choice>>` que resolver (`desasignarProfesor(asignaturaProgramaId, profesorId)`).
- si la plantilla cambió y la `Guia` activa está `Aprobada`, dispara `Guia.enviarARevision()` + fila de `HistorialCambio` -- nunca toca `Guia.profesorado` (issue #254).

**Colaboraciones:**
- **Entrada:** `DesasignarProfesorAsignaturaProgramaView`.
- **Salida:** `AsignaturaProgramaRepository`, `GuiaRepository`, `Guia`.

## Clases de modelo

### `AsignaturaPrograma`

**Responsabilidades:**
- pierde un `Profesor` de su colección asociada.

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`, vía `AsignaturaProgramaRepository`.
- **Salida:** compone `Profesor` asignados (sin el retirado).

### `AsignaturaProgramaRepository`

**Responsabilidades:**
- retira la asignación (`desasignarProfesor(asignaturaProgramaId, profesorId)`) -- agregación simple, sin invariante de mínimo (a diferencia de `Programa`-`DirectorPrograma`).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `AsignaturaPrograma`.

### `Guia` / `GuiaRepository`

**Responsabilidades:**
- `GuiaRepository.obtenerPorAsignaturaPrograma(asignaturaProgramaId)` localiza la `Guia` activa; `Guia.enviarARevision()` (Fat Model) la pasa de `Aprobada` a `EnRevision` cuando la desasignación cambió la plantilla. La re-derivación de `Guia -- Profesor` ocurre después, en `Guia.aprobar()`/`escalarAAprobada()` (ver [`aprobarGuia()`](../aprobarGuia/README.md)).

**Colaboraciones:**
- **Entrada:** `AsignaturaProgramaController`.
- **Salida:** gestiona `Guia`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md) -- confirmación con advertencia condicional, sin bloqueo (discussion #33).
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `ASIGNATURA_PROGRAMA_ABIERTO --> ASIGNATURA_PROGRAMA_ABIERTO : desasignarProfesorAsignaturaPrograma()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `AsignaturaPrograma -- Profesor`; `Guia -- Profesor` re-derivada al aprobar (issue #254).
- [Issue #254](https://github.com/mmasias/pyCelda/issues/254) / [discussion #255](https://github.com/mmasias/pyCelda/discussions/255) -- efecto colateral `Aprobada -> EnRevision`.
- [`asignarProfesorAAsignaturaPrograma()`](../asignarProfesorAAsignaturaPrograma/README.md) -- caso de uso complementario (alta de la asignación), mismo efecto.
- `eliminarProfesor()` en Desarrollo -- `motivosBloqueoEliminacion()` comprueba `Guia -- Profesor` aparte. Con #254 la copia sigue a la plantilla en la siguiente aprobación: matiz interino (ahora -> #222) -- un profesor desasignado de todo pasa a ser borrable en cuanto se re-aprueba la guía activa, todavía no hay acta archivada que proteger.

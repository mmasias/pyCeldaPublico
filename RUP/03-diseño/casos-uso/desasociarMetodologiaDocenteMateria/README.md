<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > desasociarMetodologiaDocenteMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`desasociarMetodologiaDocenteMateria()`](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteMateria/README.md): `<<choice>>` bloqueante -- rompe `MetodologiaMateria` solo si ninguna `AsignaturaGrado` de la `Materia` usa ya esa `MetodologiaDocente` (primer escalón de la cascada de dos pasos). El chequeo de Análisis (`Materia.tieneMetodologiaDocenteEnUso()`) es un método del Modelo: se conserva como Fat Model, no baja al Repository.

**Retocado (issue #179, 2026-09-05)**: `tiene_metodologia_docente_en_uso() : bool` pasa a `asignaturas_grado_con_metodologia_docente() : list[str]` -- mismo patrón que `ResultadoAprendizajeRepository.nombres_asignaciones()` (PR #178), auditado y replicado aquí. El endpoint de chequeo pasa de `bool` a `list[str]` ([] = no bloqueada); el `DELETE` reverifica y construye el 409 con los mismos nombres.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarMetodologiaDocenteMateriaView` (React) -- pide la lista de bloqueo antes de confirmar; en la rama bloqueada presenta el motivo con los nombres reales.
- **API**: `routers/materia.py::puede_desasociar_metodologia_docente(materia_id, metodologia_docente_id)` / `::desasociar_metodologia_docente(materia_id, metodologia_docente_id)` -- funciones sueltas.
- **Modelo**: `Materia.asignaturas_grado_con_metodologia_docente(metodologia_docente_id)` -- recorre sus `AsignaturaGrado` y devuelve los nombres de las que ya usan la `MetodologiaDocente`; regla de bloqueo en el Modelo, no en la consulta.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` (con las asociadas cargadas por relación ORM) / `MetodologiaMateriaRepository.eliminar(materia_id, metodologia_docente_id)` -- borra la fila de asociación, no la `MetodologiaDocente`.

## Decisiones de diseño

- **La regla de bloqueo queda en el Modelo, como en Análisis**: Diseño lo traduce cargando la `Materia` con sus relaciones (un solo `SELECT` con `joinedload`) y preguntando al objeto, en vez de duplicar la regla como `SELECT` del Repository. Una sola fuente de verdad de la invariante.
- **`asignaturas_grado_con_metodologia_docente()` reemplaza `tiene_metodologia_docente_en_uso()` (issue #179)**: no coexisten los dos métodos -- el booleano se deriva trivialmente de `len(...) > 0` donde hace falta (no en este caso, ya que el propio detalle es lo que la Vista necesita mostrar). Mismo criterio que `ResultadoAprendizajeRepository.nombres_asignaciones()` (PR #178): la lista es la fuente de verdad única, no una segunda consulta redundante junto al booleano.
- **El endpoint de chequeo cambia de contrato: `bool` -> `list[str]`** (`[]` = no bloqueada) -- único consumidor es esta pantalla, verificado antes de cambiarlo (sin otros lugares del frontend que dependieran del booleano).
- **El `DELETE` reverifica antes de borrar**, no confía en el chequeo previo (pudo cambiar entre el `GET` y la confirmación) -- 409 con el mismo formato de nombres que el precedente de `ResultadoAprendizaje` (`f"AsignaturaGrado {nombre!r}"`, unidos por coma).
- **Dos endpoints (chequeo + `DELETE`)**, mismo criterio que `eliminarResultadoAprendizaje()`: el bloqueo debe conocerse antes de abrir el diálogo de confirmación.
- **204 No Content**: el `DELETE` no devuelve entidad; la Vista refresca el listado de asociadas de la `Materia`.
- **La rama "cancelada" no genera llamada HTTP** -- se modela como rama del `alt` para reflejar las tres salidas de Análisis (verde/roja/azul).

## Referencias

- [`desasociarMetodologiaDocenteMateria()` en Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocenteMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocenteMateria/README.md).
- [`desasociarMetodologiaDocenteAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteAsignaturaGrado/README.md) -- contraste: último escalón, sin bloqueo, solo advertencia condicional.
- [`desasociarResultadoAprendizajeAMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarResultadoAprendizajeAMateria/README.md) -- mismo patrón de bloqueo con el otro asociado.
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- precedente del patrón de mensaje con nombres reales (PR #178), auditado y replicado aquí (issue #179).

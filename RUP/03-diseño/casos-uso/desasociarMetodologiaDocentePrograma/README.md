<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasociarMetodologiaDocentePrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocentePrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`desasociarMetodologiaDocentePrograma()`](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocentePrograma/README.md): `<<choice>>` bloqueante -- rompe `Programa o-- MetodologiaDocente` solo si ninguna `Materia` del `Programa` la tiene asociada. El chequeo de Análisis (`Programa.materiasConMetodologiaDocente()`) es un método del Modelo: se conserva como Fat Model, no baja al Repository. `ProgramaController` converge en `routers/programa.py`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasociarMetodologiaDocentePrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasociarMetodologiaDocenteProgramaView` (React) -- pide la lista de bloqueo antes de confirmar; en la rama bloqueada presenta el motivo con los nombres reales.
- **API**: `routers/programa.py::puede_desasociar_metodologia_docente_del_programa(programa_id, metodologia_docente_id)` / `::desasociar_metodologia_docente_del_programa(programa_id, metodologia_docente_id)` -- funciones sueltas; ambas pasan por `_verificar_programa_del_director()`.
- **Modelo**: `Programa.materias_con_metodologia_docente(metodologia_docente_id)` -- recorre sus `Materia` y sus `MetodologiaMateria` y devuelve los nombres de las `Materia` que ya la usan; regla de bloqueo en el Modelo, no en la consulta.
- **Repositorio**: `ProgramaRepository.obtener(programa_id)` / `ProgramaRepository.desasociar_metodologia_docente(programa_id, metodologia_docente_id)` -- borra la fila de `programas_metodologias_docentes`, no la `MetodologiaDocente`.

## Decisiones de diseño

- **La regla de bloqueo queda en el Modelo, como en Análisis**: Diseño lo traduce cargando el `Programa` y preguntando al objeto, en vez de duplicar la regla como `SELECT` del Repository. Una sola fuente de verdad de la invariante; mismo patrón que `Materia.asignaturas_programa_con_metodologia_docente()` en el nivel inferior.
- **Devuelve `list[str]`, no un booleano** desde el principio: la `Vista` necesita los nombres de las `Materia` para el mensaje de bloqueo (mismo criterio que el retoque del issue [#179](https://github.com/mmasias/pyCelda/issues/179) en `desasociarMetodologiaDocenteMateria()`).
- **El `DELETE` reverifica antes de borrar**, no confía en el chequeo previo (pudo cambiar entre el `GET` y la confirmación) -- 409 con `En uso en: Materia 'X'` (nombres unidos por coma).
- **Dos endpoints (chequeo + `DELETE`)**: el bloqueo debe conocerse antes de abrir el diálogo de confirmación.
- **Sin clase de asociación**: a diferencia de `desasociarMetodologiaDocenteMateria()` (que borra vía `MetodologiaMateriaRepository.eliminar()`), la tabla intermedia es del propio `Programa` y la borra `ProgramaRepository`.
- **Un único endpoint para `DirectorPrograma` y `Admin`** (`_verificar_programa_del_director()` deja pasar a `Admin`); no hay endpoint espejo `/api/v1/admin/...`. La secuencia es idéntica con `Admin` como actor.
- **204 No Content**: el `DELETE` no devuelve entidad; la Vista refresca el listado de asociadas del `Programa`.
- **La rama "cancelada" no genera llamada HTTP** -- se modela como rama del `alt` para reflejar las tres salidas de Análisis (verde/roja/azul).

## Referencias

- [`desasociarMetodologiaDocentePrograma()` en Análisis](/RUP/02-analisis/casos-uso/desasociarMetodologiaDocentePrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasociarMetodologiaDocentePrograma/README.md).
- [`desasociarMetodologiaDocenteMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/README.md) -- plantilla estructural: mismo bloqueo un nivel más abajo.
- [`asociarMetodologiaDocenteAPrograma()` en Diseño](/RUP/03-diseño/casos-uso/asociarMetodologiaDocenteAPrograma/README.md) -- caso de uso complementario.

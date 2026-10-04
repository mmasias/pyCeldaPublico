<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > desasignarProfesorAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26

## Propósito

Bajada a diseño del caso de análisis [`desasignarProfesorAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaPrograma/README.md): sin `<<choice>>` bloqueante -- confirmación con advertencia condicional si es el único `Profesor` de la `AsignaturaPrograma`, resuelta en el propio cliente. Un único endpoint retira la asignación.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasignarProfesorAsignaturaProgramaView` (React) -- carga el detalle de la `AsignaturaPrograma` (ya la trae el listado/detalle previos), calcula si el `Profesor` a desasignar es el único de la lista y presenta confirmar/cancelar con la advertencia si aplica; al confirmar, `DELETE`.
- **API**: `routers/asignatura_programa.py::desasignar_profesor_de_asignatura_programa(asignatura_programa_id, profesor_id)` -- `404` si la `AsignaturaPrograma` no existe o si el `Profesor` no está asignado a ella.
- **Modelo**: la asociación vive en la tabla M2M `asignaturas_programa_profesores` -- el router retira de `AsignaturaPrograma.profesorado`. Efecto colateral #254: el mismo helper `_revisar_guia_por_cambio_de_profesorado()` que `asignarProfesorAAsignaturaPrograma()` -- si la `Guia` activa está `Aprobada`, `guia.enviar_a_revision()` + fila de `HistorialCambio` (autor centinela), atómico con el `DELETE` de la plantilla. Nunca toca `Guia -- Profesor`.
- **Repositorio**: `AsignaturaProgramaRepository.imparte(asignatura_programa_id, profesor_id)` (ya existía, reutilizado como guardia de pertenencia) / `.desasignar_profesor(asignatura_programa_id, profesor_id)` (nuevo).

## Decisiones de diseño

- **Advertencia calculada en el cliente, sin endpoint dedicado**: a diferencia de `quedaSinMetodologiasDocentesTrasDesasociar()`/`quedaSinResultadosAprendizajeTrasDesasociar()` (consulta aparte al backend), la Vista ya tiene el `profesorado` completo de la `AsignaturaPrograma` cargado desde el detalle -- `otrosProfesores.length === 0` es toda la lógica que hace falta, sin round-trip extra. Decisión mecánica de esta implementación, no un patrón nuevo que generalizar.
- **`404`, no `409`, para "no está asignado"**: pedir la baja de una asociación que no existe es un problema de identificador, no un conflicto de estado -- mismo reparto que otros `404` de asociación inexistente del proyecto.
- **Sin `<<choice>>` bloqueante, confirmado contra el código**: no hay invariante de mínimo profesorado (a diferencia de `Programa`-`DirectorPrograma`, que exige al menos un `DirectorPrograma`) -- `desasignar_profesor()` siempre procede si la asociación existe.
- **Solo toca `AsignaturaPrograma.profesorado`, nunca `Guia.profesorado`** -- el punto central de todo este pipeline: antes de la migración de `Guia.profesorado` a relación propia, este endpoint habría vaciado retroactivamente el profesorado de `Guia` ya creadas (el hallazgo del issue #13 de PR #137). Con `Guia.profesorado` como tabla independiente (`guias_profesores`, no tocada aquí), la referencia histórica sobrevive intacta.
- **`204 No Content`**: retirada de una fila M2M, sin entidad que devolver.
- **La rama "cancelada" no genera llamada HTTP**: no pulsar el botón es la cancelación.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`desasignarProfesorAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaPrograma/README.md) y [discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del sin-bloqueo.
- [`asignarProfesorAAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaPrograma/README.md) -- el alta complementaria.
- [`eliminarProfesor()` en Diseño](/RUP/03-diseño/casos-uso/eliminarProfesor/README.md) -- ahora que `Guia.profesorado` es relación propia, un `Profesor` desasignado aquí que impartió esa `Guia` sigue bloqueado para el borrado físico (issue #13, cerrado de verdad).

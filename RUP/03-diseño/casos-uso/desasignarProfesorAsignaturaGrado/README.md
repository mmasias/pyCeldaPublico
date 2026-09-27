<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > desasignarProfesorAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26

## Propósito

Bajada a diseño del caso de análisis [`desasignarProfesorAsignaturaGrado()`](/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaGrado/README.md): sin `<<choice>>` bloqueante -- confirmación con advertencia condicional si es el único `Profesor` de la `AsignaturaGrado`, resuelta en el propio cliente. Un único endpoint retira la asignación.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/desasignarProfesorAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `DesasignarProfesorAsignaturaGradoView` (React) -- carga el detalle de la `AsignaturaGrado` (ya la trae el listado/detalle previos), calcula si el `Profesor` a desasignar es el único de la lista y presenta confirmar/cancelar con la advertencia si aplica; al confirmar, `DELETE`.
- **API**: `routers/asignatura_grado.py::desasignar_profesor_de_asignatura_grado(asignatura_grado_id, profesor_id)` -- `404` si la `AsignaturaGrado` no existe o si el `Profesor` no está asignado a ella.
- **Modelo**: la asociación vive en la tabla M2M `asignaturas_grado_profesores` -- el router retira de `AsignaturaGrado.profesorado`. Efecto colateral #254: el mismo helper `_revisar_guia_por_cambio_de_profesorado()` que `asignarProfesorAAsignaturaGrado()` -- si la `Guia` activa está `Aprobada`, `guia.enviar_a_revision()` + fila de `HistorialCambio` (autor centinela), atómico con el `DELETE` de la plantilla. Nunca toca `Guia -- Profesor`.
- **Repositorio**: `AsignaturaGradoRepository.imparte(asignatura_grado_id, profesor_id)` (ya existía, reutilizado como guardia de pertenencia) / `.desasignar_profesor(asignatura_grado_id, profesor_id)` (nuevo).

## Decisiones de diseño

- **Advertencia calculada en el cliente, sin endpoint dedicado**: a diferencia de `quedaSinMetodologiasDocentesTrasDesasociar()`/`quedaSinResultadosAprendizajeTrasDesasociar()` (consulta aparte al backend), la Vista ya tiene el `profesorado` completo de la `AsignaturaGrado` cargado desde el detalle -- `otrosProfesores.length === 0` es toda la lógica que hace falta, sin round-trip extra. Decisión mecánica de esta implementación, no un patrón nuevo que generalizar.
- **`404`, no `409`, para "no está asignado"**: pedir la baja de una asociación que no existe es un problema de identificador, no un conflicto de estado -- mismo reparto que otros `404` de asociación inexistente del proyecto.
- **Sin `<<choice>>` bloqueante, confirmado contra el código**: no hay invariante de mínimo profesorado (a diferencia de `Grado`-`DirectorGrado`, que exige al menos un `DirectorGrado`) -- `desasignar_profesor()` siempre procede si la asociación existe.
- **Solo toca `AsignaturaGrado.profesorado`, nunca `Guia.profesorado`** -- el punto central de todo este pipeline: antes de la migración de `Guia.profesorado` a relación propia, este endpoint habría vaciado retroactivamente el profesorado de `Guia` ya creadas (el hallazgo del issue #13 de PR #137). Con `Guia.profesorado` como tabla independiente (`guias_profesores`, no tocada aquí), la referencia histórica sobrevive intacta.
- **`204 No Content`**: retirada de una fila M2M, sin entidad que devolver.
- **La rama "cancelada" no genera llamada HTTP**: no pulsar el botón es la cancelación.
- **Autorización de `Admin`: `Depends(require_admin)`**.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`desasignarProfesorAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/desasignarProfesorAsignaturaGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/desasignarProfesorAsignaturaGrado/README.md) y [discussion #33](https://github.com/mmasias/pyCelda/discussions/33) -- cierre del sin-bloqueo.
- [`asignarProfesorAAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/asignarProfesorAAsignaturaGrado/README.md) -- el alta complementaria.
- [`eliminarProfesor()` en Diseño](/RUP/03-diseño/casos-uso/eliminarProfesor/README.md) -- ahora que `Guia.profesorado` es relación propia, un `Profesor` desasignado aquí que impartió esa `Guia` sigue bloqueado para el borrado físico (issue #13, cerrado de verdad).

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > eliminarMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`eliminarMetodologiaDocente()`](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo institucional, bloqueado si la `MetodologiaDocente` está asociada a alguna `Materia` (tabla `metodologias_materia`). A diferencia de `eliminarAsignatura()` (borrado lógico sin bloqueo), aquí sí hay rama roja, y el motivo del bloqueo nombra las `Materia` asociadas en el `detail` del `409`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarMetodologiaDocenteView` (React) -- carga la información con `GET /api/v1/metodologias-docentes/{metodologia_docente_id}` y pide confirmar/cancelar; si la confirmación recibe `409`, presenta la rama bloqueada con el `detail` tal cual (los nombres de las `Materia` asociadas).
- **API**: `routers/metodologia_docente.py::eliminar_metodologia_docente(metodologia_docente_id)` -- función suelta, un único endpoint que resuelve el `<<choice>>` y el borrado.
- **Modelo**: ninguno con lógica propia invocada -- sin `estado` propio que mutar, el borrado es físico (a diferencia de `Asignatura.extinguir()`).
- **Repositorio**: `MetodologiaDocenteRepository.nombres_materias_asociadas(metodologia_docente_id)` (join `metodologias_materia` -> `Materia`) / `.eliminar(metodologia_docente_id)`.

## Decisiones de diseño

- **Un solo endpoint, sin `GET` de chequeo previo**: a diferencia de `eliminarResultadoAprendizaje()`/`eliminarFacultad()` (dos endpoints: chequeo + `DELETE`), aquí el `<<choice>>` se resuelve dentro del propio `DELETE` -- lista vacía de `nombres_materias_asociadas()` procede al borrado (`204`), lista no vacía devuelve `409` con el `detail` `MetodologiaDocente asignada a: ...`. La Vista presenta la confirmación con la información del `GET` de detalle y la rama bloqueada aparece al confirmar, mostrando ese `detail` tal cual. La invariante queda protegida en el servidor aunque un cliente dispare el `DELETE` a ciegas: el endpoint reconsulta antes de borrar.
- **El bloqueo comprueba solo `metodologias_materia`, no `asignaturas_grado_metodologias_docentes`** -- decisión cerrada, no una simplificación: el guard de `desasociarMetodologiaDocenteMateria()` (409 si la metodología está en uso en alguna `AsignaturaGrado` de esa `Materia`) garantiza que una `MetodologiaDocente` nunca puede estar asociada a una `AsignaturaGrado` sin estar también asociada a la `Materia` padre -- `listar_disponibles_para_asignatura_grado()` solo ofrece como disponibles las que ya están en `metodologias_materia` de la `Materia`. Si `metodologias_materia` no tiene ninguna fila para la metodología, es imposible que `asignaturas_grado_metodologias_docentes` sí la tenga: comprobar solo la primera tabla es correcto y suficiente.
- **`nombres_materias_asociadas()` devuelve nombres, no un booleano** -- mismo patrón que `ResultadoAprendizajeRepository.nombres_asignaciones()` (PR [#132](https://github.com/mmasias/pyCelda/pull/132)) pero solo con `Materia`, sin `AsignaturaGrado`: la lista vacía es el booleano (puede eliminarse) y los nombres alimentan el `detail` del `409` -- un método, dos usos.
- **`204 No Content` para el `DELETE`**: borrado físico, no hay entidad que devolver (contraste con `eliminarAsignatura()`, que devuelve `200` con el objeto `Extinguido` porque el recurso sigue existiendo) -- la Vista refresca el listado.
- **La rama "cancelada" no genera llamada HTTP**: la cancelación cierra el diálogo en el cliente -- se modela como rama del `alt` para reflejar las tres salidas de Análisis (verde/roja/azul), pero sin tocar el backend.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio, no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de `Admin`, sin pertenencia que verificar. Especialmente relevante aquí por ser endpoint de borrado: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`eliminarMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/eliminarMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarMetodologiaDocente/README.md).
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico y `detail` con nombres; allí con `GET` de chequeo previo.
- [`eliminarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignatura/README.md) -- contraste: borrado lógico sin `<<choice>>`, `200` con el objeto actualizado.
- [`desasociarMetodologiaDocenteMateria()` en Diseño](/RUP/03-diseño/casos-uso/desasociarMetodologiaDocenteMateria/README.md) -- el guard cuya invariante hace suficiente el chequeo de una sola tabla.

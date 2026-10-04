<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: ClaudeF-pyCelda-SDF1

## Propósito

Bajada a diseño del caso de análisis [`eliminarActividadFormativa()`](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md): `<<choice>>` bloqueante -- borrado físico, bloqueado si la `ActividadFormativa` está en uso (horas > 0 en alguna `Materia` o `AsignaturaPrograma`). El motivo del bloqueo nombra las `Materia` afectadas en el `detail` del `409`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarActividadFormativaView` (React) -- carga la información con `GET /api/v1/actividades-formativas/{actividad_formativa_id}` y pide confirmar/cancelar; si la confirmación recibe `409`, presenta la rama bloqueada con el `detail` tal cual.
- **API**: `routers/actividad_formativa.py::eliminar_actividad_formativa(actividad_formativa_id)` -- función suelta, un único endpoint que resuelve el `<<choice>>` y el borrado.
- **Modelo**: ninguno con lógica propia invocada -- borrado físico.
- **Repositorio**: `ActividadFormativaRepository.nombres_materias_asociadas(actividad_formativa_id)` / `.eliminar(actividad_formativa_id)`.

## Decisiones de diseño

- **Un solo endpoint, sin `GET` de chequeo previo**: el `<<choice>>` se resuelve dentro del propio `DELETE` -- lista vacía de `nombres_materias_asociadas()` procede al borrado (`204`), lista no vacía devuelve `409` con el `detail` `ActividadFormativa asignada a: ...`. La Vista confirma con la información del `GET` de detalle y la rama bloqueada aparece al confirmar. La invariante queda protegida en el servidor aunque un cliente dispare el `DELETE` a ciegas.
- **"En uso" = horas > 0, no mera existencia de fila**: toda `Materia`/`AsignaturaPrograma` de la `Universidad` tiene una fila a 0 por actividad (autopoblado); contarlas bloquearía siempre. `nombres_materias_asociadas()` une las `Materia` con horas > 0 en `ActividadFormativaMateria` y las `Materia` de las `AsignaturaPrograma` con horas > 0 en `ActividadFormativaAsignaturaPrograma`.
- **Chequeo de dos tablas, a diferencia de `MetodologiaDocente`**: no hay aquí un guard que garantice que el uso en `AsignaturaPrograma` implica el uso en la `Materia` padre, así que se comprueban las dos.
- **Al borrar, se retiran antes las filas a 0 de asociación** de ambas tablas, para no dejar FKs colgando; solo se llega ahí sin filas en uso.
- **Desbloqueo**: poner las horas a 0 en esas `Materia`/`AsignaturaPrograma` (vía `editarActividadesFormativasMateria()`/`editarActividadesFormativasAsignaturaPrograma()`) habilita el borrado.
- **`204 No Content` para el `DELETE`**; la Vista refresca el listado.
- **La rama "cancelada" no genera llamada HTTP**.
- **`404` si el identificador no existe** -- guardia de Router.
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de `Admin`, sin pertenencia que verificar (sin `get_current_director_programa_id`). El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor. Especialmente relevante por ser endpoint de borrado.
- **Sin capa Service**: Router delgado -> Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).

## Referencias

- [`eliminarActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/eliminarActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarActividadFormativa/README.md).
- [`eliminarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md) -- clúster plantilla.
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- mismo patrón de `<<choice>>` bloqueante con borrado físico y `detail` con nombres.
- [`eliminarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignatura/README.md) -- contraste: borrado lógico sin `<<choice>>`.

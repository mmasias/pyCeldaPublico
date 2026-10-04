<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarSistemaEvaluacion() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarSistemaEvaluacion/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`eliminarSistemaEvaluacion()`](/RUP/02-analisis/casos-uso/eliminarSistemaEvaluacion/README.md): `<<choice>>` bloqueante -- borrado físico de la composición de la `Materia`, bloqueado si alguna `PonderacionEvaluacion` usa el sistema (`PonderacionEvaluacion --> SistemaEvaluacion`, desde la `Guia`). `SistemaEvaluacion` no tiene `estado` propio: vive y muere con la `Materia` que lo contiene, su borrado es siempre físico.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarSistemaEvaluacion/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarSistemaEvaluacion` (React, ruta `/admin/sistemas-evaluacion/:id/eliminar`) -- fases cargando/confirmando/bloqueada; carga la información con `GET /api/v1/sistemas-evaluacion/{id}` y pide confirmar/cancelar; si la confirmación recibe `409`, presenta la rama bloqueada con el `detail` tal cual.
- **API**: `routers/sistema_evaluacion.py::eliminar_sistema_evaluacion(sistema_evaluacion_id)` -- función suelta, un único endpoint que resuelve el `<<choice>>` y el borrado.
- **Modelo**: ninguno con lógica propia invocada -- sin `estado` propio que mutar, el borrado es físico (a diferencia de `Asignatura.extinguir()`).
- **Repositorio**: `SistemaEvaluacionRepository.nombres_asignaciones(sistema_evaluacion_id)` (`PonderacionEvaluacion` -> `Guia` -> `AsignaturaPrograma`, `DISTINCT` de nombres ordenados, formateados `AsignaturaPrograma '{nombre}'`) / `.eliminar(sistema_evaluacion_id)`.

## Decisiones de diseño

- **Un solo endpoint, sin `GET` de chequeo previo** (patrón `eliminarMetodologiaDocente()`, no `eliminarResultadoAprendizaje()`): el `<<choice>>` se resuelve dentro del propio `DELETE` -- lista vacía procede al borrado (`204`), lista no vacía devuelve `409` con el `detail` `SistemaEvaluacion en uso en: AsignaturaPrograma '{nombre}', ...`. La Vista presenta la confirmación con la información del `GET` de detalle y la rama bloqueada aparece al confirmar. La invariante queda protegida en el servidor aunque un cliente dispare el `DELETE` a ciegas: el endpoint reconsulta antes de borrar.
- **Nombres de `AsignaturaPrograma`, no conteo (issue #581)**: como `desasociarResultadoAprendizaje()` (`nombres_asignaciones()`), el `detail` nombra las `AsignaturaPrograma` que bloquean, sin repetidas (`DISTINCT`) y ordenadas por nombre. Una `Guia` sin `AsignaturaPrograma` queda fuera por el `INNER JOIN`.
- **`204 No Content` para el `DELETE`**: borrado físico, no hay entidad que devolver -- la Vista refresca el listado.
- **La rama "cancelada" no genera llamada HTTP**: la cancelación cierra el diálogo en el cliente -- se modela como rama del `alt` para reflejar las tres salidas de Análisis (verde/roja/azul), pero sin tocar el backend.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** -- especialmente relevante por ser endpoint de borrado (historial IDOR #86/#96).
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`eliminarSistemaEvaluacion()` en Análisis](/RUP/02-analisis/casos-uso/eliminarSistemaEvaluacion/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarSistemaEvaluacion/README.md).
- [`eliminarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md) -- patrón directo: endpoint único sin chequeo previo; allí el `detail` lista nombres, aquí cuenta.
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- contraste: allí con `GET` de chequeo previo.

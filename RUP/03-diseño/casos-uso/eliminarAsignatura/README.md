<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > eliminarAsignatura() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarAsignatura/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`eliminarAsignatura()`](/RUP/02-analisis/casos-uso/eliminarAsignatura/README.md): borrado lógico, sin `<<choice>>` bloqueante. El modelo de dominio cierra que `Asignatura` nunca se borra físicamente -- usa `estado` (Vigente/Extinguido), que bloquea altas nuevas en `AsignaturaGrado` pero preserva lo existente para no romper `Guia` históricas. Un único endpoint `DELETE` que siempre tiene éxito si el recurso existe, con `alt` de dos ramas (verde/azul) para las dos salidas de Análisis.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarAsignatura/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarAsignaturaView` (React) -- presenta la información y pide confirmar/cancelar directamente, sin consulta previa de bloqueo (a diferencia de `EliminarFacultadView`, que primero pregunta si hay `Grado` asociados).
- **API**: `routers/asignatura.py::eliminar_asignatura(asignatura_id)` -- función suelta, un único endpoint.
- **Modelo**: `Asignatura.extinguir()` -- método nuevo: pasa `estado` a `Extinguido`; invocado solo desde aquí, nunca desde la edición.
- **Repositorio**: `AsignaturaRepository.obtener(asignatura_id)` (reutilizado) / `.actualizar(asignatura)` (reutilizado de `editarAsignatura()`) -- la entidad sigue existiendo, ningún borrado físico.

## Decisiones de diseño

- **`200 OK` con `AsignaturaResponse` (estado: `"Extinguido"`), no `204 No Content`** -- decisión explícita: a diferencia de `eliminarFacultad()`/`eliminarResultadoAprendizaje()` (borrado físico, `204 No Content`, nada que devolver), aquí el recurso sigue existiendo con un campo mutado -- devolver el objeto actualizado es más útil para que la Vista refresque sin una segunda petición, y es semánticamente más preciso que un `204` que sugeriría que el recurso desapareció.
- **Sin rama de bloqueo/`409` ni endpoint de chequeo**: a diferencia de `eliminarFacultad()` (dos endpoints: `GET /tiene-grados-asociados` + `DELETE`), aquí no hay `<<choice>>` que aplicar -- el `DELETE` siempre tiene éxito si el recurso existe; el único fallo posible es la cancelación del propio actor. Sin `AsignaturaController.puedeEliminar()` y sin `AsignaturaRepository.eliminar()`: no existen.
- **La rama "cancelada" no genera llamada HTTP**: la cancelación cierra el diálogo en el cliente -- se modela como segunda rama del `alt` para reflejar las dos salidas de Análisis (verde/azul), pero sin tocar el backend.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio, no se modela como rama del diagrama porque desde el listado solo se alcanzan identificadores existentes.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py` (bloque anterior, ya mergeado), sin nota de pendiente. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.
- **Sin capa Service**: Router delgado -> Modelo/Repository.

## Referencias

- [`eliminarAsignatura()` en Análisis](/RUP/02-analisis/casos-uso/eliminarAsignatura/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignatura/README.md).
- [`eliminarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md) -- contraste: borrado físico con `<<choice>>`, dos endpoints y `204`.
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- otro contraste de borrado físico.
- [`editarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md) -- el otro caso de uso que muta `Asignatura`, siempre sin tocar `estado`.
- [`abrirAsignaturas()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignaturas/README.md) -- listado que ofrece `[Eliminar]` por fila, punto de invocación.

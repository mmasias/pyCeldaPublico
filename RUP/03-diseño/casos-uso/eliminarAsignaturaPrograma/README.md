<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`eliminarAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/eliminarAsignaturaPrograma/README.md): borrado lógico, sin `<<choice>>` bloqueante -- mismo patrón exacto que `eliminarPrograma()`. El modelo de dominio cierra que `AsignaturaPrograma` nunca se borra físicamente -- usa `estado` (Vigente/Extinguido), que bloquea altas nuevas apoyadas en ella pero preserva lo existente para no romper `Guia` históricas. Un único endpoint `DELETE` que siempre tiene éxito si el recurso existe, con `alt` de dos ramas (verde/azul) para las dos salidas de Análisis. `AsignaturaPrograma` gana aquí su método `extinguir()`. Se dispara desde la tabla embebida de la ficha del `Programa` (variante Admin de `abrirPrograma()`), con pantalla de confirmación dedicada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarAsignaturaProgramaAdmin.tsx` (React, ruta `/admin/asignaturas-programa/{id}/eliminar`) -- presenta la información y pide confirmar/cancelar directamente, sin consulta previa de bloqueo; vuelve a la ficha del `Programa` tras confirmar o cancelar.
- **API**: `routers/asignatura_programa.py::eliminar_asignatura_programa(asignatura_programa_id)` -- función suelta, un único endpoint.
- **Modelo**: `AsignaturaPrograma.extinguir()` -- método nuevo: pasa `estado` a `Extinguido`; invocado solo desde aquí, nunca desde la edición.
- **Repositorio**: `AsignaturaProgramaRepository.obtener(asignatura_programa_id)` (reutilizado) / `.actualizar(asignatura_programa)` (reutilizado de `editarAsignaturaPrograma()`) -- la entidad sigue existiendo, ningún borrado físico.

## Decisiones de diseño

- **`200 OK` con `AsignaturaProgramaResponse` (estado: `"Extinguido"`), no `204 No Content`** -- mismo criterio explícito que `eliminarPrograma()`/`eliminarAsignatura()`: el recurso sigue existiendo con un campo mutado. Aquí además la respuesta resuelve la vuelta: lleva el `programa_id` (propiedad derivada de la `Materia`) que la pantalla de confirmación necesita para navegar de vuelta a la ficha del `Programa`.
- **Sin rama de bloqueo/`409` ni endpoint de chequeo**: no hay `<<choice>>` que aplicar -- el `DELETE` siempre tiene éxito si el recurso existe; el único fallo posible es la cancelación del propio actor. Sin `puedeEliminar()`.
- **Pantalla de confirmación dedicada, no acción inline**: el wireframe reserva una vista propia con el aviso naranja ("Esta acción no se puede deshacer") y la explicación de qué implica `Extinguido` -- misma granularidad que `EliminarProgramaView`, a diferencia de `eliminarFacultad()`/`eliminarPrograma()` en listado que sí operan inline.
- **La fila llega por estado de navegación, sin endpoint Admin de detalle individual**: la única entrada del CU es el `[Eliminar]` de la tabla embebida de `abrirPrograma()`, que ya tiene el objeto `AsignaturaProgramaResponse` cargado; la Vista lo pasa como estado de la ruta. No se crea un `GET /api/v1/admin/asignaturas-programa/{id}` solo para esta pantalla -- el `programa_id` de la vuelta llega en la respuesta del `DELETE`, así la confirmación funciona incluso en recarga directa.
- **La rama "cancelada" no genera llamada HTTP**: se modela como segunda rama del `alt` para reflejar las dos salidas de Análisis (verde/azul), pero sin tocar el backend.
- **`404` si el identificador no existe** -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de escritura, guard explícito por el historial IDOR (#86/#96).

## Referencias

- [`eliminarAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/eliminarAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarAsignaturaPrograma/README.md) -- fuente de verdad de las dos ramas y del aviso de extinción.
- [`eliminarPrograma()` en Diseño](/RUP/03-diseño/casos-uso/eliminarPrograma/README.md) -- mismo patrón exacto de borrado lógico con `200` y sin bloqueo, el precedente directo de la rebanada anterior.
- [`crearAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaPrograma/README.md) -- la otra acción sobre la misma tabla embebida, construida en este mismo lote.
- [`abrirPrograma()` en Diseño](/RUP/03-diseño/casos-uso/abrirPrograma/README.md) -- la tabla embebida desde la que se dispara, con su variante Admin documentada en este mismo lote.

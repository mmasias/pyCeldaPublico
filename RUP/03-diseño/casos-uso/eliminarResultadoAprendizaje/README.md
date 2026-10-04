<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > eliminarResultadoAprendizaje() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/eliminarResultadoAprendizaje/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-19
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`eliminarResultadoAprendizaje()`](/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/README.md): `<<choice>>` bloqueante -- borrado físico del catálogo del `Programa`, bloqueado si el `ResultadoAprendizaje` está asignado a alguna `Materia` o `AsignaturaPrograma` (los dos niveles de la cascada, cubiertos en una sola consulta). A diferencia de `eliminarPonderacionEvaluacion()`/`eliminarReferenciaBibliografica()` (mutación de lista de trabajo del cliente, sin backend), aquí sí hay endpoint: la comprobación de bloqueo y el borrado son de servidor.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarResultadoAprendizajeView` (React) -- pide el estado de asignación antes de abrir la confirmación; en la rama bloqueada presenta el motivo sin diálogo.
- **API**: `routers/resultado_aprendizaje.py::esta_asignado(resultado_aprendizaje_id)` / `::eliminar_resultado_aprendizaje(resultado_aprendizaje_id)` -- dos funciones sueltas.
- **Modelo**: ninguno con lógica propia invocada -- sin `estado` propio que mutar, el borrado es físico.
- **Repositorio**: `ResultadoAprendizajeRepository.esta_asignado(resultado_aprendizaje_id)` (un `SELECT EXISTS` con joins a las dos tablas de asociación) / `.eliminar(resultado_aprendizaje_id)`.

## Decisiones de diseño

- **Dos endpoints, no uno**: el `<<choice>>` de Análisis (`puedeEliminar()` antes de `eliminar()`) exige conocer el bloqueo ANTES de presentar la confirmación -- un único `DELETE` que respondiera 409 obligaría a la Vista a abrir el diálogo a ciegas. El chequeo es un `GET` barato que decide si la fila ofrece `[Eliminar]` operativo o el motivo de bloqueo.
- **Ruta de chequeo `/esta-asignado`**: pregunta literal de negocio, misma familia que `existe_pendiente_de()`/`existe_alguna_de()` ya usadas en el hilo `Guia` -- nombre de método en el Repository, subrecurso en la URL.
- **204 No Content para el `DELETE`**: no hay entidad que devolver -- la Vista refresca el listado (el estado bloqueado de otras filas no cambia con esta eliminación).
- **La rama "cancelada" no genera llamada HTTP**: la cancelación cierra el diálogo en el cliente -- se modela como tercera rama del `alt` para reflejar las tres salidas de Análisis (verde/roja/azul), pero sin tocar el backend.
- **Autorización: Director del Programa o Admin**: el endpoint es el mismo para ambos actores (sin espejo `/api/v1/admin/...`). El router resuelve la identidad con `get_current_director_programa_id_opcional` y `get_current_admin_email_opcional` y autoriza con `_verificar_resultado_del_director` (que delega en `_verificar_programa_del_director_o_admin`): con sesión Admin no exige dirigir el `Programa`; sin Admin, un `Programa` que no se dirige (o inexistente) responde 404 uniforme, sin distinguir "no existe" de "no es tuyo" (en los endpoints por resultado, el 404 es el de `ResultadoAprendizaje no encontrado`). La Vista de Admin es una pantalla propia (`*Admin.tsx`) sobre la misma llamada.

## Referencias

- [`eliminarResultadoAprendizaje()` en Análisis](/RUP/02-analisis/casos-uso/eliminarResultadoAprendizaje/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarResultadoAprendizaje/README.md).
- [`enviarGuiaARevision()` en Diseño](/RUP/03-diseño/casos-uso/enviarGuiaARevision/README.md) -- precedente de rama bloqueante con 409.
- [`eliminarPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/eliminarPonderacionEvaluacion/README.md) -- contraste: eliminación sin backend (lista de trabajo del cliente).

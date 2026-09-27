<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > eliminarFacultad() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/eliminarFacultad/README.md)|[Análisis](/RUP/02-analisis/casos-uso/eliminarFacultad/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`eliminarFacultad()`](/RUP/02-analisis/casos-uso/eliminarFacultad/README.md): `<<choice>>` bloqueante -- borrado físico de la `Facultad`, bloqueado si tiene `Grado`s asociados (`Facultad *-d- Grado`, composición: primero se eliminan o reubican los Grados). Mismo patrón de dos endpoints que `eliminarResultadoAprendizaje()`: la comprobación de bloqueo y el borrado son de servidor, con `alt` de tres ramas (verde/roja/azul) para las tres salidas de Análisis.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/eliminarFacultad/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EliminarFacultadView` (React) -- pide el estado de asociación antes de abrir la confirmación; en la rama bloqueada presenta el motivo sin diálogo de confirmación.
- **API**: `routers/facultad.py::tiene_grados_asociados(facultad_id)` / `::eliminar_facultad(facultad_id)` -- dos funciones sueltas.
- **Modelo**: ninguno con lógica propia invocada -- `Facultad` se borra físicamente, sin `estado` propio que mutar.
- **Repositorio**: `FacultadRepository.tiene_grados_asociados(facultad_id)` (un `SELECT EXISTS` sobre `grados`) / `.eliminar(facultad_id)`.

## Decisiones de diseño

- **Dos endpoints, no uno**: el `<<choice>>` de Análisis (`puedeEliminar()` antes de `eliminar()`) exige conocer el bloqueo ANTES de presentar la confirmación -- un único `DELETE` que respondiera 409 obligaría a la Vista a abrir el diálogo a ciegas. El chequeo es un `GET` barato que decide si la fila ofrece `[Eliminar]` operativo o el motivo de bloqueo.
- **Ruta de chequeo `/tiene-grados-asociados`**: pregunta literal de negocio, misma familia que `/esta-asignado` de `eliminarResultadoAprendizaje()` -- nombre de método en el Repository, subrecurso en la URL.
- **204 No Content para el `DELETE`**: no hay entidad que devolver -- la Vista refresca el listado (el estado bloqueado de otras filas no cambia con esta eliminación).
- **La rama "cancelada" no genera llamada HTTP**: la cancelación cierra el diálogo en el cliente -- se modela como tercera rama del `alt` para reflejar las tres salidas de Análisis (verde/roja/azul), pero sin tocar el backend.
- **La consulta de bloqueo (`tiene_grados_asociados`) depende de la columna `facultad_id` en `grados`** -- ver la migración descrita en [`crearFacultad()`](/RUP/03-diseño/casos-uso/crearFacultad/README.md), no repetida aquí.
- **Autorización de `Admin`: `Depends(require_admin)`** (dependencia fijada en el diseño de [`iniciarSesion()`](/RUP/03-diseño/casos-uso/iniciarSesion/README.md), no implementada en este documento) -- aplica a los dos endpoints de este CU (`GET` de chequeo y `DELETE`). Especialmente relevante aquí por ser endpoint de escritura/borrado: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`eliminarFacultad()` en Análisis](/RUP/02-analisis/casos-uso/eliminarFacultad/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/eliminarFacultad/README.md).
- [`eliminarResultadoAprendizaje()` en Diseño](/RUP/03-diseño/casos-uso/eliminarResultadoAprendizaje/README.md) -- patrón de dos endpoints con `alt` de tres ramas.
- [`crearFacultad()` en Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md) -- migración de `Grado.facultad_id` de la que depende el chequeo de bloqueo.
- [`abrirFacultades()` en Diseño](/RUP/03-diseño/casos-uso/abrirFacultades/README.md) -- listado que ofrece `[Eliminar]` por fila, punto de invocación.

<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > abrirGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirGrado()`](/RUP/02-analisis/casos-uso/abrirGrado/README.md), en sus dos variantes, ambas de un solo paso y solo lectura. La `Admin` es "la misma ficha" (`GradoAdmin.tsx`, en producción desde el lote de Grado vía `GET /api/v1/admin/grados/{grado_id}`) **más** el agregado del lote de Materia/AsignaturaGrado: la tabla embebida de `AsignaturaGrado` (con `[Eliminar]` activo y `[Abrir]` deshabilitado), el botón `+ Crear AsignaturaGrado` y el enlace "Ver Materias" -- los tres exclusivos de `Admin`. Sin cambio en este retoque.

**`DirectorGrado` -- retocada (2026-09-05, Manuel usando el producto)**: presentaba los datos propios del `Grado` y su tabla de `AsignaturaGrado` (agregación de lectura con dos consultas, mismo mecanismo que `abrirGuia()`); pasa a presentar los datos propios del `Grado` y el listado de `Guia` -- ahora dos `GET` reales en serie desde la Vista (antes uno agregando `AsignaturaGrado` server-side; el segundo `GET` es el mismo endpoint ya existente que usa [`consultarEstadoGuias()`](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md), reutilizado tal cual). Sin backend nuevo.

Este `secuencia.puml` contiene **dos diagramas**: el primero (`abrirGrado-diseño`) es la variante `DirectorGrado`; el segundo (`abrirGrado-admin-diseño`) es la variante `Admin` -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirGrados()`](../abrirGrados/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|`DirectorGrado` (`/api/v1/grados/{grado_id}` + `.../guias`)|`Admin` (`/api/v1/admin/grados/{grado_id}` + tabla embebida)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/abrirGrado/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/abrirGrado/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Variante DirectorGrado (retocada, 2026-09-05)

- **Vista**: `AbrirGradoView` (`frontend/src/pages/Grado.tsx`) -- `Promise.all` de `GET /api/v1/grados/{grado_id}` (ficha: `codigo`, `nombre`, `estado`) y `GET /api/v1/grados/{grado_id}/guias` (listado de `Guia`: `AsignaturaGrado`, profesorado, estado, última actualización, botón `Notificar guías actualizadas`) -- antes `GET /api/v1/grados/{grado_id}/asignaturas-grado`. El segundo endpoint es el mismo que ya usa [`consultarEstadoGuias()`](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) (`ConsultarEstadoGuias.tsx`) -- reutilizado tal cual, sin backend nuevo.
- **API**: `routers/grado.py::obtener_grado(grado_id)` (sin cambio) / `routers/guia.py::listar_guias_del_grado(grado_id)` (reutilizado, antes solo consumido por `consultarEstadoGuias()`); guard de `DirectorGrado` en ambos.
- **Modelo**: ninguno con lógica propia invocada -- `Grado` y `Guia` portan los datos presentados.
- **Repositorio**: `GradoRepository.obtener(grado_id)` / `GuiaRepository.listar_del_grado(grado_id)` -- el segundo, antes `AsignaturaGradoRepository.listar_del_grado(grado_id)`.

### Variante Admin

- **Vista**: `GradoAdmin.tsx` (React, ruta `/admin/grados/{grado_id}`) -- `Promise.all` de `GET /api/v1/admin/grados/{grado_id}` (ficha: `codigo`, `nombre`, `estado`, botones `Editar`/`Eliminar`/`Volver`) y `GET /api/v1/admin/grados/{grado_id}/asignaturas-grado` (tabla embebida: asignatura, materia, curso, carácter, estado, `[Abrir]` deshabilitado en esta rebanada, `[Eliminar]` activo hacia `EliminarAsignaturaGradoAdmin.tsx`); más el botón `+ Crear AsignaturaGrado` (hacia `CrearAsignaturaGradoAdmin.tsx`) y el enlace "Ver Materias" (hacia `MateriasAdmin.tsx`).
- **API**: `routers/grado.py::obtener_grado_admin(grado_id)` (existente desde el lote de Grado) / `routers/asignatura_grado.py::listar_asignaturas_grado_admin(grado_id)` -- función nueva; ambos con `Depends(require_admin)`.
- **Modelo**: ninguno con lógica propia invocada -- `Grado` y `AsignaturaGrado` portan los datos presentados.
- **Repositorio**: `GradoRepository.obtener(grado_id)` / `AsignaturaGradoRepository.listar_del_grado(grado_id)` -- ambos reutilizados tal cual.

## Decisiones de diseño

- **DirectorGrado -- se reemplaza la fuente de la segunda consulta, no se cambia el patrón**: seguía siendo `Promise.all` de dos `GET` (antes `GradoDetalleResponse` + `AsignaturaGradoConEstadoGuiaResponse[]`, ahora `GradoDetalleResponse` + `GuiaResumenResponse[]`) -- mismo mecanismo, sin backend nuevo. El campo `asignaturas_grado` que ya embebía `GradoDetalleResponse` server-side sigue existiendo en el schema (sin tocar) pero deja de pintarse en esta pantalla -- no era la fuente real de la tabla ni antes ni ahora (la tabla siempre vino del segundo `GET`, agregado en el Router de un modo que este mismo diagrama documentaba de forma imprecisa antes de este retoque: como un único endpoint agregado, cuando en realidad ya eran dos llamadas desde la Vista -- corregido de camino al redibujar este bloque).
- **Segundo `GET` reutilizado tal cual de `consultarEstadoGuias()`**: sin variante nueva de endpoint, sin parámetro nuevo -- mismo `GuiaRepository.listar_del_grado(grado_id)`, mismo `GuiaResumenResponse`.
- **Admin -- sin cambio.** Dos `GET` en paralelo en la Vista, no un endpoint agregado: el endpoint `GET /api/v1/admin/grados/{grado_id}` existía plano (`GradoResponse`) desde el lote de Grado -- se reutiliza tal cual y la tabla embebida se pide aparte (`GET /api/v1/admin/grados/{grado_id}/asignaturas-grado`), que la Vista lanza en el mismo `useEffect` vía `Promise.all`. No se introduce un `GradoDetalleResponse` Admin: la ficha Admin nunca necesitó el agregado hasta ahora y el listado suelto sirve además a otras pantallas.
- **Admin -- filas planas, sin profesorado ni estado de `Guia`**: a diferencia del listado de `Guia` que ahora consume `DirectorGrado`, la variante Admin sigue usando `AsignaturaGradoResponse` sobre su propia tabla de `AsignaturaGrado` -- `Admin` no gestiona `Guia` ni profesorado desde esta pantalla; añadirlo sería acarrear joins que nadie pinta.
- **`[Abrir]` por fila deshabilitado (Admin)**: la variante Admin de `abrirAsignaturaGrado()` no se construye en esta rebanada -- el botón se renderiza con `title="Fuera de alcance de esta rebanada"`.

## Referencias

- [`abrirGrado()` en Análisis](/RUP/02-analisis/casos-uso/abrirGrado/README.md) -- diagrama de colaboración origen, con ambas variantes.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirGrado/README.md).
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- precedente de agregado de lectura con varias consultas.
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- origen del segundo `GET`/`GuiaRepository.listar_del_grado()` que la variante DirectorGrado reutiliza aquí; caso de uso propio, sin fusionar.
- [`crearAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaGrado/README.md) / [`eliminarAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaGrado/README.md) -- las dos acciones exclusivas de Admin que esa tabla embebe, sin cambio.
- [`abrirMaterias()` en Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md) -- destino del enlace "Ver Materias" en la variante Admin, sin cambio.
- [PR #235](https://github.com/mmasias/pyCelda/pull/235) -- precedente del patrón de divergencia Admin/DirectorGrado aplicado aquí.

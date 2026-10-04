<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > abrirPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/abrirPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-25
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`abrirPrograma()`](/RUP/02-analisis/casos-uso/abrirPrograma/README.md), en sus dos variantes, ambas de un solo paso y solo lectura. La `Admin` es "la misma ficha" (`ProgramaAdmin.tsx`, en producción desde el lote de Programa vía `GET /api/v1/admin/programas/{programa_id}`) **más** el agregado del lote de Materia/AsignaturaPrograma: la tabla embebida de `AsignaturaPrograma` (con `[Eliminar]` activo y `[Abrir]` deshabilitado), el botón `+ Crear AsignaturaPrograma` y el enlace "Ver Materias" -- los tres exclusivos de `Admin`. Sin cambio en este retoque.

**`DirectorPrograma` -- retocada (2026-09-05, Manuel usando el producto)**: presentaba los datos propios del `Programa` y su tabla de `AsignaturaPrograma` (agregación de lectura con dos consultas, mismo mecanismo que `abrirGuia()`); pasa a presentar los datos propios del `Programa` y el listado de `Guia` -- ahora dos `GET` reales en serie desde la Vista (antes uno agregando `AsignaturaPrograma` server-side; el segundo `GET` es el mismo endpoint ya existente que usa [`consultarEstadoGuias()`](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md), reutilizado tal cual). Sin backend nuevo.

Este `secuencia.puml` contiene **dos diagramas**: el primero (`abrirPrograma-diseño`) es la variante `DirectorPrograma`; el segundo (`abrirPrograma-admin-diseño`) es la variante `Admin` -- mismo criterio de troceo que `secuencia.puml` de `iniciarSesion()` y de la variante Admin de [`abrirProgramas()`](../abrirProgramas/README.md).

## Diagrama de secuencia de diseño

<div align=center>

|`DirectorPrograma` (`/api/v1/programas/{programa_id}` + `.../guias`)|`Admin` (`/api/v1/admin/programas/{programa_id}` + tabla embebida)|
|:-:|:-:|
|![](/images/RUP/03-diseño/casos-uso/abrirPrograma/secuencia.svg)|![](/images/RUP/03-diseño/casos-uso/abrirPrograma/secuencia-admin.svg)|
|<sup>Código fuente: [secuencia.puml](secuencia.puml)</sup>|<sup>mismo fichero, segundo bloque `@startuml`</sup>|

</div>

## Participantes

### Variante DirectorPrograma (retocada, 2026-09-05)

- **Vista**: `AbrirProgramaView` (`frontend/src/pages/Programa.tsx`) -- `Promise.all` de `GET /api/v1/programas/{programa_id}` (ficha: `codigo`, `nombre`, `estado`) y `GET /api/v1/programas/{programa_id}/guias` (listado de `Guia`: `AsignaturaPrograma`, profesorado, estado, última actualización, botón `Notificar guías actualizadas`) -- antes `GET /api/v1/programas/{programa_id}/asignaturas-programa`. El segundo endpoint es el mismo que ya usa [`consultarEstadoGuias()`](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) (`ConsultarEstadoGuias.tsx`) -- reutilizado tal cual, sin backend nuevo.
- **API**: `routers/programa.py::obtener_programa(programa_id)` (sin cambio) / `routers/guia.py::listar_guias_del_programa(programa_id)` (reutilizado, antes solo consumido por `consultarEstadoGuias()`); guard de `DirectorPrograma` en ambos.
- **Modelo**: ninguno con lógica propia invocada -- `Programa` y `Guia` portan los datos presentados.
- **Repositorio**: `ProgramaRepository.obtener(programa_id)` / `GuiaRepository.listar_del_programa(programa_id)` -- el segundo, antes `AsignaturaProgramaRepository.listar_del_programa(programa_id)`.

### Variante Admin

- **Vista**: `ProgramaAdmin.tsx` (React, ruta `/admin/programas/{programa_id}`) -- `Promise.all` de `GET /api/v1/admin/programas/{programa_id}` (ficha: `codigo`, `nombre`, `estado`, botones `Editar`/`Eliminar`/`Volver`) y `GET /api/v1/admin/programas/{programa_id}/asignaturas-programa` (tabla embebida: asignatura, materia, curso, carácter, estado, `[Abrir]` deshabilitado en esta rebanada, `[Eliminar]` activo hacia `EliminarAsignaturaProgramaAdmin.tsx`); más el botón `+ Crear AsignaturaPrograma` (hacia `CrearAsignaturaProgramaAdmin.tsx`) y el enlace "Ver Materias" (hacia `MateriasAdmin.tsx`).
- **API**: `routers/programa.py::obtener_programa_admin(programa_id)` (existente desde el lote de Programa) / `routers/asignatura_programa.py::listar_asignaturas_programa_admin(programa_id)` -- función nueva; ambos con `Depends(require_admin)`.
- **Modelo**: ninguno con lógica propia invocada -- `Programa` y `AsignaturaPrograma` portan los datos presentados.
- **Repositorio**: `ProgramaRepository.obtener(programa_id)` / `AsignaturaProgramaRepository.listar_del_programa(programa_id)` -- ambos reutilizados tal cual.

## Decisiones de diseño

- **DirectorPrograma -- se reemplaza la fuente de la segunda consulta, no se cambia el patrón**: seguía siendo `Promise.all` de dos `GET` (antes `ProgramaDetalleResponse` + `AsignaturaProgramaConEstadoGuiaResponse[]`, ahora `ProgramaDetalleResponse` + `GuiaResumenResponse[]`) -- mismo mecanismo, sin backend nuevo. El campo `asignaturas_programa` que ya embebía `ProgramaDetalleResponse` server-side sigue existiendo en el schema (sin tocar) pero deja de pintarse en esta pantalla -- no era la fuente real de la tabla ni antes ni ahora (la tabla siempre vino del segundo `GET`, agregado en el Router de un modo que este mismo diagrama documentaba de forma imprecisa antes de este retoque: como un único endpoint agregado, cuando en realidad ya eran dos llamadas desde la Vista -- corregido de camino al redibujar este bloque).
- **Segundo `GET` reutilizado tal cual de `consultarEstadoGuias()`**: sin variante nueva de endpoint, sin parámetro nuevo -- mismo `GuiaRepository.listar_del_programa(programa_id)`, mismo `GuiaResumenResponse`.
- **Admin -- sin cambio.** Dos `GET` en paralelo en la Vista, no un endpoint agregado: el endpoint `GET /api/v1/admin/programas/{programa_id}` existía plano (`ProgramaResponse`) desde el lote de Programa -- se reutiliza tal cual y la tabla embebida se pide aparte (`GET /api/v1/admin/programas/{programa_id}/asignaturas-programa`), que la Vista lanza en el mismo `useEffect` vía `Promise.all`. No se introduce un `ProgramaDetalleResponse` Admin: la ficha Admin nunca necesitó el agregado hasta ahora y el listado suelto sirve además a otras pantallas.
- **Admin -- filas planas, sin profesorado ni estado de `Guia`**: a diferencia del listado de `Guia` que ahora consume `DirectorPrograma`, la variante Admin sigue usando `AsignaturaProgramaResponse` sobre su propia tabla de `AsignaturaPrograma` -- `Admin` no gestiona `Guia` ni profesorado desde esta pantalla; añadirlo sería acarrear joins que nadie pinta.
- **`[Abrir]` por fila deshabilitado (Admin)**: la variante Admin de `abrirAsignaturaPrograma()` no se construye en esta rebanada -- el botón se renderiza con `title="Fuera de alcance de esta rebanada"`.

## Referencias

- [`abrirPrograma()` en Análisis](/RUP/02-analisis/casos-uso/abrirPrograma/README.md) -- diagrama de colaboración origen, con ambas variantes.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/abrirPrograma/README.md).
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- precedente de agregado de lectura con varias consultas.
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- origen del segundo `GET`/`GuiaRepository.listar_del_programa()` que la variante DirectorPrograma reutiliza aquí; caso de uso propio, sin fusionar.
- [`crearAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignaturaPrograma/README.md) / [`eliminarAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaPrograma/README.md) -- las dos acciones exclusivas de Admin que esa tabla embebe, sin cambio.
- [`abrirMaterias()` en Diseño](/RUP/03-diseño/casos-uso/abrirMaterias/README.md) -- destino del enlace "Ver Materias" en la variante Admin, sin cambio.
- [PR #235](https://github.com/mmasias/pyCelda/pull/235) -- precedente del patrón de divergencia Admin/DirectorPrograma aplicado aquí.

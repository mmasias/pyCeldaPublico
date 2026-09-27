<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > consultarEstadoGuias() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/README.md)|[Análisis](/RUP/02-analisis/casos-uso/consultarEstadoGuias/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/consultarEstadoGuias/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-18
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`consultarEstadoGuias()`](/RUP/02-analisis/casos-uso/consultarEstadoGuias/README.md): `GET /api/v1/grados/{grado_id}/guias`, primer endpoint de listado agregado por `Grado` de toda la rebanada -- a diferencia de las lecturas independientes por colección de `abrirGuia()`, aquí una única consulta con joins recorre `Grado -> Materia -> AsignaturaGrado -> Guia` del `CursoAcademico` activo, porque no hay una `Guia` ya identificada de la que partir.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/consultarEstadoGuias/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ConsultarEstadoGuias.tsx` (`DirectorGrado`, `/grados/:id/guias`) y `ConsultarEstadoGuiasAdmin.tsx` (`Admin`, `/admin/grados/:id/guias` -- gemela de `MateriaAdmin`/`AsignaturaGradoAdmin`, issue [#262](https://github.com/mmasias/pyCelda/issues/262)). Las dos pintan el listado con el componente compartido `components/ListaGuiasDelGrado.tsx`, que gana un prop `modo` (`"director"` | `"admin"`).
- **API**: `routers/guia.py::listar_guias_del_grado(grado_id)` -- gate ampliado a `admin_email is not None or GradoRepository.dirige(grado_id, director_grado_id)` (deps `_opcional` de Admin + DirectorGrado), `404` uniforme -- patrón exacto de `descargar_guia_pdf` (#238/#220) y `previsualizar_guia` (#262). Un único camino de servidor; la variante de fila es de la Vista.
- **Modelo**: `Guia.tiene_pdf_generado()` -- reutilizada (ya la usa `descargarGuiaPDF()`), para el campo `tiene_pdf` del resumen.
- **Repositorio**: `GuiaRepository.listar_del_grado(grado_id)` -- sin cambio; ya carga la cascada que el resumen necesita.

## Decisiones de diseño

- **Una sola consulta con joins, no N+1**: a diferencia de `abrirGuia()` (lecturas independientes por colección, reflejando las colaboraciones de Análisis), aquí no hay una `Guia` de partida -- el listado completo del `Grado` se resuelve con una única consulta que junta `guias`, `asignaturas_grado`, `materias` y filtra por `curso_academico_id` activo.
- **`routers/guia.py`, no un router nuevo de `Grado`**: aunque la URL cuelga de `/grados/{grado_id}`, el recurso gestionado es `Guia` -- no se introduce un módulo `routers/grado.py` para un único endpoint de listado; `Grado` no tiene ningún Modelo propio en esta rebanada.
- **`GuiaResumenResponse`, no `GuiaResponse` completo**: el listado solo necesita `AsignaturaGrado`, profesorado y `estado` por fila -- un schema de respuesta más ligero que el de `abrirGuia()`, sin las colecciones de Evaluación/Bibliografía. Con #262 gana `tiene_pdf: bool` (`guia.tiene_pdf_generado()`): la única fila que lo consume es la de `Admin`, para deshabilitar `[Descargar PDF]` con motivo en vez de dejar que muestre el `409` de `/pdf`.
- **El gate se traduce en dep opcional + guard, no en dos endpoints** (issue [#262](https://github.com/mmasias/pyCelda/issues/262)): `listar_guias_del_grado` pasa de `get_current_director_grado_id` (hard, 403 al Admin) a `get_current_director_grado_id_opcional` + `get_current_admin_email_opcional` + `admin_email is not None or GradoRepository.dirige(...)`. Mismo movimiento que #263 hizo con `previsualizar_guia` y #238 con `descargar_guia_pdf`. Un `Admin` ve las guías de cualquier grado; un `DirectorGrado`, solo las suyas; cualquier otro, `404`.
- **`ListaGuiasDelGrado` con prop `modo`, no un componente por actor**: el JSX del listado ya está compartido entre `abrirGrado()` y `consultarEstadoGuias()` (`DirectorGrado`); `modo` añade la tercera variante (`Admin`) sin duplicarlo. En `modo="admin"` la fila cambia `[Abrir]` por `[Previsualizar]` + `[Descargar PDF]` (deshabilitado si `!tiene_pdf`) y se oculta el botón `[Notificar guías actualizadas]` -- todo presentación de la Vista, el endpoint no cambia.
- **Forward-compat con `CursoAcademico` (#222)**: la ruta `/admin/grados/:gradoId/guias` y la firma de `listar_guias_del_grado` se piensan sabiendo que va a venir un `?curso=` opcional (por defecto el vigente), sin construirlo ahora. El `<h2>` de la pantalla de `Admin` rotula "curso actual" (sin año hasta que #222 modele `CursoAcademico`; `CURSO_ACADEMICO_VIGENTE` está en config pero no expuesto al frontend hoy).
- **Profesorado en vivo (issue [#254](https://github.com/mmasias/pyCelda/issues/254))**: la columna de profesorado pasa a leer `guia.asignatura_grado.profesorado`, no `guia.profesorado`. El router deja de devolver las filas `Guia` en crudo (`response_model` con `from_attributes` leería la copia) y construye `GuiaResumenResponse` explícitamente. `GuiaRepository.listar_del_grado()` gana `selectinload(AsignaturaGrado.profesorado)` + `selectinload(Guia.historial)` (evita el N+1 que ya arrastraba `ultima_actualizacion_rol`). Esa propiedad gana además el valor "Administración" para la transición `Aprobada -> EnRevision` con `autor_id == 0`.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`consultarEstadoGuias()` en Análisis](/RUP/02-analisis/casos-uso/consultarEstadoGuias/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarEstadoGuias/README.md).
- [`abrirGuia()` en Diseño](/RUP/03-diseño/casos-uso/abrirGuia/README.md) -- contraste: lecturas independientes por colección en vez de una consulta agregada.
- [`notificarGuiasActualizadas()` en Diseño](/RUP/03-diseño/casos-uso/notificarGuiasActualizadas/README.md) -- self-loop sobre el mismo listado que este caso presenta.

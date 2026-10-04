<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarHistorialCambios() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/README.md)|[Análisis](/RUP/02-analisis/casos-uso/consultarHistorialCambios/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`consultarHistorialCambios()`](/RUP/02-analisis/casos-uso/consultarHistorialCambios/README.md): dos `GET` de solo lectura sobre `HistorialCambio` -- `GET /api/v1/historial-cambios` (feed de las últimas 50 acciones + índice de autores, con `?curso=` opcional) y `GET /api/v1/historial-cambios/autores/{clave}` (historial completo de un autor). Sin repositorio propio: `routers/historial_cambio.py` consulta `HistorialCambio` directamente con la `Session` y reutiliza `CursoAcademicoRepository`/`ProgramaRepository`/`ProfesorRepository` como colaboradores puntuales. Las dos funciones de `HistorialCambioController` convergen en el mismo módulo, funciones sueltas, sin capa Service. Es una vista de **solo lectura**: este caso de uso nunca escribe en `HistorialCambio`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/consultarHistorialCambios/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ConsultarHistorialCambiosView` -- `HistorialCambios.tsx` (`/admin/historial-cambios`: feed + autores + selector de curso) y `HistorialCambiosAutor.tsx` (`/admin/historial-cambios/autores/:clave`: historial de un autor, con columna de rol). Carga en paralelo `GET /api/v1/historial-cambios` y el selector de curso (`GET /api/v1/cursos-academicos`, el de lectura de [`abrirCursosAcademicos()`](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md)); al cambiar de curso, repite el primero con `?curso=`.
- **API**: `routers/historial_cambio.py::consultar_historial_cambios(curso)` / `consultar_historial_cambios_de_autor(clave)`. Helpers: `_clasificar_autor()`, `_email_de()`, `_clave_agrupacion()`, `_resolver_autor()`, `_a_response()`.
- **Modelo**: `HistorialCambio` (solo lectura); `Profesor`, `DirectorPrograma` para resolver al autor; `Guia.curso_academico_id` para el filtro por join.
- **Repositorios**: `CursoAcademicoRepository.obtener(curso)` (`404` si el filtro apunta a un curso inexistente); `ProgramaRepository.obtener(programa_id)` (código del `Programa`); `ProfesorRepository.obtener_por_email(email)` (nombre del `DirectorPrograma`).
- **Schemas**: `HistorialCambiosResponse` (`ultimos` + `autores`), `HistorialCambioResponse`, `AutorHistorialResponse`, `AutorIndiceResponse`.

## Decisiones de diseño

- **`autor_id` no es un único espacio de identificadores** (`_clasificar_autor`): `campo="estado"` con el centinela `AUTOR_ADMIN_CENTINELA` (`0`) es `Admin`; `campo="estado"` con identificador real es `DirectorPrograma.id`; cualquier otro `campo` (`contenido`, `planificacion_docente`, ...) es `Profesor.id`. La tabla de verdad está en la función, no en una columna.
- **Índice de autores fusionado por email normalizado** (`_clave_agrupacion`, issue [#401](https://github.com/mmasias/pyCelda/issues/401)): `Profesor.email` y `DirectorPrograma.email` son `unique`; la misma persona con fila en las dos tablas fusiona en una sola entrada, con clave en minúsculas. `Admin` (sin email) queda aislado con clave literal `"admin"`. Si el `Profesor`/`DirectorPrograma` referenciado ya no existe, se aísla por `tipo:id` -- fallback defensivo, sin fusión posible.
- **`DirectorPrograma` sin `nombre` propio** (issue [#62](https://github.com/mmasias/pyCelda/issues/62)): `_resolver_autor` cruza por email contra `Profesor` y muestra su nombre; si no hay `Profesor` con ese email, muestra el email; si el `DirectorPrograma` ya no existe, `Director #id`.
- **`?curso=` opcional, default opuesto al de `consultarEstadoGuias()`** (issue [#442](https://github.com/mmasias/pyCelda/issues/442)): **sin filtro, histórico completo de todos los cursos**; con él, join `HistorialCambio -> Guia` filtrado por `curso_academico_id`. `404` (`CursoAcademico no encontrado`) si el curso no existe. Otros filtros naturales de una auditoría (profesor, fechas, campo...) quedan fuera a propósito.
- **Feed limitado a 50, con desempate determinista**: `ORDER BY fecha DESC, id DESC LIMIT 50` -- varias filas pueden compartir el mismo `datetime.now(UTC)` si se escriben en el mismo instante; sin el desempate, "más reciente primero" no sería determinista. El índice de autores, en cambio, se calcula sobre **todas** las filas del filtro, no solo sobre las 50 del feed.
- **Historial por autor sin límite ni filtro de curso**: `consultar_historial_cambios_de_autor` carga todas las filas ordenadas y filtra en Python por clave de agrupación. Una clave desconocida **no es `404`**: es una búsqueda con cero resultados (coherente con que la clave es un email, no un identificador validable en la URL). Coste lineal en el tamaño del historial, aceptado -- es una pantalla de auditoría de uso esporádico.
- **Etiquetas de campo en el Router** (`ETIQUETAS_CAMPO`: `estado` -> "Estado", `contenido` -> "Contenido", ...); un `campo` sin etiqueta se devuelve tal cual (p.ej. `bibliografia`, escrito por [`importarBibliografiaDeGuiaHermana()`](/RUP/03-diseño/casos-uso/importarBibliografiaDeGuiaHermana/README.md), hoy sin entrada en el mapa).
- **Columna Guía en texto plano `Asignatura@SiglaPrograma`** (issues [#403](https://github.com/mmasias/pyCelda/issues/403)/[#398](https://github.com/mmasias/pyCelda/issues/398)): `_a_response` carga el `Programa` por fila para la sigla; la tabla no enlaza a `abrirGuia()` -- "este listado tiene como propósito solo mostrar".
- **Sin capa Service**: Router delgado -> `Session`/Repositories (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización de `Admin`: `Depends(require_admin)`** en ambos endpoints -- la auditoría expone qué hizo cada persona; el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`consultarHistorialCambios()` en Análisis](/RUP/02-analisis/casos-uso/consultarHistorialCambios/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/README.md).
- [`consultarEstadoGuias()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoGuias/README.md) -- plantilla de lectura con selector de curso (default opuesto).
- [`consultarCopiasSeguridad()` en Diseño](/RUP/03-diseño/casos-uso/consultarCopiasSeguridad/README.md) -- caso de uso hermano de auditoría de `Admin`.
- [`abrirCursosAcademicos()` en Diseño](/RUP/03-diseño/casos-uso/abrirCursosAcademicos/README.md) -- el selector de curso (`GET /cursos-academicos`) que la Vista reutiliza.

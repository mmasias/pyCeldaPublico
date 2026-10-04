<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearPrograma/README.md)|**Diseño**|[Desarrollo](/RUP/04-desarrollo/casos-uso/crearPrograma/README.md)|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearPrograma()`](/RUP/02-analisis/casos-uso/crearPrograma/README.md): CRUD real e inmediato contra `ProgramaRepository`, sin ninguna capa Service. El formulario de Requisitos pide `codigo` y `nombre`, ambos obligatorios (a diferencia de `crearUniversidad()`, un solo campo; `crearAsignatura()` también pide los dos desde el issue #181, pero sigue deferiendo `ects`/`contenido`); no queda nada por deferir, `estado` nace `Vigente` por defecto sin pedirlo. La obligatoriedad se resuelve por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia. El Objetivo de Requisitos es literalmente "Dar de alta un Programa mínimo en el catálogo de una Facultad": la creación vive anidada bajo `Facultad`, con `facultad_id` en la URL y no en el body (`POST /api/v1/admin/facultades/{facultad_id}/programas`, mismo patrón que `POST /api/v1/universidades/{universidad_id}/facultades`).

**Retocado (issue #148, 2026-09-05)**: `<<choice>>` de unicidad de `codigo` -- antes un único paso sin ramas.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearProgramaView` (React) -- formulario mínimo (`codigo`+`nombre`, sin selector de Facultad: llega de la URL `/facultades/{facultad_id}/programas/crear`); al confirmar, `POST /api/v1/admin/facultades/{facultad_id}/programas`.
- **API**: `routers/programa.py::crear_programa(facultad_id, datos)` -- función suelta, sin capa Service; delega directo en el repositorio.
- **Modelo**: `Programa` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente con `estado` por defecto `Vigente`, no hay método de dominio que llamar.
- **Repositorio**: `ProgramaRepository.obtener_por_codigo(codigo)` (método nuevo, issue #148) + `ProgramaRepository.crear(codigo, nombre, facultad_id)` -- persistencia real e inmediata, no una mutación de sesión.

## Decisiones de diseño

- **`existeCodigo(codigo) : boolean` de Análisis baja a `obtener_por_codigo(codigo) : Programa | None`** en el Repositorio real: devolver el objeto en vez de un booleano no cuesta nada más (mismo `SELECT`) y dejaría el repositorio listo si el mensaje de error necesitara en el futuro algo del Programa existente (su `nombre`, su `Facultad`) -- hoy el 409 solo repite el `codigo`, pero no hay motivo para forzar una segunda consulta si se necesitara más adelante.
- **Comprobación en el Router, antes de `crear()`** -- mismo lugar donde vive el resto de precondiciones de creación/borrado del catálogo (`eliminar_facultad`, `desasociar_metodologia_docente_materia`): el Repositorio permanece "tonto", solo hace la escritura; el Router decide si procede.
- **`409 Conflict`**, no `400 Bad Request`: el dato en sí es válido (un `codigo` bien formado), el conflicto es con el estado ya existente del recurso -- mismo código que `eliminar_facultad()` usa para su propio bloqueo relacional.
- **Unicidad global al catálogo, no por `Facultad`**: `obtener_por_codigo(codigo)` no filtra por `facultad_id` -- ya lo fijó Requisitos (`codigo` identifica el `Programa`, la `Facultad` es dónde se administra). El índice único a nivel de esquema (`ix_programas_codigo`, ver Desarrollo) es la misma restricción reforzada en BD, no solo en aplicación -- defensa en profundidad ante cualquier otro camino de escritura que se añada más adelante (script de datos, otra ruta) y que se salte esta comprobación del Router.

- **Namespace propio `/api/v1/admin/facultades/{facultad_id}/programas`, separado de `/api/v1/programas`** (ya existente para `DirectorPrograma`) -- mismo motivo que `/auth/admin/login` se separó de `/auth/login`: evitar mezclar la autorización de dos actores distintos en el mismo endpoint. `/api/v1/programas` declara `Depends(get_current_director_programa_id)`; `/api/v1/admin/facultades/{facultad_id}/programas` declara `Depends(require_admin)`. Separar rutas mantiene cada guard en su sitio sin condicionales por rol dentro de una misma función.
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `ProgramaCreate` (Pydantic) exige `codigo` y `nombre` antes de que la función del Router se ejecute -- mismo mecanismo que `AsignaturaCreate` de referencia. `validarDatosObligatorios(codigo, nombre)` de Análisis se disuelve en Pydantic, mismo hallazgo ya documentado en el diagrama de clases de Diseño (discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)).
- **`201 Created`** con el objeto creado (incluido su `id`), no `204 No Content` -- la Vista navega de inmediato a `editarPrograma()` (`<<include>>` ya cerrado en Análisis) y necesita ese `id`.
- **Listado propio de Admin, anidado bajo Facultad**: `GET /api/v1/admin/facultades/{facultad_id}/programas` -> `listar_programas_de_la_facultad(facultad_id)` -> `ProgramaRepository.listar_de_la_facultad(facultad_id)` (método nuevo, con filtro `WHERE facultad_id = :facultad_id` -- a diferencia de `listar_dirigidos_por(director_programa_id)`, la variante `DirectorPrograma` ya existente). Es la variante `Admin` de `abrirProgramas()` que en su momento quedó fuera de alcance (ver Análisis de [`abrirProgramas()`](/RUP/02-analisis/casos-uso/abrirProgramas/README.md)): entonces no se construía porque no había ninguna acción de escritura que la necesitara -- el alta de catálogo era por SQL en bloque (discussion [#65](https://github.com/mmasias/pyCelda/discussions/65)). Ahora la hay: `crearPrograma()`/`eliminarPrograma()` se invocan desde ese listado, así que se construye la variante mínima necesaria -- solo listar y navegar, sin acciones que no sean estas. Corregido tras revisión en vivo de Manuel -- el wireframe real de `abrirProgramas()` (`PROGRAMAS -- ESCUELA POLITÉCNICA SUPERIOR`) y el Objetivo de `crearPrograma()` ("en el catálogo de una Facultad") exigen listado/creación anidados bajo `Facultad`, no un listado global -- verificado contra el wireframe antes de corregir.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py` (bloque anterior, ya mergeado), sin nota de pendiente: toda función nueva de `routers/programa.py` la declara explícitamente. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`crearPrograma()` en Análisis](/RUP/02-analisis/casos-uso/crearPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearPrograma/README.md).
- [`crearAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignatura/README.md) -- mismo patrón de creación con `201` + `<<include>>`.
- [`editarPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarPrograma/README.md) -- destino del `<<include>>`.
- [`abrirProgramas()` en Análisis](/RUP/02-analisis/casos-uso/abrirProgramas/README.md) -- por qué la variante `Admin` del listado quedó fuera de alcance entonces y por qué se construye ahora.
- [`editarPonderacionEvaluacion()` en Diseño](/RUP/03-diseño/casos-uso/editarPonderacionEvaluacion/README.md) -- precedente del patrón `<<choice>>` con `alt` en la secuencia.
- [`eliminarFacultad()`](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md) -- precedente de `409 Conflict` para un conflicto de estado del recurso, no de dato inválido.

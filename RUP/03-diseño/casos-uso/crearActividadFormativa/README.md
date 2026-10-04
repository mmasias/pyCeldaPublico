<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearActividadFormativa() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: ClaudeF-pyCelda-SDF1

## Propósito

Bajada a diseño del caso de análisis [`crearActividadFormativa()`](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md): CRUD real e inmediato contra `ActividadFormativaRepository`, sin ninguna capa Service. Un único paso, sin `<<choice>>` -- ambos campos (`codigo`, `nombre`) se piden en el alta: sin patrón C->U, como `crearMetodologiaDocente()`. La obligatoriedad se resuelve por esquema de entrada (Pydantic). La actividad nace dentro de una `Universidad` (`POST /universidades/{universidad_id}/actividades-formativas`).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearActividadFormativa/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearActividadFormativaView` (React) -- formulario de dos campos (`codigo`, `nombre`) más la `Universidad` destino; al confirmar, `POST /api/v1/universidades/{universidad_id}/actividades-formativas`.
- **API**: `routers/actividad_formativa.py::crear_actividad_formativa(universidad_id, datos)` -- función suelta; comprueba que la `Universidad` exista (`404` si no) y delega en el repositorio.
- **Modelo**: `ActividadFormativa` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente.
- **Repositorio**: `ActividadFormativaRepository.crear(universidad_id, codigo, nombre)` -- persistencia real e inmediata; además puebla a 0 las filas de asociación de las `Materia`/`AsignaturaPrograma` existentes de la `Universidad`.

## Decisiones de diseño

- **Sin capa Service**: la función del Router llama al repositorio directamente (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Validación de obligatoriedad por esquema de entrada**: `ActividadFormativaCreate` (Pydantic) exige `codigo` y `nombre` antes de que la función del Router se ejecute (`422` si falta alguno). `validarDatosObligatorios(codigo, nombre)` de Análisis se disuelve en Pydantic, mismo hallazgo ya documentado en el diagrama de clases de Diseño (discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)).
- **`Universidad` inexistente: `404`** -- guardia en el Router con `UniversidadRepository.obtener()`, antes de crear. `ActividadFormativa` es catálogo de `Universidad` (`universidad_id` NOT NULL, issue [#655](https://github.com/mmasias/pyCelda/issues/655)): cada `Universidad` tiene el suyo, por eso el listado y el alta cuelgan de `/universidades/{universidad_id}` y el detalle/edición/borrado por identificador propio.
- **Invariante de autopoblado en el propio `crear()`** (issue [#655](https://github.com/mmasias/pyCelda/issues/655)): toda `Materia`/`AsignaturaPrograma` tiene una fila a 0 por cada `ActividadFormativa` de su `Universidad`; al crear una nueva, el repositorio las puebla (lógica de aplicación, no un trigger de BD). Se representa como un segundo `INSERT` en la secuencia, no como colaboración de Análisis.
- **`201 Created` con el objeto creado (incluido su `id`), navegando al detalle** -- sin patrón C->U no hay `<<include>>` de edición: la Vista navega a `abrirActividadFormativa()` de la recién creada; la nota `editarActividadFormativa()` de la transición de Requisitos es la edición disponible desde ese detalle.
- **Autorización de `Admin`: `Depends(require_admin)`** -- catálogo de `Admin`, sin pertenencia que verificar (sin `get_current_director_programa_id`). El historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real, no un detalle menor. Especialmente relevante por ser endpoint de escritura.

## Referencias

- [`crearActividadFormativa()` en Análisis](/RUP/02-analisis/casos-uso/crearActividadFormativa/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearActividadFormativa/README.md).
- [`crearMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md) -- clúster plantilla.
- [`abrirActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/abrirActividadFormativa/README.md) -- destino de la navegación tras crear.
- [`editarActividadFormativa()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadFormativa/README.md) -- edición disponible desde el detalle alcanzado.

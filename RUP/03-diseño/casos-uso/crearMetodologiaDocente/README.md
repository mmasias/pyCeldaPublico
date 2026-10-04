<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > crearMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearMetodologiaDocente()`](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md): CRUD real e inmediato contra `MetodologiaDocenteRepository`, sin ninguna capa Service. Un único paso, sin `<<choice>>` -- ambos campos (`codigo`, `descripcion`) se piden en el alta porque los dos identifican la metodología: Requisitos cierra "sin patrón C->U", a diferencia de `crearAsignatura()` que difiere `ects`/`contenido` a la edición. La obligatoriedad se resuelve por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearMetodologiaDocenteView` (React) -- formulario con selector de `Universidad` y dos campos (`codigo`, `descripcion`); al confirmar, `POST /api/v1/universidades/{universidad_id}/metodologias-docentes`.
- **API**: `routers/metodologia_docente.py::crear_metodologia_docente(universidad_id, datos)` -- función suelta, sin capa Service; responde 404 si la `Universidad` no existe y delega en el repositorio.
- **Modelo**: `MetodologiaDocente` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente, no hay método de dominio que llamar.
- **Repositorio**: `MetodologiaDocenteRepository.crear(universidad_id, codigo, descripcion)` -- persistencia real e inmediata, no una mutación de sesión.

## Decisiones de diseño

- **Sin capa Service**: la función del Router llama al repositorio directamente -- decisión ya cerrada en la discussion [#58](https://github.com/mmasias/pyCelda/discussions/58).
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `MetodologiaDocenteCreate` (Pydantic) exige `codigo` y `descripcion` antes de que la función del Router se ejecute -- mismo mecanismo que `AsignaturaCreate` de referencia. `validarDatosObligatorios(codigo, descripcion)` de Análisis se disuelve en Pydantic, mismo hallazgo ya documentado en el diagrama de clases de Diseño (discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)).
- **`201 Created` con el objeto creado (incluido su `id`), navegando al detalle** -- sin patrón C->U no hay `<<include>>` de edición: la Vista navega a `abrirMetodologiaDocente()` de la `MetodologiaDocente` recién creada (`:METODOLOGIA_DOCENTE_ABIERTO`); la nota `editarMetodologiaDocente()` de la transición de Requisitos es la edición disponible desde ese detalle, no un salto directo al formulario.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py`, sin nota de pendiente: toda función de `routers/metodologia_docente.py` la declara explícitamente. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`crearMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/crearMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearMetodologiaDocente/README.md) -- cierre explícito de "sin patrón C->U".
- [`crearAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignatura/README.md) -- contraste: creación con `<<include>>` C->U hacia la edición.
- [`abrirMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md) -- destino de la navegación tras crear.
- [`editarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md) -- edición disponible desde el detalle alcanzado.

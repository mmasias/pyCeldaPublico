<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearProfesor() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearProfesor/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearProfesor()`](/RUP/02-analisis/casos-uso/crearProfesor/README.md): CRUD real e inmediato contra `ProfesorRepository`, sin capa Service. Un único paso -- ambos campos (`nombre`, `email`) se piden en el alta porque los dos identifican al `Profesor` (único caso del lote sin patrón C->U, regla de Requisitos). A diferencia de `crearMetodologiaDocente()`, aquí sí hay un conflicto posible: el `email` es único en el catálogo, así que el `201` convive con un `409` si ya existe un `Profesor` con ese email.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearProfesor/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearProfesorView` (React) -- formulario de dos campos (`nombre`, `email`); al confirmar, `POST /api/v1/profesores`.
- **API**: `routers/profesor.py::crear_profesor(datos)` -- función suelta, sin capa Service; comprueba unicidad de email y delega en el repositorio.
- **Modelo**: `Profesor` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente. La columna `nombre` (añadida nullable + backfill previo) se exige siempre vía Pydantic aquí.
- **Repositorio**: `ProfesorRepository.crear(nombre, email)` -- persistencia real e inmediata; normaliza el email (`strip().lower()`) para que la resolución de rol por email contra `DirectorGrado` y el login funcionen sin variantes de caja.

## Decisiones de diseño

- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `ProfesorCreate` (Pydantic) exige `nombre` y `email` antes de que la función del Router se ejecute -- `validarDatosObligatorios(nombre, email)` de Análisis se disuelve en Pydantic, mismo hallazgo ya documentado en el diagrama de clases de Diseño (discussion [#60](https://github.com/mmasias/pyCelda/discussions/60)).
- **`409` por email duplicado, comprobado antes de crear**: el endpoint consulta `obtener_por_email()` y responde `409` con `detail="Ya existe un Profesor con el email ..."` -- el `unique=True` de la columna queda como red de seguridad de último nivel, no como mecanismo de respuesta al usuario (un `IntegrityError` crudo no llevaría mensaje útil).
- **`201 Created` con el objeto creado (incluido su `id`), navegando al detalle** -- sin patrón C->U no hay `<<include>>` de edición: la Vista navega a `abrirProfesor()` del `Profesor` recién creado (`:PROFESOR_ABIERTO`); la nota `editarProfesor()` de la transición de Requisitos es la edición disponible desde ese detalle, no un salto directo al formulario.
- **Normalización de email en el repositorio** (`strip().lower()`), mismo criterio que `app/scripts/definir_director_grado.py`: la unicidad y la resolución de rol por email operan sobre una sola forma canónica.
- **Autorización de `Admin`: `Depends(require_admin)`** -- especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`crearProfesor()` en Análisis](/RUP/02-analisis/casos-uso/crearProfesor/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearProfesor/README.md) -- cierre explícito de "sin patrón C->U".
- [`crearMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md) -- mismo patrón de alta sin C->U, allí sin conflicto posible de clave.
- [`abrirProfesor()` en Diseño](/RUP/03-diseño/casos-uso/abrirProfesor/README.md) -- destino de la navegación tras crear.
- [`editarProfesor()` en Diseño](/RUP/03-diseño/casos-uso/editarProfesor/README.md) -- la misma regla de unicidad de email, en edición.

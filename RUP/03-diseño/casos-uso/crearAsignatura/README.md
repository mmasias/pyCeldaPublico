<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearAsignatura() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearAsignatura/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-09-05
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`crearAsignatura()`](/RUP/02-analisis/casos-uso/crearAsignatura/README.md): CRUD real e inmediato contra `AsignaturaRepository`, sin ninguna capa Service. `ects`, `contenido` y `estado` se completan al editar, y `estado` nace `Vigente` por defecto sin pedirlo (patrón C->U). La obligatoriedad de `codigo`/`nombre` se resuelve por esquema de entrada (Pydantic), no por una llamada explícita en la secuencia.

**Retocado (issue #181, 2026-09-05)**: `<<choice>>` de unicidad de `codigo` -- antes un único paso sin ramas, mismo patrón que [`crearGrado()`](/RUP/03-diseño/casos-uso/crearGrado/README.md) (issue #148).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearAsignatura/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearAsignaturaView` (React) -- formulario mínimo (`codigo`+`nombre`); al confirmar, `POST /api/v1/asignaturas`.
- **API**: `routers/asignatura.py::crear_asignatura(datos)` -- función suelta, sin capa Service; comprueba unicidad de `codigo` y delega en el repositorio.
- **Modelo**: `Asignatura` (SQLAlchemy) -- sin lógica propia invocada: el Repository construye la fila directamente con `estado` por defecto `Vigente`, no hay método de dominio que llamar.
- **Repositorio**: `AsignaturaRepository.obtener_por_codigo(codigo)` (método nuevo, issue #181) + `AsignaturaRepository.crear(codigo, nombre)` -- persistencia real e inmediata, no una mutación de sesión.

## Decisiones de diseño

- **`existeCodigo(codigo) : boolean` de Análisis baja a `obtener_por_codigo(codigo) : Asignatura | None`** en el Repositorio real -- mismo razonamiento que `GradoRepository.obtener_por_codigo()` (#148): devolver el objeto no cuesta más que el booleano y deja el repositorio listo si el mensaje de error necesitara en el futuro algo de la `Asignatura` existente.
- **Comprobación en el Router, antes de `crear()`** -- mismo lugar donde vive el resto de precondiciones de creación/borrado del catálogo.
- **`409 Conflict`**, no `400 Bad Request`: mismo código que `crearGrado()` -- el dato en sí es válido, el conflicto es con el estado ya existente del recurso.
- **Unicidad global al catálogo institucional**: no hay partición por `Grado`/`Facultad` -- `Asignatura` es un catálogo plano, a diferencia de `Grado` (que sí aclara explícitamente "global, no por Facultad" porque podría confundirse). La restricción se refuerza en BD, no solo en aplicación -- **`unique=True` en el modelo Y el índice `ix_asignaturas_codigo` de la migración**, mismo criterio de defensa en profundidad que `Grado.codigo` tras #148 (una BD fresca nace ya con la restricción; producción la gana al correr `migrar_asignatura_catalogo_y_fk.py`, porque `Base.metadata.create_all()` no altera la tabla `asignaturas` ya existente). `unique=True` y `nullable=True` conviven (SQLite/PostgreSQL permiten varios `NULL` bajo `UNIQUE`), así que las placeholder legado sin código no chocan. El script de backfill del catálogo puebla `Asignatura` directamente por SQLAlchemy sin pasar por este Router -- se apoya en la misma restricción para no duplicar si se reejecuta.
- **Validación de obligatoriedad por esquema de entrada**, no por paso explícito de la secuencia: `AsignaturaCreate` (Pydantic) exige `codigo` y `nombre` antes de que la función del Router se ejecute.
- **`201 Created`** con el objeto creado (incluido su `id`), no `204 No Content` -- la Vista navega de inmediato a `editarAsignatura()` (`<<include>>` ya cerrado en Análisis) y necesita ese `id` para completar `ects` y `contenido`.
- **Autorización de `Admin`: `Depends(require_admin)`** -- sin cambio respecto a la versión anterior de este caso de uso.

## Referencias

- [`crearAsignatura()` en Análisis](/RUP/02-analisis/casos-uso/crearAsignatura/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignatura/README.md).
- [`crearGrado()` en Diseño](/RUP/03-diseño/casos-uso/crearGrado/README.md) -- precedente del `<<choice>>` de unicidad de código y de `409 Conflict` (issue #148), reutilizado aquí punto por punto.
- [`editarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md) -- destino del `<<include>>`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- FK `AsignaturaGrado.asignatura_id` y backfill del catálogo (issue #181), contexto de por qué `codigo` deja de ser opcional.

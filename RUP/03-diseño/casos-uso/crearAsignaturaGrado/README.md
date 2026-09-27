<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > crearAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/crearAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.1
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`crearAsignaturaGrado()`](/RUP/02-analisis/casos-uso/crearAsignaturaGrado/README.md): la creación más compuesta del catálogo -- dos `GET` previos para poblar los selectores (Materias del `Grado` por un lado, `Asignatura` del catálogo por otro), un `POST` que valida la pertenencia de la `Materia` al `Grado` de la URL, resuelve la herencia de `nombre`/`ects`/`contenido` y persiste con `estado` naciendo `Vigente`; tras persistir, crea también la `Guia` vacía de la `AsignaturaGrado` recién nacida (efecto colateral documentado en Requisitos). Sin capa Service: la herencia se resuelve en el propio Router, coordinación sin regla de negocio (el modelo de dominio define la herencia, el Router solo aplica el default). La salida vuelve a la ficha del `Grado`, sin `<<include>>` -- excepción documentada en Análisis.

**Retocado (issue #181, 2026-09-05)**: el `asignatura_id` elegido en el selector, hasta ahora usado solo como plantilla en el instante de creación para resolver `nombre`/`ects`/`contenido` y descartado después, **se persiste como FK real** (`AsignaturaGrado.asignatura_id`, nullable) -- honra por fin `(Grado, Asignatura) .. AsignaturaGrado` del [modelo de dominio](/RUP/00-modelo-del-dominio/README.md), que la implementación no cumplía (hallazgo original de #181). Sin cambio de comportamiento visible para el `Admin`: el selector y la herencia ya funcionaban así, Requisitos/Análisis ya estaban correctos -- lo que cambia es que el sistema ahora recuerda de qué `Asignatura` del catálogo procede cada `AsignaturaGrado`, en vez de perder esa referencia tras la creación. **No implica que `AsignaturaGrado.contenido` deje de ser una copia independiente**: sigue divergiendo libremente de `Asignatura.contenido` tras la creación (patrón catálogo -> override -> materialización, discussion #191) -- la FK es trazabilidad, no vínculo vivo.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/crearAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `CrearAsignaturaGradoAdmin.tsx` (React, ruta `/admin/grados/{grado_id}/asignaturas-grado/crear`) -- al montar, `Promise.all` de `GET /api/v1/admin/grados/{grado_id}/materias` (selector Materia) y `GET /api/v1/asignaturas` (selector Asignatura, endpoint del catálogo ya existente); al elegir una Asignatura, autorrellena `nombre`/`ECTS`/`Contenido` con sus valores heredados, editables in situ.
- **API**: `routers/asignatura_grado.py::crear_asignatura_grado(grado_id, datos)` -- función nueva; valida `Materia` y `Asignatura`, resuelve la herencia, delega en el repositorio y crea la `Guia` vacía.
- **Modelo**: `AsignaturaGrado` (SQLAlchemy) -- sin lógica propia invocada en la creación: el Repository construye la fila con `estado="Vigente"` explícito. `Guia` (SQLAlchemy) -- ídem: el Repository la construye con `estado="Borrador"` explícito.
- **Repositorio**: `MateriaRepository.obtener(materia_id)` / `AsignaturaRepository.obtener(asignatura_id)` (reutilizados); `AsignaturaGradoRepository.crear(...)` -- gana el parámetro `asignatura_id` (issue #181), fija `estado="Vigente"` explícitamente (no delega en el `default` de la columna, inerte); `GuiaRepository.crear(grado_id, asignatura_grado_id, semestre)` -- método nuevo que fija `estado="Borrador"` explícitamente.

## Decisiones de diseño

- **`materia_id` viaja en el body, `grado_id` en la URL**: la URL identifica el agregado (`Grado`) desde el que se crea; el body (`AsignaturaGradoCreate`) lleva las dos referencias de los selectores (`materia_id`, `asignatura_id`), los cuatro campos de identidad (`curso`, `caracter`, `idioma`, `semestre_default`) obligatorios, y los tres overrides (`nombre`, `ects`, `contenido`) opcionales con `None = heredar del catálogo`.
- **La guardia de pertenencia es del Router**: `materia.grado_id != grado_id` -> `404 "Materia no encontrada en este Grado"` -- la composición `Materia *-- AsignaturaGrado` vive dentro del `Grado`; el selector solo ofrece Materias válidas, la guardia cubre el caso de un request artesanal (mismo papel que el `404` de identificador inexistente).
- **La herencia se resuelve en el Router, no en el Modelo ni en la Vista**: `nombre = datos.nombre if datos.nombre is not None else asignatura.nombre` (ídem `ects` con `float(asignatura.ects or 0)`, `contenido`). La Vista ya muestra el valor heredado, pero el `None` del body es quien decide -- así un cliente que omite los overrides siempre hereda, sin depender de que la Vista haya rellenado bien.
- **`estado="Vigente"` explícito en `AsignaturaGradoRepository.crear()`**: el `default="Activo"` de la columna `estado` es un detalle inerte que ningún camino real usa; la creación fija `Vigente` a mano, igual que hacía el SQL de carga inicial.
- **`201 Created` con `AsignaturaGradoResponse`**: la Vista vuelve a la ficha del `Grado` y refresca la tabla embebida; el objeto devuelto permite verificar la herencia resuelta en pruebas sin segunda petición.
- **La `Guia` vacía nace en el mismo `POST`, sin esperar a `activarCursoAcademico()`**: `GuiaRepository.crear(grado_id, asignatura_grado_id, asignatura_grado.semestre_default)` inmediatamente después de persistir la `AsignaturaGrado` -- `estado="Borrador"`, sin ponderaciones/referencias/profesorado, mismo criterio que `activarCursoAcademico()` documenta para el caso "sin `Guia` anterior que clonar" (ver [modelo del dominio](/RUP/00-modelo-del-dominio/README.md)). Sin ella, `listar_mis_asignaturas_grado()` devolvería `guia_id: None` y el `Profesor` asignado no vería "Abrir guía" -- inconsistencia detectada en producción. `grado_id` sale del path param, sin ir a buscarlo por `materia.grado_id`. Simplificación actual: `CursoAcademico` no existe todavía como tabla, así que hoy la creación es incondicional -- cuando exista, adquirirá la condición de curso activo sin rediseñar este paso.
- **Namespace `/api/v1/admin/grados/{grado_id}/asignaturas-grado`, con `Depends(require_admin)`** -- separado del `/api/v1/grados/{grado_id}/asignaturas-grado` de `DirectorGrado` (que además agrega profesorado y estado de `Guia` por fila). Endpoint de escritura: guard explícito por el historial IDOR (#86/#96).
- **Selector de `Asignatura` contra `GET /api/v1/asignaturas` ya existente**: el catálogo institucional no tiene variantes por actor -- ya sirve a `abrirAsignaturas()` de `Admin`; no se duplica endpoint Admin para lo mismo.
- **`asignatura_id` persiste como FK nullable, no obligatoria a nivel de esquema** (issue #181): las 786 `AsignaturaGrado` ya existentes en producción se backfillean por correlación de código contra los JSON del seed (ver [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md)), pero el backfill no puede resolver el 100% de los casos (2 pares `(grado, nombre)` ambiguos detectados en los datos reales de GTEL, ver el mismo documento) -- la columna admite `NULL` para esos casos en vez de forzar una resolución arbitraria. `crear_asignatura_grado()` sí exige `asignatura_id` en el body (ya lo hacía `AsignaturaGradoCreate`, sin cambio): la nulidad de la columna es solo para el dato legado, todo alta nueva la trae siempre.

## Referencias

- [`crearAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/crearAsignaturaGrado/README.md) -- diagrama de colaboración origen, con la excepción de salida sin `<<include>>`.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/crearAsignaturaGrado/README.md) -- fuente de verdad del formulario, incluida la corrección que añadió el selector de `Materia`.
- [`crearGrado()` en Diseño](/RUP/03-diseño/casos-uso/crearGrado/README.md) -- contraste: `crearX()` simple con `<<include>>`, el precedente de la rebanada anterior.
- [`abrirGrado()` en Diseño](/RUP/03-diseño/casos-uso/abrirGrado/README.md) -- la tabla embebida desde la que se dispara y a la que se vuelve, con su variante Admin documentada en este mismo lote.
- [`eliminarAsignaturaGrado()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignaturaGrado/README.md) -- la otra acción sobre la misma tabla, construida en este mismo lote.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) -- issue #181: FK `AsignaturaGrado.asignatura_id`, catálogo `Asignatura` poblado, `Asignatura.codigo` obligatorio/único/fijo.

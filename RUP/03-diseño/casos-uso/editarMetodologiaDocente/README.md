<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarMetodologiaDocente() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarMetodologiaDocente()`](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md): CRUD real e inmediato, `PUT /api/v1/metodologias-docentes/{metodologia_docente_id}`, sin ninguna llamada a otra entidad. Sin `alt` de negocio -- `MetodologiaDocente` no tiene ninguna regla de validación cruzada en el modelo de dominio; la única validación es de forma (`codigo` y `descripcion` obligatorios), resuelta por Pydantic. `MetodologiaDocente` gana aquí su método `actualizar(codigo, descripcion)`.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarMetodologiaDocente/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarMetodologiaDocenteView` (React) -- carga el formulario con `GET /api/v1/metodologias-docentes/{metodologia_docente_id}` (mismo endpoint que `abrirMetodologiaDocente()`), envía cambios con `PUT`; el `codigo` se presenta de solo lectura (regla de Requisitos: no editable una vez creada la metodología).
- **API**: `routers/metodologia_docente.py::editar_metodologia_docente(metodologia_docente_id, datos)` -- función nueva; sin validación de negocio, solo coordina la actualización.
- **Modelo**: `MetodologiaDocente.actualizar(codigo, descripcion)` -- método nuevo, mismo patrón que `Asignatura.actualizar(nombre, ects, contenido)`.
- **Repositorio**: `MetodologiaDocenteRepository.obtener(metodologia_docente_id)` (reutilizado) / `.editar(metodologia_docente, codigo, descripcion)` -- método nuevo.

## Decisiones de diseño

- **Sin `alt` de negocio**: la única validación es de forma, resuelta por `MetodologiaDocenteUpdate` (Pydantic: `codigo` y `descripcion` obligatorios), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`.
- **El `codigo` viaja en `MetodologiaDocenteUpdate` aunque el formulario no lo edita**: regla de Requisitos ("el código no es editable una vez creada la metodología") resuelta en la Vista -- el campo se muestra de solo lectura y se reenvía sin cambios; el esquema de entrada no distingue campos por caso de uso, mismo criterio que `ProgramaAdminUpdate` frente al `codigo` de `Programa`.
- **`MetodologiaDocenteRepository.editar(metodologia_docente, codigo, descripcion)` es método nuevo**: el repositorio ya existía con las queries de disponibilidad; gana aquí su método de persistencia de edición (invoca `MetodologiaDocente.actualizar(codigo, descripcion)` y persiste), mismo reparto Modelo-muta/Repository-persiste que `Asignatura.actualizar()` + `AsignaturaRepository.actualizar()`.
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **Reutiliza el `GET` de `abrirMetodologiaDocente()`**: mismo endpoint de carga, sin duplicar lógica de lectura.
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT` -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** -- toda función de `routers/metodologia_docente.py` la declara explícitamente. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`editarMetodologiaDocente()` en Análisis](/RUP/02-analisis/casos-uso/editarMetodologiaDocente/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarMetodologiaDocente/README.md).
- [`abrirMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/abrirMetodologiaDocente/README.md) -- mismo endpoint `GET`, reutilizado.
- [`crearMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/crearMetodologiaDocente/README.md) -- el alta alcanza el detalle desde el que se edita.
- [`eliminarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/eliminarMetodologiaDocente/README.md) -- el otro caso de uso que muta el catálogo, con `<<choice>>` bloqueante.
- [`editarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/editarAsignatura/README.md) -- mismo patrón de `GET` previo + `PUT` sin `alt` de negocio.

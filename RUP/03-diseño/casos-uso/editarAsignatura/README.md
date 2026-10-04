<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarAsignatura() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarAsignatura/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-24
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarAsignatura()`](/RUP/02-analisis/casos-uso/editarAsignatura/README.md): CRUD real e inmediato, `PUT /api/v1/asignaturas/{asignatura_id}`, sin ninguna llamada a otra entidad. Sin `alt` de negocio -- `Asignatura` no tiene ninguna regla de validación cruzada en el modelo de dominio; la única validación es de forma (`nombre` y `ects` obligatorios, `contenido` opcional), resuelta por Pydantic. `estado` queda fuera del formulario: se gestiona en exclusiva desde [`eliminarAsignatura()`](/RUP/03-diseño/casos-uso/eliminarAsignatura/README.md). `Asignatura` gana aquí su método `actualizar(nombre, ects, contenido)`. Es también el destino del `<<include>>` de `crearAsignatura()`: tras crear, el `Admin` queda editando la `Asignatura` recién creada, completando `ects` y `contenido`.

**Retocado (issue #181, 2026-09-05)**: `codigo` (obligatorio y único desde `crearAsignatura()`) no viaja en `AsignaturaUpdate` -- el formulario lo muestra como texto plano de solo lectura, mismo patrón que `editarPrograma()` (issue #148).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarAsignatura/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarAsignaturaView` (React) -- carga el formulario con `GET /api/v1/asignaturas/{asignatura_id}` (mismo endpoint que `abrirAsignatura()`), envía cambios con `PUT`; el formulario presenta `codigo` como texto plano de solo lectura (no un `<input>` deshabilitado) y nunca presenta `estado`.
- **API**: `routers/asignatura.py::editar_asignatura(asignatura_id, datos)` -- función nueva; sin validación de negocio, solo coordina la actualización.
- **Modelo**: `Asignatura.actualizar(nombre, ects, contenido)` -- método nuevo, mismo patrón que `Universidad.actualizar(nombre)`.
- **Repositorio**: `AsignaturaRepository.obtener(asignatura_id)` (reutilizado); `.actualizar(asignatura)` -- método nuevo.

## Decisiones de diseño

- **Sin `alt` de negocio**: `Asignatura` no tiene ninguna regla de validación cruzada en el modelo de dominio -- la única validación es de forma, resuelta por `AsignaturaUpdate` (Pydantic: `nombre` y `ects` obligatorios, `contenido` opcional), mismo mecanismo ya documentado en el diagrama de clases de Diseño para `validarDatosObligatorios()`. `estado` no viaja en el esquema: la edición no puede mutarlo.
- **`codigo` no viaja en `AsignaturaUpdate` -- se muestra en el formulario pero como solo lectura**: su inmutabilidad se garantiza por ausencia del esquema, no por confiar en que la Vista lo envíe intacto -- mismo criterio que `ProgramaUpdate` (#148).
- **`AsignaturaRepository.actualizar(asignatura)` es método nuevo**: el repositorio nace en esta rebanada con `listar`/`obtener`/`crear`/`actualizar`, reutilizado también por `eliminarAsignatura()` para persistir el `Extinguido`.
- **Sin capa Service**: Router delgado -> Modelo/Repository.
- **Reutiliza el `GET` de `abrirAsignatura()`**: mismo endpoint de carga, sin duplicar lógica de lectura.
- **`404` si el identificador no existe**, tanto en el `GET` previo como en el `PUT` -- guardia de Router sobre el `None` del repositorio.
- **Autorización de `Admin`: `Depends(require_admin)`** -- ya disponible en `backend/app/core/auth.py` (bloque anterior, ya mergeado), sin nota de pendiente: toda función de `routers/asignatura.py` la declara explícitamente. Especialmente relevante aquí por ser endpoint de escritura: el historial de bugs de autorización del proyecto (IDOR #86/#96) hace que dejarlo implícito sea un hueco real.

## Referencias

- [`editarAsignatura()` en Análisis](/RUP/02-analisis/casos-uso/editarAsignatura/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarAsignatura/README.md).
- [`abrirAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/abrirAsignatura/README.md) -- mismo endpoint `GET`, reutilizado.
- [`crearAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/crearAsignatura/README.md) -- `<<include>>` de origen.
- [`eliminarAsignatura()` en Diseño](/RUP/03-diseño/casos-uso/eliminarAsignatura/README.md) -- único gestor del `estado`, fuera de este formulario.
- [`editarUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) -- mismo patrón de `GET` previo + `PUT` sin `alt` de negocio.
- [`editarPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarPrograma/README.md) -- mismo criterio de `codigo` fijo, mostrado solo lectura (issue #148).

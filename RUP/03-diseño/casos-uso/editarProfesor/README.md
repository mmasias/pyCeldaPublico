<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarProfesor() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarProfesor/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-08-26
- **Autor**: GLM (vía opencode)

## Propósito

Bajada a diseño del caso de análisis [`editarProfesor()`](/RUP/02-analisis/casos-uso/editarProfesor/README.md): CRUD real contra `ProfesorRepository`, sin `<<choice>>`. Ambos campos siempre editables (a diferencia de `editarMetodologiaDocente()`, que congela el `codigo`): el formulario precarga `nombre`/`email` y los reenvía completos. El único conflicto es la unicidad del nuevo `email`: `409` si lo usa otro `Profesor`; reenviar el propio email vigente no es conflicto (el chequeo excluye el id propio).

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarProfesor/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarProfesorView` (React) -- precarga con `GET /api/v1/profesores/{profesor_id}`; al confirmar, `PUT /api/v1/profesores/{profesor_id}`; vuelve al detalle.
- **API**: `routers/profesor.py::editar_profesor(profesor_id, datos)` -- `404` si no existe, `409` si el nuevo email lo usa otro.
- **Modelo**: `Profesor.actualizar(nombre, email)` -- el método de dominio que ya trajo la mini-rebanada del modelo.
- **Repositorio**: `ProfesorRepository.obtener_por_email_de_otro(email, excluir_id)` (chequeo de conflicto) / `.editar(profesor, nombre, email)` (persistencia, con normalización de email).

## Decisiones de diseño

- **`obtener_por_email_de_otro(email, excluir_id)`**, no `obtener_por_email()`: la misma dirección de email reenviada sin cambios es el caso normal de edición, no un conflicto -- excluir el propio id en la query lo expresa directamente.
- **Implicación conocida y aceptada de la edición del email**: la resolución `Profesor`-`DirectorPrograma` es por email (ver [`abrirProfesor()`](/RUP/03-diseño/casos-uso/abrirProfesor/README.md)); cambiar el email de un `Profesor` que dirige `Programa` desvincula su rol hasta que el `DirectorPrograma` se alinee -- Requisitos no fija bloqueo para este caso y no se añade uno; el desajuste es visible (la sección "Programas que dirige" queda vacía en el detalle) y reversible reeditando.
- **Validación de obligatoriedad por esquema de entrada**: `ProfesorUpdate` (Pydantic) exige ambos campos -- el formulario reenvía siempre los dos, no hay parches parciales.
- **`200 OK` con `ProfesorResponse`** -- el detalle al que se vuelve se recarga con su propio `GET`; el `PUT` no necesita ensamblar la sección de programas.
- **Autorización de `Admin`: `Depends(require_admin)`** -- endpoint de escritura, explícito.
- **Sin capa Service**: Router delgado -> Repository.

## Referencias

- [`editarProfesor()` en Análisis](/RUP/02-analisis/casos-uso/editarProfesor/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarProfesor/README.md).
- [`editarMetodologiaDocente()` en Diseño](/RUP/03-diseño/casos-uso/editarMetodologiaDocente/README.md) -- contraste: campo identificador congelado tras crear; aquí ambos editables.
- [`crearProfesor()` en Diseño](/RUP/03-diseño/casos-uso/crearProfesor/README.md) -- la misma regla de unicidad, en alta.

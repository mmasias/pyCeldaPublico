<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasMateria() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-04
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarActividadesFormativasMateria()`](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md): rejilla de un submit sobre las 10 filas `ActividadFormativaMateria` de una `Materia`. Dos interacciones de Análisis (`cargarActividadesFormativas` + `guardarActividadesFormativas`) sobre la misma URL: `GET` + `PUT`. `<<choice>>` de validación de entrada = `422` sin persistir nada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadesFormativasMateriaView` (React) -- rejilla de 10 filas, `codigo`/`nombre` de solo lectura, `horas` editable (numérico, decimales); `GET` + `PUT /api/v1/materias/{materia_id}/actividades-formativas`. Vive en la pantalla de detalle de `Materia` ([`abrirMateria()`](/RUP/03-diseño/casos-uso/abrirMateria/README.md)).
- **API**: `routers/materia.py::listar_actividades_formativas(materia_id)` / `::editar_actividades_formativas(materia_id, datos)` -- funciones sueltas, auth `get_current_director_programa_id` + `_verificar_materia_del_director` (mismo guard que el resto de self-loops de `MATERIA_ABIERTO`).
- **Modelo**: `ActividadFormativaMateria.actualizar(horas)` -- única columna editable.
- **Repositorio**: `ActividadFormativaMateriaRepository.listar_de(materia_id)` / `.actualizar_lote(filas)`.

## Contrato de endpoint

### GET `/api/v1/materias/{materia_id}/actividades-formativas`

**Response (200 OK):** lista de 10 objetos `{ actividad_formativa_id, codigo, nombre, horas }`, ordenados por `codigo` (`AF1`..`AF10`).

**Response (404 Not Found):** `{ "detail": "Materia no encontrada" }` -- `Materia` inexistente o no dirigida por el `DirectorPrograma`.

### PUT `/api/v1/materias/{materia_id}/actividades-formativas`

**Request body:** `{ "actividades": [ { "actividad_formativa_id": int, "horas": number }, ... ] }` -- se espera el conjunto de las 10; cada entrada actualiza su fila por `actividad_formativa_id`.

**Response (200 OK):** la lista actualizada, mismo shape que el `GET`.

**Response (422 Unprocessable Entity):**
```json
{ "detail": "horas no puede ser negativa" }
```
o `actividad_formativa_id` fuera del catálogo / duplicado. **Nada se persiste** (validación antes de tocar la BD).

**Response (404 Not Found):** `Materia` inexistente o ajena.

## Decisiones de diseño

- **URL sin id de la fila de asociación**: `ActividadFormativaMateria` no tiene id propio (PK compuesta `(materia_id, actividad_formativa_id)`). El recurso es "las actividades formativas de esta `Materia`" como conjunto -- `GET`/`PUT` de la colección entera, no de una fila. Paralelo al patrón `sincronizar_*` de `Guia` (un `PUT` con la lista final), no al `PUT /{sub_id}` de `editarAsociacionMetodologiaDocenteMateria()`.
- **`PUT` idempotente y transaccional**: aplica las 10 actualizaciones en una sola transacción; si alguna `horas` es negativa o un `actividad_formativa_id` no está en el catálogo, `422` y `rollback` -- el reparto no queda a medias.
- **`horas` es `Numeric(6, 2)`** (mismo criterio que `ects`/`ponderacion`): admite decimales, no negativos. Sin cota superior explícita -- no hay regla de negocio que la fije (la suma vs ECTS no se valida, decisión de la discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)).
- **La regla `AfM = Σ AfAdM` no se toca aquí**: es responsabilidad de [`consultarEstadoActividadesFormativasMateria()`](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md), medidor blando. Guardar un reparto que aún no cuadra es válido.
- **Sin `HistorialCambio`**: `editarMateria()`/`editarAsignaturaPrograma()` tampoco lo generan -- `HistorialCambio` es del agregado `Guia`. Consistente.
- **Tabla nueva `actividades_formativas_materia`** (`materia_id` PK/FK, `actividad_formativa_id` PK/FK, `horas`). Se crea en la migración de esquema del clúster; las 10 filas por `Materia` se autopueblan a 0 en el `crear()` del repositorio, en `seed_programa.py` y en el backfill de la migración (ver [modelo de datos](/RUP/03-diseño/modelo-datos/README.md)).

## Referencias

- [`editarActividadesFormativasMateria()` en Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md).
- [`editarActividadesFormativasAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) -- mismo patrón con `porcentaje_presencialidad` además de `horas`.
- [`consultarEstadoActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) -- el medidor de la regla `AfM = Σ AfAdM`.

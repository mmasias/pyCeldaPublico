<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaGrado() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorGrado.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-04
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarActividadesFormativasAsignaturaGrado()`](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md): mismo patrón que [`editarActividadesFormativasMateria()`](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) sobre la asociación `ActividadFormativaAsignaturaGrado`, con `porcentaje_presencialidad` (rango 0-100) además de `horas`. `GET` + `PUT` sobre la misma URL; `<<choice>>` de validación de entrada = `422` sin persistir.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaGrado/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadesFormativasAsignaturaGradoView` (React) -- rejilla de 10 filas, `codigo`/`nombre` de solo lectura, `horas` y `porcentaje_presencialidad` editables; `GET` + `PUT /api/v1/asignaturas-grado/{asignatura_grado_id}/actividades-formativas`. Vive en la pantalla de detalle de `AsignaturaGrado` ([`abrirAsignaturaGrado()`](/RUP/03-diseño/casos-uso/abrirAsignaturaGrado/README.md)).
- **API**: `routers/asignatura_grado.py::listar_actividades_formativas(asignatura_grado_id)` / `::editar_actividades_formativas(asignatura_grado_id, datos)` -- auth `get_current_director_grado_id` + `_verificar_asignatura_grado_del_director`.
- **Modelo**: `ActividadFormativaAsignaturaGrado.actualizar(horas, porcentaje_presencialidad)`.
- **Repositorio**: `ActividadFormativaAsignaturaGradoRepository.listar_de(asignatura_grado_id)` / `.actualizar_lote(filas)`.

## Contrato de endpoint

### GET `/api/v1/asignaturas-grado/{asignatura_grado_id}/actividades-formativas`

**Response (200 OK):** lista de 10 objetos `{ actividad_formativa_id, codigo, nombre, horas, porcentaje_presencialidad }`, ordenados por `codigo`.

**Response (404 Not Found):** `AsignaturaGrado` inexistente o no dirigida por el `DirectorGrado`.

### PUT `/api/v1/asignaturas-grado/{asignatura_grado_id}/actividades-formativas`

**Request body:** `{ "actividades": [ { "actividad_formativa_id": int, "horas": number, "porcentaje_presencialidad": number }, ... ] }`.

**Response (200 OK):** la lista actualizada.

**Response (422 Unprocessable Entity):**
```json
{ "detail": "porcentaje_presencialidad debe estar entre 0 y 100" }
```
o `horas` negativa, o `actividad_formativa_id` fuera de catálogo / duplicado. Nada se persiste.

**Response (404 Not Found):** `AsignaturaGrado` inexistente o ajena.

## Decisiones de diseño

- **`porcentaje_presencialidad` es `Numeric(5, 2)`** con validación de rango `[0, 100]` en el schema (Pydantic `ge=0, le=100`) y cinturón en el modelo. Es el único campo del clúster con cota -- se corresponde con un porcentaje real del formulario oficial.
- **Mismas decisiones de forma que `editarActividadesFormativasMateria()`**: URL de colección sin id de fila, `PUT` transaccional con `rollback` en `422`, sin `HistorialCambio`, la regla `AfM = Σ AfAdM` fuera de este endpoint.
- **Nivel consumido por el render de la `Guia`**: `render/guia_docente.py` deja de usar la constante `_ACTIVIDADES_FORMATIVAS` y lee `guia.asignatura_grado` -> filas `ActividadFormativaAsignaturaGrado` (las 10, con `horas` y `porcentaje_presencialidad`) para la sección 4 del formulario oficial. Ese cambio del render va en el PR posterior (junto al medidor), sobre tablas ya pobladas en producción -- ver fichas de Desarrollo de [`descargarGuiaPDF()`](/RUP/04-desarrollo/casos-uso/descargarGuiaPDF/README.md) / [`previsualizarGuia()`](/RUP/04-desarrollo/casos-uso/previsualizarGuia/README.md).
- **Tabla nueva `actividades_formativas_asignatura_grado`** (`asignatura_grado_id` PK/FK, `actividad_formativa_id` PK/FK, `horas`, `porcentaje_presencialidad`). Autopoblado a 0 al crear la `AsignaturaGrado` (`crear()` del repositorio, `seed_grado.py`, backfill de migración) -- ver [modelo de datos](/RUP/03-diseño/modelo-datos/README.md).

## Referencias

- [`editarActividadesFormativasAsignaturaGrado()` en Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaGrado/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaGrado/README.md).
- [`editarActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) -- el mismo patrón un nivel arriba.

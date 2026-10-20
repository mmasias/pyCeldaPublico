<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarActividadesFormativasAsignaturaPrograma() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarActividadesFormativasAsignaturaPrograma()`](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md): mismo patrón que [`editarActividadesFormativasMateria()`](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) sobre la asociación `ActividadFormativaAsignaturaPrograma`, solo con `horas`. La respuesta añade a cada fila el `porcentaje_presencialidad` de la `Materia` de la asignatura, de solo lectura (issue [#772](https://github.com/mmasias/pyCelda/issues/772)). `GET` + `PUT` sobre la misma URL; `<<choice>>` de validación de entrada = `422` sin persistir.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadesFormativasAsignaturaPrograma` (React) -- rejilla con una fila por actividad del catálogo del programa, `codigo`/`nombre` de solo lectura, `horas` editable, columna "% presencialidad (de la materia)" de solo lectura; `GET` + `PUT /api/v1/asignaturas-programa/{asignatura_programa_id}/actividades-formativas`. Se entra desde la ficha de `AsignaturaPrograma` ([`abrirAsignaturaPrograma()`](/RUP/03-diseño/casos-uso/abrirAsignaturaPrograma/README.md)).
- **API**: `routers/asignatura_programa.py::listar_actividades_formativas_asignatura_programa(asignatura_programa_id)` / `::editar_actividades_formativas_asignatura_programa(asignatura_programa_id, datos)` -- auth `get_current_director_programa_id` + `_verificar_asignatura_programa_del_director`; `_materia_id_de()` para leer la presencialidad.
- **Modelo**: `ActividadFormativaAsignaturaPrograma.actualizar(horas)`.
- **Comprobación por ECTS en la Vista** (issue [#786](https://github.com/mmasias/pyCelda/issues/786)): `comprobarHorasAsignatura(ects, horas)` (`frontend/src/horasEcts.ts`), espejo en TypeScript de `AsignaturaPrograma.comprobacion_horas_ects()`, sobre las horas tecleadas; la pinta el mismo `LineaHorasEcts` de la ficha. `ects` sale del detalle de la asignatura (`GET /api/v1/asignaturas-programa/{id}`, que la Vista ya pide para el nombre).
- **Repositorio**: `ActividadFormativaAsignaturaProgramaRepository.listar_de(asignatura_programa_id)` / `.guardar()`; `presencialidad_de_la_materia(db, materia_id)` y `serializar_actividades_formativas_asignatura_programa(db, materia_id, filas)` en `repositories/actividad_formativa.py`.

## Contrato de endpoint

### GET `/api/v1/asignaturas-programa/{asignatura_programa_id}/actividades-formativas`

**Response (200 OK):** lista de `{ actividad_formativa_id, codigo, nombre, horas, porcentaje_presencialidad }`, una por actividad del catálogo del `Programa`, en orden de alta. `porcentaje_presencialidad` es el de la `Materia` (0 si no tiene fila, caso que el autopoblado impide).

**Response (404 Not Found):** `AsignaturaPrograma` inexistente o no dirigida por el `DirectorPrograma`.

### PUT `/api/v1/asignaturas-programa/{asignatura_programa_id}/actividades-formativas`

**Request body:** `{ "actividades": [ { "actividad_formativa_id": int, "horas": number }, ... ] }`. Un `porcentaje_presencialidad` en una fila se ignora (no forma parte de `ActividadFormativaAsignaturaProgramaItem`).

**Response (200 OK):** la lista actualizada, mismo shape que el `GET`.

**Response (422 Unprocessable Entity):** `horas` negativa (Pydantic), o `actividad_formativa_id` fuera de catálogo / duplicado (router). Nada se persiste.

**Response (404 Not Found):** `AsignaturaPrograma` inexistente o ajena.

## Decisiones de diseño

- **Presencialidad en la respuesta, no en la tabla**: `ActividadFormativaAsignaturaProgramaResponse` conserva `porcentaje_presencialidad` para que la Vista, la ficha de la asignatura y `abrirGuia()` sigan recibiendo la misma forma; el valor sale de `ActividadFormativaMateria` vía `serializar_actividades_formativas_asignatura_programa()`, compartido con `routers/guia.py`.
- **Ignorar, no rechazar, la presencialidad del body**: un cliente antiguo que la siga enviando no recibe `422`; simplemente no tiene efecto.
- **Mismas decisiones de forma que `editarActividadesFormativasMateria()`**: URL de colección sin id de fila, `PUT` transaccional, sin `HistorialCambio`, la regla `AfM = Σ AfAdM` fuera de este endpoint.
- **Nivel consumido por el render de la `Guia`**: `render/guia_docente.py` lee las filas `ActividadFormativaAsignaturaPrograma` de `guia.asignatura_programa` para las horas de la sección 4, y la presencialidad de `materia.actividades_formativas` -- ver fichas de Desarrollo de `descargarGuiaPDF()` / `previsualizarGuia()`.
- **Tabla `actividades_formativas_asignatura_programa`** (`asignatura_programa_id` PK/FK, `actividad_formativa_id` PK/FK, `horas`). Autopoblado a 0 al crear la `AsignaturaPrograma` (`crear()` del repositorio, `seed_programa.py`) y al crear una actividad del programa -- ver [modelo de datos](/RUP/03-diseño/modelo-datos/README.md).
- **Total frente a ECTS calculado en la Vista** (#786): se recalcula a cada pulsación, antes de guardar, sin ida y vuelta al servidor -- mismo criterio que el total de [`editarActividadesFormativasMateria()`](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md). El cálculo se duplica (Python en el modelo, TypeScript en la Vista) con las mismas reglas: sin `ects` no hay comprobación, redondeo a dos decimales, `sin_horas` si la suma es 0. Informativo: no entra en la validación del `PUT`.
- **Histórico**: hasta #772 la tabla tenía también `porcentaje_presencialidad` (`Numeric(5, 2)`, rango 0-100 en el schema) y el `PUT` lo editaba; la migración `migrar_catalogos_por_programa.py` lo movió a `actividades_formativas_materia`.

**Actor `Admin` (issue [#599](https://github.com/mmasias/pyCelda/issues/599))**: endpoint espejo bajo `/api/v1/admin/...` (`GET`/`PUT /api/v1/admin/asignaturas-programa/{id}/actividades-formativas`), autenticado con `require_admin` en vez de `get_current_director_programa_id` + comprobación de propiedad; reutiliza sin cambios los mismos métodos de repositorio. La secuencia es idéntica con `Admin` como actor.

## Referencias

- [`editarActividadesFormativasAsignaturaPrograma()` en Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md).
- [`editarActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/README.md) -- el mismo patrón un nivel arriba, donde se edita la presencialidad.

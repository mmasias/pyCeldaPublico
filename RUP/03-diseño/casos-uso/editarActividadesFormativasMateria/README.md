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
- **Versión**: 2.0
- **Fecha**: 2026-10-17
- **Autor**: Claude (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarActividadesFormativasMateria()`](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md): rejilla de un submit sobre las filas `ActividadFormativaMateria` de una `Materia` -- una por cada `ActividadFormativa` del catálogo de su `Programa` --, con `horas` y `porcentaje_presencialidad` (issue [#772](https://github.com/mmasias/pyCelda/issues/772)). Dos interacciones de Análisis (`cargarActividadesFormativas` + `guardarActividadesFormativas`) sobre la misma URL: `GET` + `PUT`. `<<choice>>` de validación de entrada = `422` sin persistir nada.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarActividadesFormativasMateria/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarActividadesFormativasMateria` (React) -- rejilla con una fila por actividad del catálogo del programa, `codigo`/`nombre` de solo lectura, `horas` y `porcentaje_presencialidad` editables (numéricos, decimales); total de horas frente a `ects × 25` si la `Materia` tiene `ects`. `GET /api/v1/materias/{materia_id}` (para `ects`) + `GET`/`PUT /api/v1/materias/{materia_id}/actividades-formativas`. Se entra desde la ficha de `Materia` ([`abrirMateria()`](/RUP/03-diseño/casos-uso/abrirMateria/README.md)).
- **API**: `routers/materia.py::listar_actividades_formativas_materia(materia_id)` / `::editar_actividades_formativas_materia(materia_id, datos)` -- funciones sueltas, auth `get_current_director_programa_id` + `_verificar_materia_del_director` (mismo guard que el resto de self-loops de `MATERIA_ABIERTO`); cuerpo común `_editar_actividades_formativas_materia()`.
- **Modelo**: `ActividadFormativaMateria.actualizar(horas, porcentaje_presencialidad=None)`.
- **Repositorio**: `ActividadFormativaMateriaRepository.listar_de(materia_id)` / `.guardar()`.

## Contrato de endpoint

### GET `/api/v1/materias/{materia_id}/actividades-formativas`

**Response (200 OK):** lista de `{ actividad_formativa_id, codigo, nombre, horas, porcentaje_presencialidad }`, una por actividad del catálogo del `Programa`, en orden de alta del catálogo.

**Response (404 Not Found):** `{ "detail": "Materia no encontrada" }` -- `Materia` inexistente o no dirigida por el `DirectorPrograma`.

### PUT `/api/v1/materias/{materia_id}/actividades-formativas`

**Request body:** `{ "actividades": [ { "actividad_formativa_id": int, "horas": number, "porcentaje_presencialidad": number | null }, ... ] }` -- cada entrada actualiza su fila por `actividad_formativa_id`; las no enviadas quedan como estaban; sin `porcentaje_presencialidad` en una entrada, se conserva el de la fila.

**Response (200 OK):** la lista completa actualizada, mismo shape que el `GET`.

**Response (422 Unprocessable Entity):** `horas` negativa o `porcentaje_presencialidad` fuera de 0-100 (Pydantic), o `actividad_formativa_id` fuera del catálogo de la `Materia` / duplicado (router). **Nada se persiste** (validación antes de tocar la BD).

**Response (404 Not Found):** `Materia` inexistente o ajena.

## Decisiones de diseño

- **URL sin id de la fila de asociación**: `ActividadFormativaMateria` no tiene id propio (PK compuesta `(materia_id, actividad_formativa_id)`). El recurso es "las actividades formativas de esta `Materia`" como conjunto -- `GET`/`PUT` de la colección entera, no de una fila. Paralelo al patrón `sincronizar_*` de `Guia` (un `PUT` con la lista final), no al `PUT /{sub_id}` de `editarAsociacionMetodologiaDocenteMateria()`.
- **`PUT` transaccional**: aplica todas las actualizaciones en una sola transacción; si algún valor no es válido o un `actividad_formativa_id` no está en el catálogo, `422` -- el reparto no queda a medias.
- **`porcentaje_presencialidad` opcional por fila** (#772): `None` conserva el valor de la fila, para que un cliente que solo reparte horas no borre la presencialidad. La Vista envía siempre los dos.
- **`horas` y `porcentaje_presencialidad` son `Numeric`** (mismo criterio que `ects`/`ponderacion`): admiten decimales. `horas` sin cota superior -- la suma frente a ECTS no se valida, solo se informa (`Materia.comprobacion_horas_ects()`, ver [`consultarEstadoActividadesFormativasMateria()`](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md)); la Vista hace el mismo cálculo en vivo mientras se teclea.
- **La regla `AfM = Σ AfAdM` no se toca aquí**: es responsabilidad del medidor blando. Guardar un reparto que aún no cuadra es válido.
- **Sin `HistorialCambio`**: `editarMateria()`/`editarAsignaturaPrograma()` tampoco lo generan -- `HistorialCambio` es del agregado `Guia`. Consistente.
- **Autopoblado**: las filas por `Materia` se crean a 0 (horas y presencialidad) en `MateriaRepository.crear()`, en `ActividadFormativaRepository.crear()` para las materias existentes del programa, en `seed_programa.py` y en la migración `migrar_catalogos_por_programa.py` (ver [modelo de datos](/RUP/03-diseño/modelo-datos/README.md)). La rejilla nunca crea ni borra filas.
- **Histórico**: hasta #772 la tabla `actividades_formativas_materia` solo tenía `horas` (la presencialidad estaba en `actividades_formativas_asignatura_programa`) y la rejilla tenía las 10 filas del catálogo de la `Universidad`.

**Actor `Admin` (issue [#755](https://github.com/mmasias/pyCelda/issues/755))**: endpoint espejo bajo `/api/v1/admin/...` (`GET`/`PUT /api/v1/admin/materias/{id}/actividades-formativas`), autenticado con `require_admin` en vez de `get_current_director_programa_id` + comprobación de propiedad; el cuerpo del `PUT` es común a los dos actores (`_editar_actividades_formativas_materia`). La secuencia es idéntica con `Admin` como actor.

## Referencias

- [`editarActividadesFormativasMateria()` en Análisis](/RUP/02-analisis/casos-uso/editarActividadesFormativasMateria/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarActividadesFormativasMateria/README.md).
- [`editarActividadesFormativasAsignaturaPrograma()` en Diseño](/RUP/03-diseño/casos-uso/editarActividadesFormativasAsignaturaPrograma/README.md) -- mismo patrón solo con `horas`; presenta de solo lectura la presencialidad de la `Materia`.
- [`consultarEstadoActividadesFormativasMateria()` en Diseño](/RUP/03-diseño/casos-uso/consultarEstadoActividadesFormativasMateria/README.md) -- el medidor de la regla `AfM = Σ AfAdM`.

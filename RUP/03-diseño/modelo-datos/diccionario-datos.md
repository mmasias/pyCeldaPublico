<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>[*Dashboard de seguimiento*](/RUP/99-seguimiento/README.md)</sub>

</div>

# Diccionario de datos

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-01
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Vista relacional del almacén de datos (SQLite + SQLAlchemy, 23 tablas), complemento del [diagrama de clases de diseño](/RUP/03-diseño/diagrama-clases-diseño.puml) (vista OO, Fat Model). Documenta lo que la vista OO deja invisible: las 6 tablas de unión, las columnas FK reales y su nulabilidad, qué asociación es FK física y cuál lógica, tipos y defaults declarados. El diagrama entidad-relación que acompaña a este diccionario está en [`DER.puml`](DER.puml).

Nivel **lógico-físico híbrido**: los tipos se dan al nivel que declara SQLAlchemy (`String(20)`, `Numeric(4, 1)`, `Text`, `Integer`, `DateTime`, `Boolean`), sin bajar a las storage classes de SQLite.

## Dos capas, dos regímenes de mantenimiento

- **Capa estructural** (secciones por tabla, al final): **generada** por `backend/app/scripts/generar_modelo_datos.py` a partir de `SQLAlchemy.metadata`. Va entre los dos marcadores HTML `BEGIN GENERADO` / `END GENERADO`. No se edita a mano -- regenerar la reescribe entera.
- **Capa de intención de diseño** (la sección de aquí abajo y las notas del DER): escrita **a mano**, fuera de los marcadores. Recoge lo que `SQLAlchemy.metadata` no sabe -- dominios de los enum, FK lógica vs física, denormalizaciones, reglas de consistencia -- enlazando al [README del modelo de dominio](/RUP/00-modelo-del-dominio/README.md) en vez de reexplicar el "por qué".

Regla de mantenimiento: **un PR que toca `backend/app/models/` regenera el DER y este diccionario y revisa la capa de intención** -- misma obligación que actualizar el README del modelo de dominio. `generar_modelo_datos.py --check` falla si hay drift.

## Capa de intención de diseño

### Dominios de los enum (validados en capa de aplicación, no en el esquema)

Ninguna de estas columnas tiene `CHECK` ni tabla de catálogo en el esquema -- el dominio lo impone Pydantic / la lógica de negocio.

| columna | dominio | dónde se valida / referencia |
|---|---|---|
| `grados.estado`, `asignaturas.estado` | `{Vigente, Extinguido}` | [borrado lógico](/RUP/00-modelo-del-dominio/README.md) -- "Nada del catálogo se borra físicamente" |
| `asignaturas_grado.estado` | `{Activo, Extinguido}` | el código nace `'Activo'`; el README del modelo lo describe como Vigente/Extinguido -- discrepancia real de nomenclatura, no de comportamiento |
| `guias.estado` | `{Borrador, EnRevision, Aprobada, Rechazada}` | [diagrama de estados de Guia](/RUP/00-modelo-del-dominio/estados-entidades/guia.puml) |
| `sistemas_evaluacion.tipo` | `{Evaluación continua, Evaluación final}` | [modelo de dominio, `SistemaEvaluacion.tipo`](/RUP/00-modelo-del-dominio/README.md) (issue #14) |
| `resultados_aprendizaje.tipo` | `{Conocimientos o contenidos, Habilidades o destrezas, Competencias o capacidades, General}` | [modelo de dominio, `ResultadoAprendizaje`](/RUP/00-modelo-del-dominio/README.md) |
| `referencias_bibliograficas.tipo` | `{Basica, Complementaria, WebsReferencia, OtrasFuentes}` | [modelo de dominio, bibliografía](/RUP/00-modelo-del-dominio/README.md) -- el enum guarda el nombre técnico, la UI muestra la forma legible |
| `sesiones.tipo` | `{CLASE_TEORICA, CLASE_PRACTICA, CLASE_TEORICO_PRACTICA, CLASE_LABORATORIO, EVALUACION_CONTINUA, EVALUACION_PARCIAL}` | [modelo de dominio, `Sesion.tipo`](/RUP/00-modelo-del-dominio/README.md) (discussion #140; 6º valor `CLASE_TEORICO_PRACTICA` en la [#198](https://github.com/mmasias/pyCelda/discussions/198)) |
| `historial_cambios.campo` | `{estado, contenido}` | `estado` desde el origen; `contenido` desde la [discussion #191](https://github.com/mmasias/pyCelda/discussions/191) |
| `asignaturas_grado.caracter` | texto libre en la práctica (`Básica`, `Obligatoria`, `Optativa`, ...) | dato del plan de estudios, sin enum cerrado |

### FK lógicas (asociación del dominio sin restricción física en el esquema)

| asociación | representación física | por qué |
|---|---|---|
| `Guia` -> `Grado` (`guias.grado_id`) | columna `Integer` nullable, **sin `FOREIGN KEY`** | denormalización: `grado_id` es derivable vía `asignatura_grado.materia.grado`; se guarda para las guías que nacen sin `AsignaturaGrado`. Ver [modelo de dominio](/RUP/00-modelo-del-dominio/README.md) |
| `HistorialCambio` -> autor (`historial_cambios.autor_id`) | columna `Integer`, **sin `FOREIGN KEY`** | FK polimórfica: el autor es `Profesor`, `DirectorGrado` o `Admin` -- el modelo lo resuelve por `Actor -> HistorialCambio`, no hay una tabla `actores` única |
| `AsignaturaGrado` -> `Grado` (`AsignaturaGrado.grado_id`) | **no es columna**: `@property` que devuelve `materia.grado_id` | la pertenencia al grado va por `materia`, no se duplica |

`AsignaturaGrado` -> `Asignatura` (`asignaturas_grado.asignatura_id`) **ya no es FK lógica**: es FK física real y nullable desde el [issue #181](https://github.com/mmasias/pyCelda/issues/181) / [PR #250](https://github.com/mmasias/pyCelda/pull/250) -- ver la nota de `asignaturas_grado` en el [DER](DER.puml) (capa generada) para el porqué de la nulabilidad.

### Denormalizaciones

| columna | qué duplica | por qué |
|---|---|---|
| `guias.grado_id` | `guia.asignatura_grado.materia.grado_id` | ver arriba, FK lógicas |
| `directores_grado.email` | `profesor.email` (el dominio modela `DirectorGrado -\|> Profesor`) | esta tabla no reproduce la herencia como joined-table inheritance -- solo resuelve el email de sesión contra "es DirectorGrado" o "es Profesor" de forma independiente ([#62](https://github.com/mmasias/pyCelda/issues/62)) |
| `historial_cambios.valor_anterior` / `valor_nuevo` (`String(50)`) | un resumen del valor real | para `campo="contenido"` el temario completo no cabe ni interesa en la auditoría -- el detalle vive en `guias.contenido` ([discussion #191](https://github.com/mmasias/pyCelda/discussions/191)) |

### Inconsistencias de declaración (no de comportamiento)

- `asignaturas.contenido` es `String` **sin longitud** (VARCHAR ilimitado), mientras que `asignaturas_grado.contenido` y `guias.contenido` son `Text`. El "espejo" del que habla la discussion #191 es semántico; la columna más antigua nunca se homogeneizó. SQLite no distingue, así que no hay efecto práctico.
- `asignaturas_grado.estado` nace `'Activo'` en el código; el README del modelo de dominio lo enuncia como `Vigente`/`Extinguido`.

### Reglas de consistencia no representadas en el esquema

Todas viven en la capa de aplicación y están razonadas en el [README del modelo de dominio](/RUP/00-modelo-del-dominio/README.md):

- `(Grado, Asignatura)` es único -- una asignatura no aparece dos veces en el mismo grado.
- La suma de `ponderacion` de las `PonderacionEvaluacion` de una guía da 100%, y la suma por `SistemaEvaluacion` cae en su rango `[ponderacion_minima, ponderacion_maxima]`.
- Una `Guia` no puede enviarse a revisión con menos de `guias.sesiones_minimas` `Sesion` vinculadas (regla c3 de `enviarGuiaARevision`, [discussion #206](https://github.com/mmasias/pyCelda/discussions/206)); `guias.sesiones_minimas` es un snapshot de `asignaturas_grado.sesiones_minimas` (config editable por Admin, cota 1-100) al nacer la guía.
- Los `ResultadoAprendizaje` de una `AsignaturaGrado` son subconjunto de los de su `Materia`.
- El `SistemaEvaluacion` de cada `PonderacionEvaluacion` pertenece a la misma `Materia` que la `AsignaturaGrado` de la guía.
- Un `Grado` no puede quedarse sin ningún `DirectorGrado`.
- Las notificaciones al profesor se filtran por `Guia.semestre == CursoAcademico.semestreActivo` (`CursoAcademico` aún no está en el esquema).

### Restricciones reales en el esquema

Solo dos: `email` con `UNIQUE` + índice en `profesores` y en `directores_grado`. Ninguna otra tabla tiene `UNIQUE`, `CHECK` ni índice explícito. Las PK compuestas de las 6 tablas de unión (y de `metodologias_materia`) son la única otra garantía estructural.

### Entidades del dominio sin tabla

- **`CursoAcademico`** (y su relación con `Universidad`): en el modelo de dominio pero **no tiene tabla** -- el ciclo de curso académico no se ha construido todavía. `Guia` es clase de asociación de `(AsignaturaGrado, CursoAcademico)` en el dominio; en el esquema solo lleva `asignatura_grado_id`.
- **`PlanificacionDocente`** (renombrado de `Cronograma`, discussion [#198](https://github.com/mmasias/pyCelda/discussions/198)): el [modelo de dominio](/RUP/00-modelo-del-dominio/README.md) la separa como entidad propia (`Guia *-- PlanificacionDocente` 1:1, `PlanificacionDocente *-- Sesion` 1:N -- "no `Guia *-- Sesion` directo", discussion [#140](https://github.com/mmasias/pyCelda/discussions/140)). En el esquema está **colapsada**: `sesiones.guia_id` apunta directamente a `guias`, sin tabla `planificaciones_docentes` intermedia. La composición 1:1 no aporta una fila propia y se resuelve como FK directa Sesion -> Guia.

---

## Capa estructural (generada)

<!-- BEGIN GENERADO -- introspección de SQLAlchemy.metadata, no editar a mano -->

### Estructura curricular

#### `universidades`

Institución. Hoy mono-institucional, pero modelada como entidad real.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `nombre` | String(200) | no | -- | -- | -- | -- |

#### `facultades`

Facultad de una universidad.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `nombre` | String(200) | no | -- | -- | -- | -- |
| `universidad_id` | Integer | no | -- | FK -> universidades.id | -- | -- |

#### `grados`

Grado (titulación). `codigo` es identificador de catálogo (ej. GII).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `codigo` | String(20) | no | -- | unique | -- | -- |
| `nombre` | String(200) | no | -- | -- | -- | -- |
| `estado` | String(20) | no | 'Vigente' | -- | {Vigente, Extinguido} | -- |
| `facultad_id` | Integer | sí | -- | FK -> facultades.id | -- | -- |

#### `materias`

Agrupación de asignaturas dentro del plan de un grado.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `nombre` | String(200) | no | -- | -- | -- | -- |
| `grado_id` | Integer | sí | -- | FK -> grados.id | -- | nullable a nivel de columna; en la práctica siempre presente |

#### `asignaturas`

Catálogo institucional plano de asignaturas (nombre/ects/contenido por defecto).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `codigo` | String(20) | sí | -- | unique | -- | nullable a nivel de columna (placeholder legado de seed_asignaturas_desde_asignatura_grado.py sin reconciliar, issue #181); crearAsignatura lo exige vía Pydantic, fijo tras el alta |
| `nombre` | String(200) | no | -- | -- | -- | -- |
| `ects` | Integer | sí | -- | -- | -- | -- |
| `contenido` | String | no | '' | -- | -- | String sin longitud (VARCHAR ilimitado); asignaturas_grado.contenido y guias.contenido son Text -- inconsistencia de declaración |
| `estado` | String(20) | no | 'Vigente' | -- | {Vigente, Extinguido} | -- |

#### `asignaturas_grado`

Concreción de una asignatura en el plan de un grado (clase de asociación (Grado, Asignatura)).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `materia_id` | Integer | no | -- | FK -> materias.id | -- | -- |
| `asignatura_id` | Integer | sí | -- | FK -> asignaturas.id | -- | -- |
| `nombre` | String(200) | no | -- | -- | -- | -- |
| `curso` | Integer | no | -- | -- | -- | -- |
| `caracter` | String(50) | no | -- | -- | -- | -- |
| `idioma` | String(50) | no | -- | -- | -- | -- |
| `ects` | Numeric(4, 1) | no | -- | -- | -- | -- |
| `semestre_default` | Integer | no | -- | -- | -- | -- |
| `contenido` | Text | no | '' | -- | -- | semilla del temario al nacer la Guia (discussion #191) |
| `requisitos_previos` | Text | sí | -- | -- | -- | texto plano; render en vivo de la guía (sección 2) y editable por DirectorGrado en editarAsignaturaGrado; NULL normaliza la familia "No aplica" en el backfill; congelado retroactivo compartido con RA en #219 (discussion #259, ítem 2 de #217) |
| `sesiones_minimas` | Integer | no | 25 | -- | 1-100 (validado en el router) | mínimo de Sesion vinculadas para enviar la Guia a revisión (regla c3, discussion #206); config editable por Admin |
| `estado` | String(20) | no | 'Activo' | -- | {Activo, Extinguido} | el modelo de dominio lo describe como Vigente/Extinguido; el código nace 'Activo' |

#### `sistemas_evaluacion`

Categoría de evaluación de una materia, con su rango de ponderación.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `materia_id` | Integer | no | -- | FK -> materias.id | -- | -- |
| `tipo` | String(50) | no | -- | -- | {Evaluación continua, Evaluación final} | -- |
| `descripcion` | String(200) | no | -- | -- | -- | -- |
| `ponderacion_minima` | Numeric(5, 2) | no | -- | -- | -- | -- |
| `ponderacion_maxima` | Numeric(5, 2) | no | -- | -- | -- | -- |

#### `metodologias_docentes`

Catálogo institucional de metodologías docentes (MD1-MD7).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `codigo` | String(20) | no | -- | -- | -- | -- |
| `descripcion` | String(500) | no | -- | -- | -- | -- |

#### `metodologias_materia`

Asociación (Materia, MetodologiaDocente) con descripción propia opcional.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `materia_id` | Integer | no | -- | PK,FK -> materias.id | -- | -- |
| `metodologia_docente_id` | Integer | no | -- | PK,FK -> metodologias_docentes.id | -- | -- |
| `descripcion_propia` | Text | no | '' | -- | -- | -- |

#### `resultados_aprendizaje`

Resultado de aprendizaje del catálogo de un grado (código + tipo + descripción).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `grado_id` | Integer | no | -- | FK -> grados.id | -- | -- |
| `codigo` | String(20) | no | -- | -- | -- | -- |
| `tipo` | String(50) | no | -- | -- | {Conocimientos o contenidos, Habilidades o destrezas, Competencias o capacidades, General} | -- |
| `descripcion` | String(500) | no | -- | -- | -- | -- |

#### `materias_resultados_aprendizaje`

Unión N:M Materia-ResultadoAprendizaje (reparto en cascada Grado->Materia).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `materia_id` | Integer | no | -- | PK,FK -> materias.id | -- | -- |
| `resultado_aprendizaje_id` | Integer | no | -- | PK,FK -> resultados_aprendizaje.id | -- | -- |

#### `asignaturas_grado_metodologias_docentes`

Unión N:M AsignaturaGrado-MetodologiaDocente.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `asignatura_grado_id` | Integer | no | -- | PK,FK -> asignaturas_grado.id | -- | -- |
| `metodologia_docente_id` | Integer | no | -- | PK,FK -> metodologias_docentes.id | -- | -- |

#### `asignaturas_grado_resultados_aprendizaje`

Unión N:M AsignaturaGrado-ResultadoAprendizaje (subconjunto de las de su materia).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `asignatura_grado_id` | Integer | no | -- | PK,FK -> asignaturas_grado.id | -- | -- |
| `resultado_aprendizaje_id` | Integer | no | -- | PK,FK -> resultados_aprendizaje.id | -- | -- |

#### `asignaturas_grado_profesores`

Unión N:M AsignaturaGrado-Profesor: profesorado asignado como plantilla estable.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `asignatura_grado_id` | Integer | no | -- | PK,FK -> asignaturas_grado.id | -- | -- |
| `profesor_id` | Integer | no | -- | PK,FK -> profesores.id | -- | -- |

#### `actividades_formativas`

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `codigo` | String(10) | no | -- | -- | -- | -- |
| `nombre` | String(200) | no | -- | -- | -- | -- |

#### `actividades_formativas_materia`

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `materia_id` | Integer | no | -- | PK,FK -> materias.id | -- | -- |
| `actividad_formativa_id` | Integer | no | -- | PK,FK -> actividades_formativas.id | -- | -- |
| `horas` | Numeric(6, 2) | no | 0 | -- | -- | -- |

#### `actividades_formativas_asignatura_grado`

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `asignatura_grado_id` | Integer | no | -- | PK,FK -> asignaturas_grado.id | -- | -- |
| `actividad_formativa_id` | Integer | no | -- | PK,FK -> actividades_formativas.id | -- | -- |
| `horas` | Numeric(6, 2) | no | 0 | -- | -- | -- |
| `porcentaje_presencialidad` | Numeric(5, 2) | no | 0 | -- | -- | -- |

#### `cursos_academicos`

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `inicio` | Date | no | -- | -- | -- | -- |
| `fin` | Date | no | -- | -- | -- | -- |
| `estado` | String(20) | no | 'Inactivo' | -- | -- | -- |
| `universidad_id` | Integer | sí | -- | FK -> universidades.id | -- | -- |
| `semestre_activo` | Integer | sí | -- | -- | -- | -- |

### Guía docente

#### `guias`

Guía docente: clase de asociación (AsignaturaGrado, CursoAcademico), fase de impartición.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `estado` | String(20) | no | 'Borrador' | -- | {Borrador, EnRevision, Aprobada, Rechazada} | -- |
| `semestre` | Integer | sí | -- | -- | -- | -- |
| `contenido` | Text | no | '' | -- | -- | apartado propio de la fase de impartición (discussion #191) |
| `sesiones_minimas` | Integer | no | 25 | -- | -- | snapshot de asignaturas_grado.sesiones_minimas al nacer la Guia (discussion #206), como semestre y contenido |
| `grado_id` | Integer | sí | -- | -- | -- | FK lógica, sin FK física; denormalizado |
| `asignatura_grado_id` | Integer | sí | -- | FK -> asignaturas_grado.id | -- | nullable: guías sin AsignaturaGrado (huérfanas históricas / del grado dirigido) |
| `curso_academico_id` | Integer | no | -- | FK -> cursos_academicos.id | -- | -- |
| `fecha_creacion` | DateTimeUTC | sí | (runtime) | -- | -- | -- |
| `fecha_ultima_modificacion` | DateTimeUTC | no | (runtime) | -- | -- | -- |
| `fecha_generacion_pdf` | DateTimeUTC | sí | -- | -- | -- | -- |

#### `ponderaciones_evaluacion`

Instrumento concreto de evaluación de una guía, apuntando a un SistemaEvaluacion.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `guia_id` | Integer | no | -- | FK -> guias.id | -- | -- |
| `sistema_evaluacion_id` | Integer | no | -- | FK -> sistemas_evaluacion.id | -- | -- |
| `descripcion` | String(200) | no | -- | -- | -- | -- |
| `ponderacion` | Numeric(5, 2) | no | -- | -- | -- | -- |
| `vinculada` | Boolean | no | False | -- | -- | False = pendiente en la lista de trabajo del cliente; True = oficial de la Guia |

#### `referencias_bibliograficas`

Entrada de bibliografía de una guía, dentro de las 4 categorías fijas.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `guia_id` | Integer | no | -- | FK -> guias.id | -- | -- |
| `tipo` | String(30) | no | -- | -- | {Basica, Complementaria, WebsReferencia, OtrasFuentes} | -- |
| `referencia` | String(500) | no | -- | -- | -- | -- |
| `vinculada` | Boolean | no | False | -- | -- | idem ponderaciones_evaluacion.vinculada |

#### `sesiones`

Sesión de la planificación docente de una guía (numerada, tipada).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `guia_id` | Integer | no | -- | FK -> guias.id | -- | -- |
| `numero` | Integer | no | -- | -- | -- | -- |
| `tipo` | String(30) | no | -- | -- | {CLASE_TEORICA, CLASE_PRACTICA, CLASE_TEORICO_PRACTICA, CLASE_LABORATORIO, EVALUACION_CONTINUA, EVALUACION_PARCIAL} | -- |
| `descripcion` | String(500) | no | -- | -- | -- | -- |
| `vinculada` | Boolean | no | False | -- | -- | idem ponderaciones_evaluacion.vinculada |

#### `historial_cambios`

Auditoría de cambios de estado y de contenido de una guía.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `guia_id` | Integer | no | -- | FK -> guias.id | -- | -- |
| `autor_id` | Integer | no | -- | -- | -- | FK lógica polimórfica (Profesor | DirectorGrado | Admin); sin FK física |
| `campo` | String(50) | no | -- | -- | {estado, contenido} | -- |
| `valor_anterior` | String(50) | no | -- | -- | -- | resumen del valor, no el texto completo |
| `valor_nuevo` | String(50) | no | -- | -- | -- | resumen del valor, no el texto completo |
| `comentario` | String(200) | sí | -- | -- | -- | -- |
| `fecha` | DateTimeUTC | no | (runtime) | -- | -- | -- |

#### `guias_profesores`

Unión N:M Guia-Profesor: quién impartió esa guía ese curso (copia puntual al nacer).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `guia_id` | Integer | no | -- | PK,FK -> guias.id | -- | -- |
| `profesor_id` | Integer | no | -- | PK,FK -> profesores.id | -- | -- |

### Personas y roles

#### `profesores`

Profesor, identificado por email (cuenta Google).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `email` | String(200) | no | -- | unique | -- | -- |
| `nombre` | String(200) | sí | -- | -- | -- | nullable a nivel de columna (filas de seed antiguas); crearProfesor/editarProfesor lo exigen vía Pydantic |
| `universidad_id` | Integer | sí | -- | FK -> universidades.id | -- | -- |

#### `directores_grado`

Director de grado, identificado por email.

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `email` | String(200) | no | -- | unique | -- | denormalizado: no reproduce DirectorGrado -|> Profesor como herencia |

#### `grados_directores_grado`

Unión N:M Grado-DirectorGrado (un grado puede tener varios directores).

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `grado_id` | Integer | no | -- | PK,FK -> grados.id | -- | -- |
| `director_grado_id` | Integer | no | -- | PK,FK -> directores_grado.id | -- | -- |

#### `perfiles_profesor_curso`

| columna | tipo | nulable | default | clave | dominio | nota |
|---|---|---|---|---|---|---|
| `id` | Integer | no | -- | PK | -- | -- |
| `profesor_id` | Integer | no | -- | FK -> profesores.id | -- | -- |
| `curso_academico_id` | Integer | no | -- | FK -> cursos_academicos.id | -- | -- |
| `validado` | Boolean | no | False | -- | -- | -- |
| `orcid` | String(19) | sí | -- | -- | -- | -- |
| `enlace_cvn` | String(300) | sí | -- | -- | -- | -- |
| `enlace_foto` | String(300) | sí | -- | -- | -- | -- |
| `enlace_scholar` | String(300) | sí | -- | -- | -- | -- |
| `es_doctor` | Boolean | no | False | -- | -- | -- |
| `universidad_doctorado` | String(200) | sí | -- | -- | -- | -- |
| `anio_doctorado` | Integer | sí | -- | -- | -- | -- |
| `programa_doctorado` | String(200) | sí | -- | -- | -- | -- |
| `mencion_internacional` | Boolean | no | False | -- | -- | -- |
| `nivel_acreditacion_siiu` | Integer | sí | -- | -- | -- | -- |
| `organismo_acreditador` | String(10) | sí | -- | -- | -- | -- |
| `organismo_acreditador_otro` | String(200) | sí | -- | -- | -- | -- |
| `num_sexenios` | Integer | no | 0 | -- | -- | -- |
| `anio_ultimo_sexenio` | Integer | sí | -- | -- | -- | -- |
| `tramitando_sexenio` | Boolean | no | False | -- | -- | -- |
| `num_quinquenios` | Integer | no | 0 | -- | -- | -- |
| `anio_ultimo_quinquenio` | Integer | sí | -- | -- | -- | -- |
| `biografia` | String(2000) | sí | -- | -- | -- | -- |
| `anios_experiencia_docente` | Integer | sí | -- | -- | -- | -- |
| `anios_experiencia_docente_virtual` | Integer | sí | -- | -- | -- | -- |
| `anios_experiencia_profesional` | Integer | sí | -- | -- | -- | -- |
| `anios_experiencia_investigadora` | Integer | sí | -- | -- | -- | -- |

<!-- END GENERADO -->

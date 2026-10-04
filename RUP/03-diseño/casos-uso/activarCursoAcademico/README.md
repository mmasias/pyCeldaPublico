<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > activarCursoAcademico() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/README.md)|[Análisis](/RUP/02-analisis/casos-uso/activarCursoAcademico/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-09-21
- **Autor**: Claude Sonnet 5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`activarCursoAcademico()`](/RUP/02-analisis/casos-uso/activarCursoAcademico/README.md): sin capa Service, `routers/curso_academico.py::activar_curso_academico()` verifica existencia (404) y elegibilidad (409) antes de delegar el efecto completo en `CursoAcademicoRepository.activar()`, transacción única. El `<<choice>>` de elegibilidad se resuelve con un método de consulta (`es_elegible_para_activar()`) que el router traduce a HTTP -- **sin excepciones de dominio**, mismo criterio que `FacultadRepository.tiene_programas_asociados()`/`eliminar_facultad()`: se revisó ese caso antes de diseñar este, en vez de inventar un código de estado nuevo.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/activarCursoAcademico/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `ActivarCursoAcademicoView` (React) -- botón `[Activar]` por fila Inactiva elegible; al confirmar, `POST /api/v1/admin/cursos-academicos/{id}/activar`. **Sin pantalla propia en esta rebanada** (ver Desarrollo), igual que `crearCursoAcademico()`.
- **API**: `routers/curso_academico.py::activar_curso_academico(curso_academico_id)` -- función suelta, sin capa Service.
- **Repositorio**: `CursoAcademicoRepository` -- gana `ultimo()`, `penultimo()`, `activo()`, `tiene_actividad_registrada(id)`, `es_elegible_para_activar(id)` y `activar(id)`.

## Decisiones de diseño

- **`<<choice>>` de elegibilidad, sin excepción de dominio**: `es_elegible_para_activar(id)` devuelve `bool`; el router decide 404 (no existe) / 409 (existe pero no elegible) / delega en `activar()`. `activar()` no re-verifica elegibilidad -- confía en que el router ya la comprobó, mismo patrón que `FacultadRepository.eliminar()` (no re-verifica `tiene_programas_asociados()`).
- **Candidato "ya Activo" bloqueado explícitamente**: la redacción original del `<<choice>>` (discussion #15/#430) no lo menciona porque en la práctica el listado nunca ofrece `[Activar]` sobre la fila Activa (ver [`abrirCursosAcademicos()`](/RUP/01-requisitos/03-detalle-casos-uso/abrirCursosAcademicos/README.md)) -- pero la API debe ser robusta a una llamada directa: `es_elegible_para_activar()` exige `estado="Inactivo"` en el candidato, además de ser último/penúltimo. Sin esta guarda, reactivar el curso vigente repetiría el efecto colateral completo sobre sí mismo (`Guia` duplicadas) -- no es una regla de negocio nueva, es la lectura necesaria de "activar" un elemento que ya lo está.
- **`AsignaturaPrograma.estado="Extinguido"` no recibe `Guia` nueva**: no está en la letra de la especificación de este caso de uso, pero sí en el [modelo del dominio](/RUP/00-modelo-del-dominio/README.md) ya cerrado ("Extinguido bloquea altas nuevas") -- dar de alta una `Guia` para una `AsignaturaPrograma` extinguida sería precisamente eso, una alta nueva. Se filtra por `estado="Activo"` al listar las `AsignaturaPrograma` de la institución.
- **Contrato de clonado exacto, sin ampliarlo ni recortarlo**: `semestre`/`contenido`/`texto_sistema_evaluacion`/`sesiones_minimas` se clonan de la `Guia` anterior si existe (sin `Guia` anterior, `texto_sistema_evaluacion` nace `""`, sin fallback; issue #610); `ponderaciones`/`referencias` se copian fila a fila (nuevas filas, `vinculada` replicado tal cual); **`Sesion` (planificación docente real) nunca se clona** -- ni la especificación ni discussion #430 la mencionan, a diferencia de `sesiones_minimas` (umbral escalar, sí clonado). `profesorado` se deriva en vivo de `AsignaturaPrograma.profesorado` al nacer -- igual que `Guia._sincronizar_profesorado()`, nunca una copia del año anterior. `estado` nace siempre `"Borrador"`; `fecha_creacion`/`fecha_ultima_modificacion`/`fecha_generacion_pdf`/`historial` nacen siempre frescos.
- **Sin joins per-`AsignaturaPrograma`**: las `Guia` del curso que queda desactivado se precargan en un único `SELECT` (diccionario `asignatura_programa_id -> Guia`) antes del bucle, para no convertir la activación institucional entera en N+1 consultas.
- **Transacción única**: un solo `commit()` al final de `activar()` -- si algo falla a mitad (p.ej. un `IntegrityError` en cualquier `INSERT`), nada se aplica; ni la desactivación del curso anterior ni ninguna `Guia` parcial quedan persistidas.
- **Autorización de `Admin`: `Depends(require_admin)`** -- mismo criterio que el resto de endpoints de escritura de `Admin`.

## Migración

Ver `migrar_curso_academico_retroactivo.py` (Desarrollo) -- backfill real y completo, no de esquema puro: un único `CursoAcademico` retroactivo `Activo`, `Guia.curso_academico_id` `NOT NULL` desde el primer día, y reset de **todas** las `Guia` existentes a `Borrador` (decisión explícita de Manuel, discussion #430).

## Referencias

- [`activarCursoAcademico()` en Análisis](/RUP/02-analisis/casos-uso/activarCursoAcademico/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/activarCursoAcademico/README.md).
- [`eliminarFacultad()` en Diseño](/RUP/03-diseño/casos-uso/eliminarFacultad/README.md) -- plantilla del `<<choice>>` -> 409 sin excepción de dominio.
- [`crearFacultad()` en Diseño](/RUP/03-diseño/casos-uso/crearFacultad/README.md) -- plantilla del molde de Router/Repository sin capa Service.

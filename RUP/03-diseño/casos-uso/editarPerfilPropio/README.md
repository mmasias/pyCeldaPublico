<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPerfilPropio() > Diseño

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/README.md)|[Análisis](/RUP/02-analisis/casos-uso/editarPerfilPropio/README.md)|**Diseño**|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Información del artefacto

- **Proyecto**: pyCelda
- **Fase RUP**: Elaboración
- **Disciplina**: Diseño
- **Versión**: 1.0
- **Fecha**: 2026-10-03
- **Autor**: Claude Sonnet 5.5 (vía Claude Code)

## Propósito

Bajada a diseño del caso de análisis [`editarPerfilPropio()`](/RUP/02-analisis/casos-uso/editarPerfilPropio/README.md): dos endpoints sobre un recurso **sin identificador en la ruta** -- `GET /api/v1/mi-perfil` (carga, tres ramas) y `PUT /api/v1/mi-perfil` (guardado con *upsert* y validación de la fila del curso activo). El perfil siempre es el del `Profesor` de la sesión, así que no hay `404` por identificador ni riesgo de acceso cruzado por la ruta. Sin capa Service: `routers/mi_perfil.py` coordina `ProfesorRepository`, `CursoAcademicoRepository` y `PerfilProfesorCursoRepository`. La validación de forma y la limpieza de campos condicionales viven en el esquema Pydantic `MiPerfilUpdate`, no en el Router.

## Diagrama de secuencia de diseño

<div align=center>

|![](/images/RUP/03-diseño/casos-uso/editarPerfilPropio/secuencia.svg)|
|-|
|<div align=right><sup>Código fuente: [secuencia.puml](secuencia.puml)</sup></div>|

</div>

## Participantes

- **Vista**: `EditarPerfilPropioView` (`MiPerfil.tsx`, `/mi-perfil`) -- carga con `GET /api/v1/mi-perfil`; presenta el formulario completo y los avisos de las ramas de carga (sugerencia de curso anterior / primer curso sin validar); guarda con `PUT /api/v1/mi-perfil` y recarga el formulario con la respuesta ("Perfil actualizado"). Un `401`/`403` redirige a `/`.
- **API**: `routers/mi_perfil.py::obtener_mi_perfil()` / `editar_mi_perfil(datos)` -- funciones sueltas; helpers `_respuesta()` y `_respuesta_en_blanco()` construyen `MiPerfilResponse` campo a campo (la fila de perfil y el `Profesor` son entidades distintas, `from_attributes` no basta).
- **Modelo**: `Profesor.actualizar_nombre(nombre)`; `PerfilProfesorCurso.actualizar(**campos)` -- asigna los campos y marca siempre `validado = True`.
- **Repositorios**: `ProfesorRepository.obtener(profesor_id)`; `CursoAcademicoRepository.activo(universidad_id)` (reutilizado de [`activarCursoAcademico()`](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md)); `PerfilProfesorCursoRepository.obtener(profesor_id, curso_academico_id)`, `.obtener_mas_reciente(profesor_id)` y `.upsert(profesor_id, curso_academico_id, **campos)` -- este último hace `flush()` sin `commit()`.
- **Schemas**: `MiPerfilUpdate` (entrada, con los validadores) y `MiPerfilResponse` (salida, con `validado` y `sugerido_de_curso_anterior`).

## Decisiones de diseño

- **Ruta sin identificador (`/mi-perfil`), no `/profesores/{id}/perfil`**: el recurso es siempre el del `Profesor` autenticado (`get_current_profesor_id`). No hay `404` de identificador desconocido ni forma de apuntar al perfil de otro por la URL (historial de IDOR del proyecto #86/#96).
- **Tres ramas en el `GET`, resueltas contra el curso activo**: (1) fila del curso activo -- tal cual; (2) sin fila activa pero con una anterior (`obtener_mas_reciente()`, por `curso_academico_id` descendente, mismo criterio de "orden de alta == cronológico" que `CursoAcademicoRepository.ultimo()`) -- se sirve como sugerencia con `sugerido_de_curso_anterior = true` y `validado` **forzado a `false`** (los datos no están confirmados para el curso activo aunque lo estuvieran para el suyo); (3) ninguna fila -- formulario en blanco (`_respuesta_en_blanco()`). El `GET` no escribe nada.
- **`PUT` siempre sobre la fila del curso activo, con *upsert***: crea la fila si no existe; la unicidad `(profesor_id, curso_academico_id)` impide duplicados. `PerfilProfesorCurso.actualizar()` marca `validado = True` incondicionalmente: es el acto de confirmar/editar el que valida, no la mera existencia de la fila (la migración retroactiva siembra filas con `validado = False` a propósito). Ese `validado` alimenta el gate de la pantalla de inicio ([`abrirInicio()`](/RUP/03-diseño/casos-uso/abrirInicio/README.md)).
- **Un solo `commit()` en el Router, `flush()` en el repositorio**: `upsert()` no confirma; el Router actualiza `nombre`, hace el *upsert*, y confirma una vez al final (`commit()` + `refresh()` de la fila y del `Profesor`). Si algo falla antes, no queda escritura parcial.
- **`nombre` se escribe en `Profesor`, el resto en `PerfilProfesorCurso`**: `datos.model_dump(exclude={"nombre"})` separa ambos; el `email` nunca forma parte de `MiPerfilUpdate`.
- **Validación en servidor, no solo en el formulario** (`MiPerfilUpdate`, `422`): ORCID `^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$`; enlace CVN restringido a `https://*.fecyt.es/...cvnOnline...`; enlace de Scholar a `https://scholar.google.<tld>/citations?...user=...` (sin abrir la suplantación tipo `scholar.google.com.evil.com`); foto solo exige `https://`; `nivel_acreditacion_siiu` en `Literal[0..5]` (`None` = no informado, distinto de `0` = sin acreditación); `biografia` hasta 2000 caracteres; `organismo_acreditador_otro` obligatorio si `organismo_acreditador = "OTRO"` (un `PUT` directo con el detalle vacío se rechaza).
- **Limpieza de campos condicionales en servidor** (`model_validator`): sin `es_doctor`, se anulan universidad/año/programa/mención; sin acreditación (`None` o `0`), se anulan organismo y detalle; con `num_sexenios = 0`/`num_quinquenios = 0`, se anula el año del último. Ocultarlos en el formulario no basta: un `PUT` directo no pasa por la Vista.
- **Invariantes rotas como `RuntimeError`, no como error de negocio**: un `Profesor` sin `universidad_id`, o una `Universidad` sin `CursoAcademico` activo, no son estados que el cliente provoque ni resuelva -- se propagan como error de servidor, mismo criterio que `crear_asignatura_programa()`.
- **Privado esta tanda**: el perfil no aparece en `abrirGuia()`, `descargarGuiaPDF()` ni `previsualizarGuia()`.
- **Sin capa Service**: Router delgado -> Modelo/Repository (discussion [#58](https://github.com/mmasias/pyCelda/discussions/58)).
- **Autorización: `Depends(get_current_profesor_id)`** en ambos endpoints -- solo el propio `Profesor` ve/edita su perfil; no hay variante de `Admin` ni de `DirectorPrograma` revisor.

## Referencias

- [`editarPerfilPropio()` en Análisis](/RUP/02-analisis/casos-uso/editarPerfilPropio/README.md) -- diagrama de colaboración origen.
- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/README.md).
- [`editarUniversidad()` en Diseño](/RUP/03-diseño/casos-uso/editarUniversidad/README.md) -- plantilla de `GET` previo + `PUT` sin `alt` de negocio.
- [`abrirInicio()` en Diseño](/RUP/03-diseño/casos-uso/abrirInicio/README.md) -- consumidor del gate `validado`.
- [`activarCursoAcademico()` en Diseño](/RUP/03-diseño/casos-uso/activarCursoAcademico/README.md) -- origen de `CursoAcademicoRepository.activo()`.

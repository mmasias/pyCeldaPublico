<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > editarPerfilPropio()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/editarPerfilPropio/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`editarPerfilPropio()`](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/README.md) (issue [#423](https://github.com/mmasias/pyCelda/issues/423), reescrito en [#436](https://github.com/mmasias/pyCelda/issues/436)): el `Profesor` ve y edita **su propio** perfil académico (ORCID, doctorado, acreditación, sexenios/quinquenios, biografía...) sin pasar por `Admin`. Un solo caso de uso para ver+editar -- sin pantalla de listado previa, se llega directo desde `INICIO_ABIERTO` al propio y único perfil. No hay precedente 1:1 en el catálogo; la forma es la de [`editarUniversidad()`](../editarUniversidad/README.md) (carga previa + guardado sin `<<choice>>` de negocio que bloquee) con tres diferencias reales: (1) el perfil **no es una entidad con identificador en la ruta** -- siempre es el del `Profesor` de la sesión; (2) está **historizado por curso** (`PerfilProfesorCurso`, una fila por `Profesor` y `CursoAcademico`), así que la carga resuelve una bifurcación de tres ramas contra el curso **activo** y el guardado hace *upsert* sobre la fila del curso activo; (3) guardar es lo que **valida** el perfil (`validado = true`), dato que alimenta el gate de la pantalla de inicio. Sin `<<choice>>` bloqueante: ninguna precondición rechaza editar; las validaciones son de forma (formato de ORCID y enlaces, rangos, `organismoAcreditadorOtro` obligatorio si el organismo es "Otro").

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/editarPerfilPropio/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `EditarPerfilPropioView`

**Responsabilidades:**
- presenta el formulario con los datos del perfil resueltos para el curso activo, junto con el aviso que corresponda a la rama de carga: "datos del curso anterior, revísalos y confirma" (sugerencia) o "primer curso: completa tu perfil" (fila sin validar).
- permite solicitar guardar; tras guardar, se queda en la misma pantalla con el perfil ya validado y el aviso "Perfil actualizado".

**Colaboraciones:**
- **Entrada:** `:INICIO_ABIERTO` -- el `Profesor` solicita editar su perfil (`[Mi perfil]` de [`abrirInicio()`](../abrirInicio/README.md)); también `:PERFIL_ABIERTO` (self-loop al guardar).
- **Control:** `ProfesorController`.
- **Salida:** `:PERFIL_ABIERTO`.

## Clases de controlador

### `ProfesorController`

**Responsabilidades:**
- carga el perfil del `Profesor` de la sesión (`cargarMiPerfil(profesorId)`) resolviendo tres ramas contra el `CursoAcademico` activo de su `Universidad`: (1) existe fila del curso activo -- se sirve tal cual, con su `validado` real; (2) no existe, pero sí de un curso anterior -- se sirve la más reciente como sugerencia, con `validado` forzado a falso; (3) nunca tuvo ninguna -- formulario en blanco, sin validar.
- valida la forma de los datos (`validarDatosPerfil(datos) : boolean`): ORCID `0000-0000-0000-0000`, CVN restringido a `*.fecyt.es`, Google Scholar a `scholar.google.<dominio>/citations?...user=...`, foto por `https://`, `nivelAcreditacionSiiu` en `{0..5}`, `organismoAcreditadorOtro` obligatorio si el organismo es "Otro"; limpia los campos condicionales que no aplican (sin doctorado, sin acreditación, sin sexenios/quinquenios).
- guarda el perfil (`guardarPerfil(profesorId, datos)`): actualiza el `nombre` del `Profesor` y hace *upsert* de la fila del curso activo, que queda `validado`.

**Colaboraciones:**
- **Entrada:** `EditarPerfilPropioView`.
- **Salida:** `Profesor`, `ProfesorRepository`, `CursoAcademicoRepository`, `PerfilProfesorCursoRepository`, `PerfilProfesorCurso`.

## Clases de modelo

### `Profesor`

**Responsabilidades:**
- porta `nombre` y `email`; solo `nombre` es editable desde aquí -- el `email` nunca forma parte del formulario.
- se actualiza a sí mismo (`actualizarNombre(nombre)`).

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** persistido por `ProfesorRepository`.

### `ProfesorRepository`

**Responsabilidades:**
- recupera el `Profesor` de la sesión (`obtener(profesorId)`).

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `Profesor`.

### `CursoAcademicoRepository`

**Responsabilidades:**
- responde cuál es el `CursoAcademico` activo de la `Universidad` del `Profesor` (`activo(universidadId)`) -- referencia contra la que se resuelve la carga y sobre la que se escribe. Que exista siempre uno es una invariante, no un estado de negocio que el usuario provoque o resuelva.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `CursoAcademico`.

### `PerfilProfesorCurso`

**Responsabilidades:**
- porta el perfil académico de un `Profesor` **en un curso concreto**: `orcid`, enlaces (CVN, foto, Scholar), doctorado (`esDoctor`, universidad, año, programa, mención internacional), acreditación (`nivelAcreditacionSiiu`, `organismoAcreditador`, `organismoAcreditadorOtro`), sexenios y quinquenios (recuento, año del último, `tramitandoSexenio`), `biografia`, años de experiencia y `validado`. Una fila por `(Profesor, CursoAcademico)`.
- se actualiza a sí misma (`actualizar(...)`) y queda siempre `validado = true` -- el acto de confirmar/editar es el que valida, no la mera existencia de la fila.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** persistida por `PerfilProfesorCursoRepository`.

### `PerfilProfesorCursoRepository`

**Responsabilidades:**
- recupera la fila del curso activo (`obtener(profesorId, cursoAcademicoId)`) y la más reciente de cualquier curso (`obtenerMasReciente(profesorId)`).
- crea la fila si no existe o actualiza la existente (`upsert(profesorId, cursoAcademicoId, datos)`) -- la unicidad `(Profesor, CursoAcademico)` impide duplicados.

**Colaboraciones:**
- **Entrada:** `ProfesorController`.
- **Salida:** gestiona `PerfilProfesorCurso`.

## Fuera de alcance de esta rebanada

Visibilidad **pública** del perfil (sección "Profesorado" de la `Guia`, listados de `Admin`/`DirectorPrograma`) y separar `nombre` en `nombre`/`apellidos`: ver [Pendiente en Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/README.md#pendiente). La lectura del perfil validado de un `Profesor` por parte de `Admin` pertenece a [`abrirProfesor()`](../abrirProfesor/README.md), no a este caso de uso.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/editarPerfilPropio/wireframes.puml) -- fuente de verdad del formulario.
- [Diagrama de contexto de Profesor](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoProfesor.puml) -- `INICIO_ABIERTO --> PERFIL_ABIERTO : editarPerfilPropio()`, `PERFIL_ABIERTO --> PERFIL_ABIERTO : editarPerfilPropio()`; heredado sin cambios por `DirectorPrograma` ([diagrama de contexto de DirectorPrograma](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoDirectorPrograma.puml)).
- [`editarUniversidad()`](../editarUniversidad/README.md) -- plantilla de carga previa + guardado sin `<<choice>>` de negocio.
- [`abrirInicio()`](../abrirInicio/README.md) -- origen de la navegación y consumidor del gate `validado`.

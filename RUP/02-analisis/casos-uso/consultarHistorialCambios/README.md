<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# pyCelda > consultarHistorialCambios()

> |[🏠️](/README.md)|[DdC](/images/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.svg)|[Detalle](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/README.md)|**Análisis**|[Diseño](/RUP/03-diseño/casos-uso/consultarHistorialCambios/README.md)|Desarrollo|Pruebas|
> |-|-|-|-|-|-|-|

## Propósito

Traducción a clases de análisis del caso de uso [`consultarHistorialCambios()`](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/README.md) (issue [#392](https://github.com/mmasias/pyCelda/issues/392)): auditoría de solo lectura, sin `<<choice>>` de bloqueo. Presenta dos cosas en una sola pantalla -- el feed de las últimas 50 acciones registradas en `HistorialCambio` y un índice de autores distintos -- y permite navegar al historial completo de un autor concreto, **dentro del mismo caso de uso** (no es un estado propio: el detalle por autor es otra lectura del mismo CU). Mismo molde que [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) (verbo `consultar`, lectura/monitoreo con selector de curso opcional), con tres diferencias reales: (1) el **default del filtro es el opuesto** -- sin `?curso=`, histórico completo de todos los cursos, mientras `consultarEstadoGuias()` preselecciona el vigente (issue [#442](https://github.com/mmasias/pyCelda/issues/442)); (2) el **autor no es un único espacio de identificadores**: se resuelve según el campo que cambió (`estado` con el centinela de `Admin` es `Admin`; `estado` con identificador real es `DirectorPrograma`; `contenido`/`planificacion_docente`... es `Profesor`); (3) el **índice de autores se fusiona por email normalizado** -- un `Profesor` y un `DirectorPrograma` con el mismo email son una sola entrada (issue [#401](https://github.com/mmasias/pyCelda/issues/401)). `HistorialCambio` (`Guia *-- HistorialCambio`) solo se **lee** aquí; lo escriben otros casos de uso.

<div align=center>

|![](/images/RUP/02-analisis/casos-uso/consultarHistorialCambios/colaboracion.svg)|
|-|
|<div align=right><sup>Código fuente: [colaboracion.puml](colaboracion.puml)</sup></div>|

</div>

## Clases de vista

### `ConsultarHistorialCambiosView`

**Responsabilidades:**
- presenta el feed de las últimas 50 acciones: fecha, `Asignatura@SiglaPrograma` de la `Guia` (texto plano, sin enlace -- issues [#398](https://github.com/mmasias/pyCelda/issues/398)/[#403](https://github.com/mmasias/pyCelda/issues/403)), campo con etiqueta legible, cambio `valorAnterior -> valorNuevo`, autor y comentario.
- presenta el índice de autores (uno por persona) y, al seleccionar uno, su historial completo con una columna de rol (`Profesor`/`Director`/`Admin`) que distingue bajo qué identidad actuó en cada fila.
- ofrece un selector de curso académico ("Todos los cursos" por defecto, o un curso concreto) que refiltra el feed y el índice.
- presenta los estados vacíos ("sin acciones registradas", "sin autores") -- un historial vacío es un estado válido, no un error.

**Colaboraciones:**
- **Entrada:** `:SISTEMA_DISPONIBLE` -- el `Admin` solicita consultar el historial de cambios (desde [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md)).
- **Control:** `HistorialCambioController`.
- **Salida:** `:HISTORIAL_CAMBIOS_ABIERTO`.

## Clases de controlador

### `HistorialCambioController`

**Responsabilidades:**
- consulta el feed y el índice de autores (`consultarHistorial(cursoAcademicoId)`): sin curso, todo el histórico; con curso, solo las filas de las `Guia` de ese curso. Si el curso indicado no existe, lo rechaza (la comprobación previa se delega en `CursoAcademicoRepository.obtener()`).
- consulta el historial completo de un autor (`consultarHistorialDeAutor(clave)`): sin límite de 50 ni filtro de curso. Una clave desconocida no es un error, es una búsqueda con cero resultados.
- resuelve el autor de cada fila según el campo que cambió (`resolverAutor(campo, autorId)`) y agrupa por email normalizado (`claveAgrupacion(...)`), con `Admin` aislado bajo la clave literal `"admin"`.
- no valida ni muta nada más -- caso de uso de solo lectura.

**Colaboraciones:**
- **Entrada:** `ConsultarHistorialCambiosView`.
- **Salida:** `HistorialCambio`, `CursoAcademicoRepository`, `ProgramaRepository`, `ProfesorRepository`, `DirectorPrograma`, `Profesor`.

## Clases de modelo

### `HistorialCambio`

**Responsabilidades:**
- porta `fecha`, `campo`, `valorAnterior`, `valorNuevo`, `comentario`, `autorId` y la `Guia` a la que pertenece (`Guia *-- HistorialCambio`); de la `Guia` salen la `AsignaturaPrograma` y el `Programa` que se muestran.
- se **lee** aquí, nunca se escribe: lo registran otros puntos del código (aprobar/rechazar/escalar/revocar guía, edición de contenido, planificación docente, importaciones...).
- la consulta se hace directamente sobre `HistorialCambio`, sin repositorio propio: ordena por `fecha` descendente, desempatando por `id` descendente (varias filas pueden compartir el mismo instante).

**Colaboraciones:**
- **Entrada:** consultada por `HistorialCambioController`.

### `Profesor` / `DirectorPrograma`

**Responsabilidades:**
- `Profesor` porta `nombre` y `email`; `DirectorPrograma` solo `email` (tabla mínima, sin `nombre` propio) -- su nombre se obtiene cruzando por email contra `Profesor` cuando existe (issue [#396](https://github.com/mmasias/pyCelda/issues/396)).
- ambos `email` son únicos: base de la fusión del índice de autores.

**Colaboraciones:**
- **Entrada:** consultados por `HistorialCambioController` (y `ProfesorRepository` para el cruce por email).

### `CursoAcademicoRepository` / `ProgramaRepository` / `ProfesorRepository`

**Responsabilidades:**
- `CursoAcademicoRepository.obtener(cursoAcademicoId)`: comprueba que el curso del filtro existe.
- `ProgramaRepository.obtener(programaId)`: aporta el código del `Programa` (`IOI`, `GII`...) para la columna Guía.
- `ProfesorRepository.obtenerPorEmail(email)`: cruce de un `DirectorPrograma` con su `Profesor` para mostrar un nombre real.

**Colaboraciones:**
- **Entrada:** `HistorialCambioController`.
- **Salida:** gestionan `CursoAcademico`, `Programa`, `Profesor`.

## Referencias

- [Especificación de Requisitos](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/especificacion.puml) y [wireframes](/RUP/01-requisitos/03-detalle-casos-uso/consultarHistorialCambios/wireframes.puml) -- fuente de verdad de las dos columnas (feed + autores) y del detalle por autor.
- [Diagrama de contexto de Admin](/RUP/01-requisitos/01-actores-casos-uso/diagramaContextoAdmin.puml) -- `SISTEMA_DISPONIBLE --> HISTORIAL_CAMBIOS_ABIERTO : consultarHistorialCambios()`, `HISTORIAL_CAMBIOS_ABIERTO --> SISTEMA_DISPONIBLE : abrirPanelAdministracion()`.
- [Modelo del dominio](/RUP/00-modelo-del-dominio/modeloDominio.puml) -- `Guia *-- HistorialCambio`.
- [`consultarEstadoGuias()`](../consultarEstadoGuias/README.md) -- plantilla de consulta de solo lectura con selector de curso (default opuesto).
- [`consultarCopiasSeguridad()`](../consultarCopiasSeguridad/README.md) -- caso de uso hermano de auditoría de `Admin`.
- [`abrirPanelAdministracion()`](../abrirPanelAdministracion/README.md) -- origen y destino de la navegación.

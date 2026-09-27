<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [**Análisis**](/RUP/02-analisis/README.md) / [Diseño](/RUP/03-diseño/README.md)</sub>

</div>

# Casos de uso en análisis

96 fichas: 93 de los 102 casos del catálogo más las tres primitivas de navegación (`iniciarSesion()`, `abrirPanelAdministracion()`, `abrirInicio()`, fuera del catálogo). Construidas en cinco grupos, los dos primeros por olas de fase y el resto por pipeline vertical por CU -- mismo artefacto, mismo formato. Los 3 del clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) y los 3 de importación/arranque entre hermanas (familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184): `importarBibliografiaDeGuiaHermana()`, `importarPlanificacionDocenteDeGuiaHermana()`, `generarPlanificacionDocenteGenerica()`) se especifican de Requisitos a Diseño en un mismo checkpoint.

Ciclo de vida completo de `Guia` (L7-L9): los 9 primeros cubren de principio a fin el ciclo de edición desde el punto de vista del `Profesor` -- abrir, crear/editar/eliminar hijos con CRUD real e inmediato, sincronizar su vinculación (como borrador o a revisión), y la aprobación del `DirectorGrado`; ya pasaron por Diseño y Desarrollo real. Los 12 siguientes completan la entidad: el CRUD completo (listado, detalle, edición) de `PonderacionEvaluacion`/`ReferenciaBibliografica`, y el resto del ciclo de revisión del `DirectorGrado` -- rechazar, escalar, revocar, editar semestre, notificar y descargar PDF; también cerrados hasta Desarrollo (PR [#68](https://github.com/mmasias/pyCelda/pull/68)). `previsualizarGuia()` (discussion [#218](https://github.com/mmasias/pyCelda/discussions/218)) se añade después, en la misma rebanada que el v1 del render real de `descargarGuiaPDF()`: vista HTML de la guía renderizada, comparte `RenderizadorGuiaDocente` con la salida PDF.

Importación entre `AsignaturaGrado` hermanas (L8/L10, issue [#184](https://github.com/mmasias/pyCelda/issues/184), 2 CU): [`importarBibliografiaDeGuiaHermana()`](importarBibliografiaDeGuiaHermana/README.md) / [`importarPlanificacionDocenteDeGuiaHermana()`](importarPlanificacionDocenteDeGuiaHermana/README.md) -- actor `Profesor` de la `AsignaturaGrado` destino, heredado por `DirectorGrado`. Copia con reemplazo total de la colección (`ReferenciaBibliografica` / `Sesion`) de una `Guia` `Aprobada` de una hermana, real e inmediata contra el repositorio (`reemplazarDesde`), degradando la guía destino si estaba `Aprobada` (`Guia.confirmar_guardado()` reutilizado) y registrando una fila de `HistorialCambio`. `Profesor` deja de estar en 0 CU restantes -- estos dos son los primeros CU de `Profesor` fuera del hilo `Guia` original.

A partir de aquí, resto del catálogo real de `DirectorGrado` (L2-L6): 21 casos que completan su catálogo propio -- CRUD de `ResultadoAprendizaje`, las cuatro asociaciones `MetodologiaDocente`/`ResultadoAprendizaje` con `Materia` y `AsignaturaGrado`, `editarAsignaturaGrado()`, y la navegación de lectura (`abrirGrados()`, `abrirGrado()`, `abrirMaterias()`, `abrirMateria()`, `abrirAsignaturaGrado()`, `abrirAsignaturasGrado()`) que reutiliza CU compartidos con `Admin` o que es exclusiva de `DirectorGrado`. `Profesor` estuvo en 0 CU restantes hasta el issue #184 (arriba). Más el clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227), 3 CU): `editarActividadesFormativasMateria()` / `editarActividadesFormativasAsignaturaGrado()` (rejilla de un submit sobre las 10 filas de asociación, siempre presentes) y `consultarEstadoActividadesFormativasMateria()` (medidor blando de `AfM = Σ AfAdM`, `Materia.discrepanciasActividadesFormativas()` en el modelo).

|Caso|Patrón que representa|
|-|-|
|[`abrirGuia()`](abrirGuia/README.md)|Entrada de la sesión de edición, solo lectura: fusiona lo ya vinculado a la `Guia` con lo pendiente-sin-vincular de sus hijos. Sin `<<choice>>`|
|[`crearReferenciaBibliografica()`](crearReferenciaBibliografica/README.md)|CRUD simple sin `<<choice>>` ("el delgado"): formulario mínimo, crea real e inmediato contra `ReferenciaBibliograficaRepository`, sin tocar `Guia`, salida a `<<include>>` de edición|
|[`crearPonderacionEvaluacion()`](crearPonderacionEvaluacion/README.md)|CRUD con validación puntual: `<<choice>>` de máximo individual por `SistemaEvaluacion` (sin suma de hermanas), crea real e inmediato sin tocar `Guia`, dos salidas (éxito a `<<include>>`, fallo al listado)|
|[`editarPonderacionEvaluacion()`](editarPonderacionEvaluacion/README.md)|Misma validación de máximo puntual, sin exclusión del valor anterior (ya no hace falta, no hay suma de la que excluir): self-loop de salida en éxito y en fallo, sin `<<include>>`|
|[`eliminarPonderacionEvaluacion()`](eliminarPonderacionEvaluacion/README.md)|Confirmación sin `<<choice>>`, sin ninguna clase de Modelo: solo quita el ítem de la lista de trabajo de la sesión, sin tocar la fila ni `Guia`. Flujo numerado por tener dos caminos (confirmar/cancelar) al mismo estado de salida|
|[`eliminarReferenciaBibliografica()`](eliminarReferenciaBibliografica/README.md)|Mismo patrón que `eliminarPonderacionEvaluacion()`, sobre `ReferenciaBibliografica`|
|[`guardarBorradorGuia()`](guardarBorradorGuia/README.md)|Sincronización por diff de `PonderacionEvaluacion`/`ReferenciaBibliografica`/`Sesion`: recibe la lista completa deseada de cada colección y vincula/desvincula contra lo ya vinculado -- desvincular borra la fila (issue #93). Sin `<<choice>>` (siempre éxito), dispara `Aprobada -> Borrador` si aplica|
|[`enviarGuiaARevision()`](enviarGuiaARevision/README.md)|Precondición de "sin pendientes" + `<<choice>>` de rango por `SistemaEvaluacion` y suma total = 100%, contra lo ya vinculado -- sin vincular ni crear nada él mismo|
|[`aprobarGuia()`](aprobarGuia/README.md)|Ciclo de vida: transición de estado `EnRevision -> Aprobada` que la `Guia` aplica sobre su propia máquina de estados, con `HistorialCambio` y persistencia real|
|[`abrirPonderacionesEvaluacion()`](abrirPonderacionesEvaluacion/README.md)|Listado de solo lectura, misma fusión vinculado+pendiente que `abrirGuia()`, aplicada a una única colección|
|[`abrirPonderacionEvaluacion()`](abrirPonderacionEvaluacion/README.md)|Detalle de solo lectura, reutiliza `cargarPonderacionEvaluacion()` ya introducido por `editarPonderacionEvaluacion()`|
|[`abrirReferenciasBibliograficas()`](abrirReferenciasBibliograficas/README.md)|Simétrico a `abrirPonderacionesEvaluacion()`, sobre `ReferenciaBibliografica`|
|[`abrirReferenciaBibliografica()`](abrirReferenciaBibliografica/README.md)|Detalle de solo lectura, introduce `ReferenciaBibliograficaRepository.obtener()`, reutilizado después por `editarReferenciaBibliografica()`|
|[`editarReferenciaBibliografica()`](editarReferenciaBibliografica/README.md)|CRUD sin `<<choice>>` de negocio (a diferencia de `editarPonderacionEvaluacion()`): cierra la asimetría del diagrama consolidado con `ReferenciaBibliografica.actualizar()`|
|[`consultarEstadoGuias()`](consultarEstadoGuias/README.md)|Listado agregado de `Guia` por `Grado`, primer método de listado de `GuiaController`; entrada al ciclo de revisión del `DirectorGrado`|
|[`rechazarGuia()`](rechazarGuia/README.md)|Ciclo de vida: `EnRevision -> Rechazada`, comentario opcional del actor registrado en `HistorialCambio` -- misma familia que `aprobarGuia()`|
|[`escalarGuiaAAprobada()`](escalarGuiaAAprobada/README.md)|Ciclo de vida: `{Borrador,Rechazada} -> Aprobada`, comentario fijo sin pedir nada al actor -- misma familia que `aprobarGuia()`|
|[`revocarAprobacionGuia()`](revocarAprobacionGuia/README.md)|Ciclo de vida: `Aprobada -> Borrador`, comentario opcional -- misma forma que `rechazarGuia()`|
|[`editarSemestreGuia()`](editarSemestreGuia/README.md)|Edición sin `<<choice>>` ni `HistorialCambio`, con efecto colateral condicional: regenera el PDF si la `Guia` estaba `Aprobada`, sin transición de estado|
|[`notificarGuiasActualizadas()`](notificarGuiasActualizadas/README.md)|Self-loop sin ninguna clase de Modelo: notificación al `Admin`, mecanismo de infraestructura fuera del dominio|
|[`descargarGuiaPDF()`](descargarGuiaPDF/README.md)|Único `<<choice>>` real del lote: bloquea si no hay PDF generado, salvaguarda estructural nunca disparada desde la interfaz. En la rama verde, `RenderizadorGuiaDocente` produce el PDF real (v1, [#218](https://github.com/mmasias/pyCelda/discussions/218))|
|[`previsualizarGuia()`](previsualizarGuia/README.md)|Vista de solo lectura que renderiza la `Guia` con el formato de la guía docente oficial (mismo `RenderizadorGuiaDocente` que `descargarGuiaPDF()`, salida HTML); sin `<<choice>>`, aviso de borrador no oficial si no `Aprobada`|
|[`abrirGrados()`](abrirGrados/README.md)|Listado de solo lectura, variante `DirectorGrado` (filtrada a sus propios Grados) de un CU compartido con `Admin`|
|[`abrirGrado()`](abrirGrado/README.md)|Detalle de solo lectura, agrega la tabla de `AsignaturaGrado` del `Grado` agrupada por `Materia`|
|[`abrirMaterias()`](abrirMaterias/README.md)|Listado de solo lectura, `DirectorGrado` navega el CRUD de `Admin` para llegar a sus propios casos de asociación|
|[`abrirMateria()`](abrirMateria/README.md)|Detalle de solo lectura, fusiona tres colecciones asociadas: `MetodologiaDocente`, `ResultadoAprendizaje`, `AsignaturaGrado`|
|[`asociarMetodologiaDocenteAMateria()`](asociarMetodologiaDocenteAMateria/README.md)|CRUD sin `<<choice>>`, crea la clase de asociación `MetodologiaMateria` con `descripcionPropia` vacía|
|[`desasociarMetodologiaDocenteMateria()`](desasociarMetodologiaDocenteMateria/README.md)|`<<choice>>` bloqueante por uso en `AsignaturaGrado` de la `Materia` (primer escalón de cascada)|
|[`editarAsociacionMetodologiaDocenteMateria()`](editarAsociacionMetodologiaDocenteMateria/README.md)|CRUD sin `<<choice>>`, único campo editable: `descripcionPropia`, patrón catálogo+override|
|[`editarActividadesFormativasMateria()`](editarActividadesFormativasMateria/README.md)|Rejilla de un submit sobre las 10 filas `ActividadFormativaMateria` (siempre presentes); `<<choice>>` de validación de entrada (`horas` negativas); regla `AfM = Σ` fuera del choice|
|[`consultarEstadoActividadesFormativasMateria()`](consultarEstadoActividadesFormativasMateria/README.md)|Solo lectura, sin `<<choice>>`; medidor blando de `AfM = Σ AfAdM`, cálculo en `Materia.discrepanciasActividadesFormativas()` (Fat Model), compuesto desde `abrirMateria()`|
|[`asociarResultadoAprendizajeAMateria()`](asociarResultadoAprendizajeAMateria/README.md)|CRUD sin `<<choice>>`, agregación simple sin clase de asociación (a diferencia de `MetodologiaDocente`)|
|[`desasociarResultadoAprendizajeAMateria()`](desasociarResultadoAprendizajeAMateria/README.md)|`<<choice>>` bloqueante por uso en `AsignaturaGrado` de la `Materia`|
|[`abrirAsignaturaGrado()`](abrirAsignaturaGrado/README.md)|Detalle de solo lectura, dos entradas y un único retorno, fusiona profesorado + `MetodologiaDocente` + `ResultadoAprendizaje` asociados|
|[`abrirAsignaturasGrado()`](abrirAsignaturasGrado/README.md)|Listado agregado exclusivo de `DirectorGrado`, reutiliza `GuiaRepository.listarDelGrado()` ya existente para el estado de cada fila|
|[`editarAsignaturaGrado()`](editarAsignaturaGrado/README.md)|CRUD sin `<<choice>>`, único caso de edición del catálogo que no es de `Admin`; hallazgo de bloqueo pendiente sobre `semestreDefault`, no resuelto|
|[`asociarMetodologiaDocenteAAsignaturaGrado()`](asociarMetodologiaDocenteAAsignaturaGrado/README.md)|CRUD sin `<<choice>>`, segundo escalón de la cascada `MetodologiaDocente`|
|[`desasociarMetodologiaDocenteAsignaturaGrado()`](desasociarMetodologiaDocenteAsignaturaGrado/README.md)|Sin `<<choice>>` bloqueante (último escalón), advertencia condicional no bloqueante|
|[`asociarResultadoAprendizajeAAsignaturaGrado()`](asociarResultadoAprendizajeAAsignaturaGrado/README.md)|CRUD sin `<<choice>>`, segundo escalón de la cascada `ResultadoAprendizaje`|
|[`desasociarResultadoAprendizajeAsignaturaGrado()`](desasociarResultadoAprendizajeAsignaturaGrado/README.md)|Sin `<<choice>>` bloqueante (último escalón), advertencia condicional no bloqueante|
|[`editarActividadesFormativasAsignaturaGrado()`](editarActividadesFormativasAsignaturaGrado/README.md)|Rejilla de un submit sobre las 10 filas `ActividadFormativaAsignaturaGrado`; `<<choice>>` de validación (`horas` negativas / `porcentajePresencialidad` fuera de 0-100); nivel que consume el render de la `Guia`|
|[`abrirResultadosAprendizaje()`](abrirResultadosAprendizaje/README.md)|Listado de solo lectura, catálogo propio del `Grado`, no institucional|
|[`abrirResultadoAprendizaje()`](abrirResultadoAprendizaje/README.md)|Detalle de solo lectura|
|[`crearResultadoAprendizaje()`](crearResultadoAprendizaje/README.md)|Sin patrón C→U, entidad demasiado minimalista para deferir campos -- pide `codigo`+`tipo`+`descripcion` de una vez|
|[`editarResultadoAprendizaje()`](editarResultadoAprendizaje/README.md)|CRUD sin `<<choice>>`, `codigo` editable (a diferencia de `MetodologiaDocente`)|
|[`eliminarResultadoAprendizaje()`](eliminarResultadoAprendizaje/README.md)|`<<choice>>` bloqueante por uso en `Materia` o `AsignaturaGrado`, borrado físico, dos niveles de cascada en una consulta|

## Catálogo de `Admin`, autenticación y `PlanificacionDocente` (L0-L1, L10)

Los grupos tercero y cuarto: el CRUD del catálogo estructural que `Admin` gestiona (universidad/facultad/grado/materia/asignatura/metodologías/sistemas de evaluación/profesorado, dirección de grado, profesorado de `AsignaturaGrado`), el login real (`iniciarSesion()`, Google OAuth2/OIDC sin auto-registro) y la planificación docente del `Profesor` (L10).

|Caso|Patrón que representa|
|-|-|
|[`abrirAsignatura()`](abrirAsignatura/README.md)|Detalle de solo lectura de `Asignatura` (`nombre`, `ects`, `estado`, `contenido`), sin catálogo hijo|
|[`abrirAsignaturas()`](abrirAsignaturas/README.md)|Listado plano del catálogo `Asignatura` bajo `SISTEMA_DISPONIBLE`, sin composición padre|
|[`abrirFacultad()`](abrirFacultad/README.md)|Detalle de solo lectura de `Facultad`; puerta a `abrirGrados()` (hueco de wireframe corregido)|
|[`abrirFacultades()`](abrirFacultades/README.md)|Listado de `Facultad` de una `Universidad`; composición real, no catálogo plano|
|[`abrirMetodologiaDocente()`](abrirMetodologiaDocente/README.md)|Detalle de solo lectura de `MetodologiaDocente` (`codigo`, `descripcion`), sin catálogo hijo|
|[`abrirMetodologiasDocentes()`](abrirMetodologiasDocentes/README.md)|Listado plano del catálogo `MetodologiaDocente`, reutilizado por `Materia` y `AsignaturaGrado`|
|[`abrirInicio()`](abrirInicio/README.md)|Primitiva de navegación: compone "Mis guías" (`<<include>>` de `abrirAsignaturasGrado()`) y "Mis grados" (`<<include>>` de `abrirGrados()`), sin Controlador ni Modelo propios; discussion #274|
|[`abrirPanelAdministracion()`](abrirPanelAdministracion/README.md)|Primitiva de navegación pura: menú fijo de seis enlaces, sin Controlador ni Modelo|
|[`abrirPlanificacionDocente()`](abrirPlanificacionDocente/README.md)|Listado de solo lectura de `Sesion` de la `Guia`, fusionando vinculado+pendiente, ordenado por `numero`|
|[`abrirProfesor()`](abrirProfesor/README.md)|Detalle de `Profesor` más sección "Grados que dirige" (rol resuelto por email)|
|[`abrirProfesores()`](abrirProfesores/README.md)|Listado plano del catálogo `Profesor` (top-level), reutilizado por `AsignaturaGrado.profesorado`|
|[`abrirSistemaEvaluacion()`](abrirSistemaEvaluacion/README.md)|Detalle de solo lectura de `SistemaEvaluacion`; destino del alta de `crearSistemaEvaluacion()`|
|[`abrirSistemasEvaluacion()`](abrirSistemasEvaluacion/README.md)|Listado de `SistemaEvaluacion` de una `Materia`; composición real bajo padre|
|[`abrirUniversidad()`](abrirUniversidad/README.md)|Detalle de solo lectura de `Universidad`; puerta a `abrirFacultades()` (wireframe corregido)|
|[`abrirUniversidades()`](abrirUniversidades/README.md)|Listado completo de `Universidad`; primer nivel de la estructura curricular|
|[`asignarProfesorAAsignaturaGrado()`](asignarProfesorAAsignaturaGrado/README.md)|Asignación libre `AsignaturaGrado -- Profesor`; completa `Guia.profesorado` si nació vacía|
|[`crearAsignatura()`](crearAsignatura/README.md)|CRUD nombre-only con patrón C->U; `estado` nace `Vigente`, salida vía `<<include>> editarAsignatura()`|
|[`crearAsignaturaGrado()`](crearAsignaturaGrado/README.md)|Creación desde selectores `Materia`+`Asignatura` con herencia overrideable; nace `Guia` vacía|
|[`crearFacultad()`](crearFacultad/README.md)|CRUD nombre-only bajo composición `Universidad`; salida vía `<<include>> editarFacultad()`|
|[`crearGrado()`](crearGrado/README.md)|CRUD `codigo`+`nombre` obligatorios; primera escritura de `Admin` sobre `Grado`|
|[`crearMateria()`](crearMateria/README.md)|CRUD nombre-only anidado bajo `Grado`; salida vía `<<include>> editarMateria()`|
|[`crearMetodologiaDocente()`](crearMetodologiaDocente/README.md)|CRUD `codigo`+`descripcion`, sin patrón C->U; salida al detalle, no `<<include>>`|
|[`crearProfesor()`](crearProfesor/README.md)|CRUD `nombre`+`email`, único del lote sin C->U; salida al detalle|
|[`crearSesion()`](crearSesion/README.md)|CRUD `Sesion` con `numero` correlativo automático; nace pendiente-sin-vincular hasta guardar la `Guia`|
|[`crearSistemaEvaluacion()`](crearSistemaEvaluacion/README.md)|CRUD de cuatro campos bajo `Materia`, sin C->U; rango validado en Vista|
|[`crearUniversidad()`](crearUniversidad/README.md)|CRUD nombre-only, el patrón original; salida vía `<<include>> editarUniversidad()`|
|[`definirDirectorGrado()`](definirDirectorGrado/README.md)|Alta del rol `DirectorGrado` sobre `Profesor`; resuelto por email, idempotente, sin `<<choice>>`|
|[`desasignarProfesorAsignaturaGrado()`](desasignarProfesorAsignaturaGrado/README.md)|Retira `Profesor` de `AsignaturaGrado` sin bloqueo; nunca toca `Guia -- Profesor`|
|[`editarAsignatura()`](editarAsignatura/README.md)|CRUD sin `<<choice>>`; `estado` fuera del formulario; destino del `<<include>>` de crear|
|[`editarFacultad()`](editarFacultad/README.md)|CRUD nombre-only, mismo patrón que `editarUniversidad()`; destino del `<<include>>` de crear|
|[`editarGrado()`](editarGrado/README.md)|Solo `nombre` editable; `codigo` congelado (identificador real), `estado` fuera|
|[`editarMateria()`](editarMateria/README.md)|CRUD nombre-only; la composición con `Grado` no se muta aquí|
|[`editarMetodologiaDocente()`](editarMetodologiaDocente/README.md)|`codigo` de solo lectura tras crear; efectivamente solo `descripcion` cambia|
|[`editarProfesor()`](editarProfesor/README.md)|`nombre` y `email` siempre editables; guardián de unicidad de email (excluye propio)|
|[`editarSesion()`](editarSesion/README.md)|Solo `tipo` y `descripcion` editables; `numero` correlativo permanece sin cambios|
|[`editarSistemaEvaluacion()`](editarSistemaEvaluacion/README.md)|Cuatro campos editables, sin campo fijo; rango es validación de forma|
|[`editarUniversidad()`](editarUniversidad/README.md)|CRUD nombre-only; `Universidad.actualizar(nombre)`, destino del `<<include>>` de crear|
|[`eliminarAsignatura()`](eliminarAsignatura/README.md)|Borrado lógico sin `<<choice>>`: `extinguir()` pasa `estado` a `Extinguido`|
|[`eliminarAsignaturaGrado()`](eliminarAsignaturaGrado/README.md)|Borrado lógico sin `<<choice>>`, mismo patrón que `eliminarGrado()`; desde tabla embebida del `Grado`|
|[`eliminarFacultad()`](eliminarFacultad/README.md)|`<<choice>>` bloqueante: borrado físico si tiene `Grado`s asociados|
|[`eliminarGrado()`](eliminarGrado/README.md)|Borrado lógico sin `<<choice>>`; preserva `Guia` históricas vía `estado`|
|[`eliminarMetodologiaDocente()`](eliminarMetodologiaDocente/README.md)|`<<choice>>` bloqueante: borrado físico si asociada a `Materia` (una sola tabla basta)|
|[`eliminarProfesor()`](eliminarProfesor/README.md)|`<<choice>>` bloqueante con tres motivos: `AsignaturaGrado` asignadas, `Guia` históricas, rol `DirectorGrado`|
|[`eliminarSesion()`](eliminarSesion/README.md)|Confirmación simple sin Modelo: quita de lista de trabajo, sin tocar fila ni `Guia`|
|[`eliminarSistemaEvaluacion()`](eliminarSistemaEvaluacion/README.md)|`<<choice>>` bloqueante por conteo de `PonderacionEvaluacion`; borrado físico bajo `Materia`|
|[`importarBibliografiaDeGuiaHermana()`](importarBibliografiaDeGuiaHermana/README.md)|Copia con reemplazo total contra `ReferenciaBibliograficaRepository.reemplazarDesde()`; hermandad por `AsignaturaGrado.asignatura_id`+`codigo`; degrada la guía destino y registra una fila de `HistorialCambio`; relajación acotada de la 404-uniforme|
|[`importarPlanificacionDocenteDeGuiaHermana()`](importarPlanificacionDocenteDeGuiaHermana/README.md)|Gemelo del anterior sobre `Sesion`; `SesionRepository.reemplazarDesde()` renumera `1..N` en persistencia sin tocar `Guia.sesiones_minimas`|
|[`iniciarSesion()`](iniciarSesion/README.md)|Dos ramas `<<extend>>` (`abrirInicio()` para Profesor/DirectorGrado, `abrirPanelAdministracion()` para Admin); OAuth Google contra catálogo, sin auto-registro; guard de rol `director_grado` = dirige `>= 1` Grado (discussion #274)|
|[`quitarDirectorGrado()`](quitarDirectorGrado/README.md)|`<<choice>>` bloqueante: un `Grado` no puede quedarse sin `DirectorGrado`|

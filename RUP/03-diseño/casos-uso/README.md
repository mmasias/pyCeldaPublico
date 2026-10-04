<div align=right>

<sub>[Modelo del dominio](/RUP/00-modelo-del-dominio/README.md) / [Actores y casos de uso](/RUP/01-requisitos/01-actores-casos-uso/README.md) / [Detalle](/RUP/01-requisitos/03-detalle-casos-uso/README.md) / [Análisis](/RUP/02-analisis/README.md) / **Diseño**</sub><br><sub>Subconjunto público de [pyCelda](https://github.com/mmasias/pyCelda) -- incluye modelo de dominio, requisitos, análisis y diseño completos; desarrollo solo para 5 casos de uso elegidos como ejemplo. Sin dashboard de seguimiento.</sub>

</div>

# Casos de uso en diseño

Recuento actual (verificado contra las carpetas, issue [#662](https://github.com/mmasias/pyCelda/issues/662); 105 en el [#660](https://github.com/mmasias/pyCelda/issues/660) más 13 de la deuda cerrada en el #662): 118 carpetas con ficha, incluidas las 5 del clúster `ActividadFormativa` (`abrirActividadesFormativas()`, `abrirActividadFormativa()`, `crearActividadFormativa()`, `editarActividadFormativa()`, `eliminarActividadFormativa()`). Recuento histórico: 96 fichas: 93 de los 102 casos del catálogo más las tres primitivas de navegación (`iniciarSesion()`, `abrirPanelAdministracion()`, `abrirInicio()`), mismas que [Análisis](/RUP/02-analisis/casos-uso/README.md). Cada caso baja su `colaboracion.puml` de Análisis a un `secuencia.puml` con orden temporal explícito, Vista -> API -> Modelo -> Repositorio -> BD, sin capa Service -- ver discussion [#58](https://github.com/mmasias/pyCelda/discussions/58). Los 3 del clúster de `ActividadFormativa` (discussion [#227](https://github.com/mmasias/pyCelda/discussions/227)) y los 3 de importación/arranque entre hermanas (familia del issue [#184](https://github.com/mmasias/pyCelda/issues/184)) llegan a Diseño en el checkpoint de prosa RUP correspondiente; `consultarEstadoActividadesFormativasMateria()` quedó en 🚧 (Diseño escrito, código en el PR posterior).

## Hilo `Guia` (L7-L9)

|Caso|Estado|
|-|-|
|[`abrirGuia()`](abrirGuia/README.md)|Hecho|
|[`crearReferenciaBibliografica()`](crearReferenciaBibliografica/README.md)|Hecho|
|[`crearPonderacionEvaluacion()`](crearPonderacionEvaluacion/README.md)|Hecho|
|[`editarPonderacionEvaluacion()`](editarPonderacionEvaluacion/README.md)|Hecho|
|[`eliminarPonderacionEvaluacion()`](eliminarPonderacionEvaluacion/README.md)|Hecho -- sin endpoint de backend|
|[`eliminarReferenciaBibliografica()`](eliminarReferenciaBibliografica/README.md)|Hecho -- sin endpoint de backend|
|[`guardarBorradorGuia()`](guardarBorradorGuia/README.md)|Hecho|
|[`enviarGuiaARevision()`](enviarGuiaARevision/README.md)|Hecho|
|[`aprobarGuia()`](aprobarGuia/README.md)|Hecho|
|[`abrirPonderacionesEvaluacion()`](abrirPonderacionesEvaluacion/README.md)|Hecho|
|[`abrirPonderacionEvaluacion()`](abrirPonderacionEvaluacion/README.md)|Hecho -- sin endpoint nuevo, reutiliza el de `editarPonderacionEvaluacion()`|
|[`abrirReferenciasBibliograficas()`](abrirReferenciasBibliograficas/README.md)|Hecho|
|[`abrirReferenciaBibliografica()`](abrirReferenciaBibliografica/README.md)|Hecho|
|[`editarReferenciaBibliografica()`](editarReferenciaBibliografica/README.md)|Hecho|
|[`consultarEstadoGuias()`](consultarEstadoGuias/README.md)|Hecho|
|[`rechazarGuia()`](rechazarGuia/README.md)|Hecho|
|[`escalarGuiaAAprobada()`](escalarGuiaAAprobada/README.md)|Hecho|
|[`revocarAprobacionGuia()`](revocarAprobacionGuia/README.md)|Hecho|
|[`editarSemestreGuia()`](editarSemestreGuia/README.md)|Hecho|
|[`notificarGuiasActualizadas()`](notificarGuiasActualizadas/README.md)|Hecho -- sin endpoint que toque base de datos|
|[`descargarGuiaPDF()`](descargarGuiaPDF/README.md)|Hecho -- render real WeasyPrint (v1, [#218](https://github.com/mmasias/pyCelda/discussions/218))|
|[`previsualizarGuia()`](previsualizarGuia/README.md)|Hecho -- vista HTML, misma plantilla que `descargarGuiaPDF()`|

## Resto del catálogo de `DirectorPrograma` (L2-L6)

|Caso|Estado|
|-|-|
|[`abrirProgramas()`](abrirProgramas/README.md)|Hecho|
|[`abrirPrograma()`](abrirPrograma/README.md)|Hecho|
|[`abrirMaterias()`](abrirMaterias/README.md)|Hecho|
|[`abrirMateria()`](abrirMateria/README.md)|Hecho|
|[`abrirAsignaturasPrograma()`](abrirAsignaturasPrograma/README.md)|Hecho -- reutiliza `GuiaRepository.listar_del_programa()`|
|[`abrirAsignaturaPrograma()`](abrirAsignaturaPrograma/README.md)|Hecho|
|[`abrirResultadosAprendizaje()`](abrirResultadosAprendizaje/README.md)|Hecho|
|[`abrirResultadoAprendizaje()`](abrirResultadoAprendizaje/README.md)|Hecho|
|[`crearResultadoAprendizaje()`](crearResultadoAprendizaje/README.md)|Hecho|
|[`editarResultadoAprendizaje()`](editarResultadoAprendizaje/README.md)|Hecho|
|[`eliminarResultadoAprendizaje()`](eliminarResultadoAprendizaje/README.md)|Hecho|
|[`asociarMetodologiaDocenteAMateria()`](asociarMetodologiaDocenteAMateria/README.md)|Hecho|
|[`desasociarMetodologiaDocenteMateria()`](desasociarMetodologiaDocenteMateria/README.md)|Hecho|
|[`editarAsociacionMetodologiaDocenteMateria()`](editarAsociacionMetodologiaDocenteMateria/README.md)|Hecho|
|[`asociarResultadoAprendizajeAMateria()`](asociarResultadoAprendizajeAMateria/README.md)|Hecho|
|[`desasociarResultadoAprendizajeAMateria()`](desasociarResultadoAprendizajeAMateria/README.md)|Hecho|
|[`asociarMetodologiaDocenteAAsignaturaPrograma()`](asociarMetodologiaDocenteAAsignaturaPrograma/README.md)|Hecho|
|[`desasociarMetodologiaDocenteAsignaturaPrograma()`](desasociarMetodologiaDocenteAsignaturaPrograma/README.md)|Hecho|
|[`asociarResultadoAprendizajeAAsignaturaPrograma()`](asociarResultadoAprendizajeAAsignaturaPrograma/README.md)|Hecho|
|[`desasociarResultadoAprendizajeAsignaturaPrograma()`](desasociarResultadoAprendizajeAsignaturaPrograma/README.md)|Hecho|
|[`editarAsignaturaPrograma()`](editarAsignaturaPrograma/README.md)|Hecho -- reutiliza `GuiaRepository.existe_alguna_de()`|
|[`editarActividadesFormativasMateria()`](editarActividadesFormativasMateria/README.md)|Diseño hecho -- `GET`/`PUT /api/v1/materias/{id}/actividades-formativas`, rejilla de un submit, `422` transaccional (clúster `ActividadFormativa`, discussion [#227](https://github.com/mmasias/pyCelda/discussions/227))|
|[`editarActividadesFormativasAsignaturaPrograma()`](editarActividadesFormativasAsignaturaPrograma/README.md)|Diseño hecho -- mismo patrón sobre `asignaturas-programa/{id}`, con `porcentaje_presencialidad` (rango 0-100)|
|[`consultarEstadoActividadesFormativasMateria()`](consultarEstadoActividadesFormativasMateria/README.md)|Diseño hecho, código 🚧 -- `GET .../actividades-formativas/validacion`, medidor blando `AfM = Σ AfAdM` en `Materia.discrepancias_actividades_formativas()`|

## Catálogo de `Admin`, autenticación y `PlanificacionDocente` (L0-L1, L10)

|Caso|Estado|
|-|-|
|[`abrirActividadesFormativas()`](abrirActividadesFormativas/README.md)|Hecho|
|[`abrirActividadFormativa()`](abrirActividadFormativa/README.md)|Hecho|
|[`abrirAsignatura()`](abrirAsignatura/README.md)|Hecho|
|[`abrirAsignaturas()`](abrirAsignaturas/README.md)|Hecho|
|[`abrirFacultad()`](abrirFacultad/README.md)|Hecho|
|[`abrirFacultades()`](abrirFacultades/README.md)|Hecho|
|[`abrirMetodologiaDocente()`](abrirMetodologiaDocente/README.md)|Hecho|
|[`abrirMetodologiasDocentes()`](abrirMetodologiasDocentes/README.md)|Hecho|
|[`abrirMetodologiasDocentesPrograma()`](abrirMetodologiasDocentesPrograma/README.md)|Hecho|
|[`abrirInicio()`](abrirInicio/README.md)|Hecho -- sin endpoint propio; compone `abrirAsignaturasPrograma()`/`abrirProgramas()` (endpoints `_opcional` -> `[]`); discussion #274|
|[`abrirPanelAdministracion()`](abrirPanelAdministracion/README.md)|Hecho -- sin endpoint de backend (menú resuelto en el cliente, sin fetch)|
|[`abrirPlanificacionDocente()`](abrirPlanificacionDocente/README.md)|Hecho|
|[`abrirProfesor()`](abrirProfesor/README.md)|Hecho|
|[`abrirProfesores()`](abrirProfesores/README.md)|Hecho|
|[`abrirSistemaEvaluacion()`](abrirSistemaEvaluacion/README.md)|Hecho|
|[`abrirSistemasEvaluacion()`](abrirSistemasEvaluacion/README.md)|Hecho|
|[`abrirUniversidad()`](abrirUniversidad/README.md)|Hecho|
|[`abrirUniversidades()`](abrirUniversidades/README.md)|Hecho|
|[`asignarProfesorAAsignaturaPrograma()`](asignarProfesorAAsignaturaPrograma/README.md)|Hecho|
|[`crearActividadFormativa()`](crearActividadFormativa/README.md)|Hecho|
|[`crearAsignatura()`](crearAsignatura/README.md)|Hecho|
|[`crearAsignaturaPrograma()`](crearAsignaturaPrograma/README.md)|Hecho|
|[`crearFacultad()`](crearFacultad/README.md)|Hecho|
|[`crearPrograma()`](crearPrograma/README.md)|Hecho|
|[`crearMateria()`](crearMateria/README.md)|Hecho|
|[`crearMetodologiaDocente()`](crearMetodologiaDocente/README.md)|Hecho|
|[`crearProfesor()`](crearProfesor/README.md)|Hecho|
|[`crearSesion()`](crearSesion/README.md)|Hecho|
|[`crearSistemaEvaluacion()`](crearSistemaEvaluacion/README.md)|Hecho|
|[`crearUniversidad()`](crearUniversidad/README.md)|Hecho|
|[`definirDirectorPrograma()`](definirDirectorPrograma/README.md)|Hecho|
|[`desasignarProfesorAsignaturaPrograma()`](desasignarProfesorAsignaturaPrograma/README.md)|Hecho|
|[`editarActividadFormativa()`](editarActividadFormativa/README.md)|Hecho|
|[`editarAsignatura()`](editarAsignatura/README.md)|Hecho|
|[`editarFacultad()`](editarFacultad/README.md)|Hecho|
|[`editarPrograma()`](editarPrograma/README.md)|Hecho|
|[`editarMateria()`](editarMateria/README.md)|Hecho|
|[`editarMetodologiaDocente()`](editarMetodologiaDocente/README.md)|Hecho|
|[`editarProfesor()`](editarProfesor/README.md)|Hecho|
|[`editarSesion()`](editarSesion/README.md)|Hecho|
|[`editarSistemaEvaluacion()`](editarSistemaEvaluacion/README.md)|Hecho|
|[`editarUniversidad()`](editarUniversidad/README.md)|Hecho|
|[`eliminarActividadFormativa()`](eliminarActividadFormativa/README.md)|Hecho|
|[`eliminarAsignatura()`](eliminarAsignatura/README.md)|Hecho|
|[`eliminarAsignaturaPrograma()`](eliminarAsignaturaPrograma/README.md)|Hecho|
|[`eliminarFacultad()`](eliminarFacultad/README.md)|Hecho|
|[`eliminarPrograma()`](eliminarPrograma/README.md)|Hecho|
|[`eliminarMetodologiaDocente()`](eliminarMetodologiaDocente/README.md)|Hecho|
|[`eliminarProfesor()`](eliminarProfesor/README.md)|Hecho|
|[`eliminarSesion()`](eliminarSesion/README.md)|Hecho -- sin endpoint de backend (mutación de lista de trabajo en cliente)|
|[`eliminarSistemaEvaluacion()`](eliminarSistemaEvaluacion/README.md)|Hecho|
|[`iniciarSesion()`](iniciarSesion/README.md)|Hecho -- rama Admin con endpoint separado y whitelist, sin `AdminRepository`|
|[`quitarDirectorPrograma()`](quitarDirectorPrograma/README.md)|Hecho|

## Fichas añadidas tras el último recuento

Existían como carpeta con ficha pero no figuraban en este índice (sincronizado en el issue [#658](https://github.com/mmasias/pyCelda/issues/658)).

|Caso|Estado|
|-|-|
|[`activarCursoAcademico()`](activarCursoAcademico/README.md)|Hecho|
|[`crearCursoAcademico()`](crearCursoAcademico/README.md)|Hecho|
|[`generarPlanificacionDocenteGenerica()`](generarPlanificacionDocenteGenerica/README.md)|Hecho|
|[`importarBibliografiaDeGuiaHermana()`](importarBibliografiaDeGuiaHermana/README.md)|Hecho|
|[`importarPlanificacionDocenteDeGuiaHermana()`](importarPlanificacionDocenteDeGuiaHermana/README.md)|Hecho|
|[`importarPlanificacionDocenteDesdeTexto()`](importarPlanificacionDocenteDesdeTexto/README.md)|Hecho|
|[`abrirCursoAcademico()`](abrirCursoAcademico/README.md)|Hecho|
|[`abrirCursosAcademicos()`](abrirCursosAcademicos/README.md)|Hecho|
|[`activarSemestre()`](activarSemestre/README.md)|Hecho|
|[`editarCursoAcademico()`](editarCursoAcademico/README.md)|Hecho|
|[`editarPerfilPropio()`](editarPerfilPropio/README.md)|Hecho|
|[`consultarCopiasSeguridad()`](consultarCopiasSeguridad/README.md)|Hecho|
|[`comprobarCopiasSeguridad()`](comprobarCopiasSeguridad/README.md)|Hecho|
|[`consultarHistorialCambios()`](consultarHistorialCambios/README.md)|Hecho|
|[`importarContenidoDeGuiaHermana()`](importarContenidoDeGuiaHermana/README.md)|Hecho|
|[`asociarMetodologiaDocenteAPrograma()`](asociarMetodologiaDocenteAPrograma/README.md)|Hecho|
|[`desasociarMetodologiaDocentePrograma()`](desasociarMetodologiaDocentePrograma/README.md)|Hecho|
|[`duplicarSesion()`](duplicarSesion/README.md)|Hecho|
|[`editarTextoSistemaEvaluacion()`](editarTextoSistemaEvaluacion/README.md)|Hecho|
|[`importarActividadesFormativasDeAsignaturaProgramaPrima()`](importarActividadesFormativasDeAsignaturaProgramaPrima/README.md)|Hecho|

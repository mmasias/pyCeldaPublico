export const API_BASE = "";

export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}

export interface PonderacionEvaluacion {
  id: number;
  guia_id: number;
  sistema_evaluacion_id: number;
  sistema_evaluacion: SistemaEvaluacionResponse;
  descripcion: string;
  ponderacion: number;
  vinculada: boolean;
}

export interface ReferenciaBibliografica {
  id: number;
  guia_id: number;
  tipo: string;
  referencia: string;
  vinculada: boolean;
}

export interface GuiaResponse {
  id: number;
  estado: string;
  semestre: number | null;
  // Temario propio de la Guia (fase de impartición), editable por el Profesor
  // -- independiente de asignatura_programa.contenido (discussion #191).
  contenido: string;
  // issue #610: texto de convocatorias del apartado 5, con [TABLA] una vez.
  texto_sistema_evaluacion: string;
  // Nullable, sin backfill (discussion #227): las guías creadas antes de
  // este campo no tienen ese dato real -- null, no una fecha inventada.
  fecha_creacion: string | null;
  fecha_ultima_modificacion: string;
  fecha_generacion_pdf: string | null;
}

export interface AsignaturaProgramaDeGuiaResponse {
  nombre: string;
  programa_nombre: string | null;
  contenido: string;
  resultados_aprendizaje: ResultadoAprendizajeResponse[];
  metodologias_docentes: MetodologiaDocenteResponse[];
  // Solo lectura -- discussion #227. Se edita desde
  // editarActividadesFormativasAsignaturaPrograma(), no desde aquí.
  actividades_formativas: ActividadFormativaAsignaturaProgramaResponse[];
}

export interface ResumenCompletitudResponse {
  sin_pendientes: boolean;
  ponderaciones_ok: boolean;
  motivo_ponderaciones: string | null;
  planificacion_docente_ok: boolean;
  sesiones_vinculadas: number;
}

export interface AbrirGuiaResponse extends GuiaResponse {
  ponderaciones: PonderacionEvaluacion[];
  referencias: ReferenciaBibliografica[];
  asignatura_programa: AsignaturaProgramaDeGuiaResponse | null;
  puede_revisar: boolean;
  // issue #254: la plantilla AsignaturaPrograma -- Profesor en vivo, no la copia
  // Guia -- Profesor (que solo la lee el render del PDF/previsualización).
  profesorado: Profesor[];
  sesiones: Sesion[];
  // Umbral de la regla c3 (discussion #206), para el medidor "N / M sesiones".
  sesiones_minimas: number;
  // Banner: no null cuando la guía volvió a EnRevisión porque Admin cambió el
  // profesorado de la AsignaturaPrograma (issue #254).
  comentario_revision_por_profesorado: string | null;
  // issue #504: resumen c1/c2/c3 del gate real de enviarGuiaARevision() --
  // puramente informativo, lo muestra AbrirGuia.tsx solo en modoRevisor.
  resumen_completitud: ResumenCompletitudResponse;
}

export interface GuiaResumenResponse {
  id: number;
  estado: string;
  semestre: number | null;
  asignatura_programa_nombre: string | null;
  // issue #508: curso/semestre de la AsignaturaPrograma -- null si se borró.
  asignatura_programa_curso: number | null;
  asignatura_programa_semestre_default: number | null;
  profesorado: Profesor[];
  ultima_actualizacion: string;
  ultima_actualizacion_rol: string;
  // issue #262: la fila de la pantalla de Admin deshabilita "Descargar PDF"
  // cuando es false.
  tiene_pdf: boolean;
}

export interface RechazarGuiaRequest {
  comentario?: string;
}

export interface RevocarAprobacionGuiaRequest {
  comentario?: string;
}

export interface EditarSemestreGuiaRequest {
  semestre: number;
}

export interface NotificacionResponse {
  detail: string;
}

// issues #441/#442: CursoAcademico -- selector compartido entre
// consultarEstadoGuias() y la Auditoría. `estado` es "Activo"/"Inactivo".
export interface CursoAcademico {
  id: number;
  inicio: string;
  fin: string;
  estado: string;
  semestre_activo: number | null;
  // issue #471: cada Universidad tiene su propio plan de CursoAcademico.
  universidad_id: number | null;
}

async function get<T>(ruta: string): Promise<T> {
  const res = await fetch(`${API_BASE}${ruta}`, { credentials: "include" });
  if (!res.ok) {
    const body = (await res.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(res.status, body?.detail ?? `HTTP ${res.status}`);
  }
  return (await res.json()) as T;
}

async function enviar<T>(
  metodo: "POST" | "PUT" | "DELETE",
  ruta: string,
  cuerpo?: unknown,
): Promise<T> {
  const res = await fetch(`${API_BASE}${ruta}`, {
    method: metodo,
    credentials: "include",
    headers: cuerpo !== undefined ? { "Content-Type": "application/json" } : undefined,
    body: cuerpo !== undefined ? JSON.stringify(cuerpo) : undefined,
  });
  if (!res.ok) {
    const body = (await res.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(res.status, body?.detail ?? `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

async function post<T>(ruta: string, cuerpo?: unknown): Promise<T> {
  return enviar<T>("POST", ruta, cuerpo);
}

async function put<T>(ruta: string, cuerpo: unknown): Promise<T> {
  return enviar<T>("PUT", ruta, cuerpo);
}

async function del(ruta: string): Promise<void> {
  await enviar<void>("DELETE", ruta);
}

export async function abrirGuia(guiaId: number): Promise<AbrirGuiaResponse> {
  return get<AbrirGuiaResponse>(`/api/v1/guias/${guiaId}`);
}

export async function listarGuiasDelPrograma(
  programaId: number,
  // issue #441: sin indicar, el curso ACTIVO (default del backend).
  cursoAcademicoId?: number,
): Promise<GuiaResumenResponse[]> {
  const query = cursoAcademicoId != null ? `?curso=${cursoAcademicoId}` : "";
  return get<GuiaResumenResponse[]>(`/api/v1/programas/${programaId}/guias${query}`);
}

// issues #441/#442: selector compartido, gate dual Admin-o-DirectorPrograma.
// issue #471: universidadId opcional -- deuda diferida (issue #472), los
// 3 consumidores actuales de este selector (ConsultarEstadoGuias.tsx/
// ConsultarEstadoGuiasAdmin.tsx/HistorialCambios.tsx) todavía no lo pasan.
export async function listarCursosAcademicosSelector(
  universidadId?: number,
): Promise<CursoAcademico[]> {
  const query = universidadId != null ? `?universidad_id=${universidadId}` : "";
  return get<CursoAcademico[]>(`/api/v1/cursos-academicos${query}`);
}

// issue #446: listado de gestión de Admin -- extiende CursoAcademico con el
// campo derivado que decide si el botón [Activar] se pinta en esa fila.
// issue #454: tiene_guia_asociada decide la variante (formulario vs
// bloqueada) de la pantalla de editar.
export interface CursoAcademicoAdmin extends CursoAcademico {
  elegible_para_activar: boolean;
  tiene_guia_asociada: boolean;
}

export interface CrearCursoAcademicoRequest {
  inicio: string; // "AAAA-MM-DD"
  fin: string;
}

export interface EditarCursoAcademicoRequest {
  inicio: string; // "AAAA-MM-DD"
  fin: string;
}

// issue #471: rutas anidadas bajo /universidades/{id}/ -- mismo patrón que
// Facultad. universidad_id ya no viaja en el body de CrearCursoAcademicoRequest,
// viene del path.
export async function listarCursosAcademicosAdmin(
  universidadId: number,
): Promise<CursoAcademicoAdmin[]> {
  return get<CursoAcademicoAdmin[]>(
    `/api/v1/universidades/${universidadId}/cursos-academicos`,
  );
}

export async function crearCursoAcademicoAdmin(
  universidadId: number,
  datos: CrearCursoAcademicoRequest,
): Promise<CursoAcademico> {
  return post<CursoAcademico>(
    `/api/v1/universidades/${universidadId}/cursos-academicos`,
    datos,
  );
}

// issue #471: sin endpoint de detalle individual (patrón de #446/#454) --
// con universidad_id ahora obligatorio en el listado de gestión, buscar un
// CursoAcademico por id (sin saber a qué Universidad pertenece, caso de
// AbrirCursoAcademicoAdmin.tsx/EditarCursoAcademicoAdmin.tsx/
// ActivarCursoAcademicoAdmin.tsx/ActivarSemestreCursoAcademicoAdmin.tsx,
// que solo reciben el id por la URL) recorre las Universidades una a una
// hasta encontrarlo. Secuencial, no Promise.all: con 1 sola Universidad
// real hoy son 2 peticiones igual que antes; el caso N Universidades es
// backlog de gestión de Admin, no una pantalla de alto tráfico. Devuelve
// también el resto de cursos de la MISMA Universidad -- ActivarCursoAcademicoAdmin.tsx
// necesita el Activo previo dentro de esa institución, no de cualquiera.
export async function buscarCursoAcademicoAdminPorId(
  id: number,
): Promise<{ curso: CursoAcademicoAdmin; cursosDeLaMismaUniversidad: CursoAcademicoAdmin[] } | null> {
  const universidades = await listarUniversidades();
  for (const universidad of universidades) {
    const cursos = await listarCursosAcademicosAdmin(universidad.id);
    const encontrado = cursos.find((c) => c.id === id);
    if (encontrado !== undefined) {
      return { curso: encontrado, cursosDeLaMismaUniversidad: cursos };
    }
  }
  return null;
}

export async function activarCursoAcademicoAdmin(id: number): Promise<CursoAcademico> {
  return post<CursoAcademico>(`/api/v1/admin/cursos-academicos/${id}/activar`);
}

export async function editarCursoAcademicoAdmin(
  id: number,
  datos: EditarCursoAcademicoRequest,
): Promise<CursoAcademico> {
  return put<CursoAcademico>(`/api/v1/admin/cursos-academicos/${id}`, datos);
}

export async function activarSemestreCursoAcademicoAdmin(
  id: number,
  semestre: 1 | 2,
): Promise<CursoAcademico> {
  return put<CursoAcademico>(`/api/v1/admin/cursos-academicos/${id}/semestre`, { semestre });
}

export async function aprobarGuia(guiaId: number): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/aprobar`);
}

export async function rechazarGuia(
  guiaId: number,
  datos: RechazarGuiaRequest,
): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/rechazar`, datos);
}

export async function escalarGuiaAAprobada(guiaId: number): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/escalar-a-aprobada`);
}

export async function revocarAprobacionGuia(
  guiaId: number,
  datos: RevocarAprobacionGuiaRequest,
): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/revocar-aprobacion`, datos);
}

export async function editarSemestreGuia(
  guiaId: number,
  datos: EditarSemestreGuiaRequest,
): Promise<GuiaResponse> {
  return put<GuiaResponse>(`/api/v1/guias/${guiaId}/semestre`, datos);
}

export async function editarTextoSistemaEvaluacion(
  guiaId: number,
  texto: string,
): Promise<GuiaResponse> {
  return put<GuiaResponse>(`/api/v1/guias/${guiaId}/texto-sistema-evaluacion`, { texto });
}

export async function notificarGuiasActualizadas(
  programaId: number,
): Promise<NotificacionResponse> {
  return post<NotificacionResponse>(
    `/api/v1/programas/${programaId}/notificar-guias-actualizadas`,
  );
}

export interface GuardarBorradorGuiaRequest {
  ids_ponderaciones_final: number[];
  ids_referencias_final: number[];
  ids_sesiones_final: number[];
  // Ausente = no se toca el temario en esta petición; string = se aplica.
  contenido?: string;
}

export async function guardarBorradorGuia(
  guiaId: number,
  datos: GuardarBorradorGuiaRequest,
): Promise<GuiaResponse> {
  return put<GuiaResponse>(`/api/v1/guias/${guiaId}/borrador`, datos);
}

export async function enviarGuiaARevision(guiaId: number): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/enviar-a-revision`);
}

// previsualizarGuia() (discussion #218): vista HTML de la guía renderizada con
// la plantilla oficial, cualquier estado, aviso de borrador no oficial si no
// está Aprobada. GET same-origin, la cookie de sesión viaja sola -- se abre en
// pestaña nueva, no hay respuesta que parsear.
export function previsualizarGuia(guiaId: number): void {
  window.open(`${API_BASE}/api/v1/guias/${guiaId}/vista`, "_blank");
}

export async function descargarGuiaPDF(guiaId: number): Promise<Blob> {
  const res = await fetch(`${API_BASE}/api/v1/guias/${guiaId}/pdf`, {
    credentials: "include",
  });
  if (!res.ok) {
    const body = (await res.json().catch(() => null)) as { detail?: string } | null;
    throw new ApiError(res.status, body?.detail ?? `HTTP ${res.status}`);
  }
  return res.blob();
}

export interface SistemaEvaluacionResponse {
  id: number;
  materia_id: number;
  tipo: string;
  descripcion: string;
  ponderacion_minima: number;
  ponderacion_maxima: number;
}

export async function listarSistemasEvaluacion(
  materiaId: number,
): Promise<SistemaEvaluacionResponse[]> {
  return get<SistemaEvaluacionResponse[]>(`/api/v1/materias/${materiaId}/sistemas-evaluacion`);
}

export async function listarSistemasEvaluacionDeGuia(
  guiaId: number,
): Promise<SistemaEvaluacionResponse[]> {
  return get<SistemaEvaluacionResponse[]>(`/api/v1/guias/${guiaId}/sistemas-evaluacion`);
}

// --- SistemaEvaluacion (composición de Materia, variante Admin: require_admin)
// El listado Admin cuelga del namespace /admin/ porque el path sin /admin/
// ya existe como selector de Profesor de CrearPonderacionEvaluacion/
// EditarPonderacionEvaluacion (listarSistemasEvaluacion, arriba) -- un mismo
// path no puede registrar dos guardas distintas. El resto de endpoints no
// colisiona y usa el path natural.

export interface SistemaEvaluacionCreate {
  tipo: string;
  descripcion?: string;
  ponderacion_minima: number;
  ponderacion_maxima: number;
}

export type SistemaEvaluacionUpdate = SistemaEvaluacionCreate;

export async function listarSistemasEvaluacionDeMateria(
  materiaId: number,
): Promise<SistemaEvaluacionResponse[]> {
  return get<SistemaEvaluacionResponse[]>(
    `/api/v1/admin/materias/${materiaId}/sistemas-evaluacion`,
  );
}

export async function obtenerSistemaEvaluacion(
  sistemaEvaluacionId: number,
): Promise<SistemaEvaluacionResponse> {
  return get<SistemaEvaluacionResponse>(`/api/v1/sistemas-evaluacion/${sistemaEvaluacionId}`);
}

export async function crearSistemaEvaluacion(
  materiaId: number,
  datos: SistemaEvaluacionCreate,
): Promise<SistemaEvaluacionResponse> {
  return post<SistemaEvaluacionResponse>(
    `/api/v1/materias/${materiaId}/sistemas-evaluacion`,
    datos,
  );
}

export async function editarSistemaEvaluacion(
  sistemaEvaluacionId: number,
  datos: SistemaEvaluacionUpdate,
): Promise<SistemaEvaluacionResponse> {
  return put<SistemaEvaluacionResponse>(
    `/api/v1/sistemas-evaluacion/${sistemaEvaluacionId}`,
    datos,
  );
}

export async function eliminarSistemaEvaluacion(sistemaEvaluacionId: number): Promise<void> {
  // 204 si elimina de verdad; 409 (con el conteo de ponderaciones asociadas
  // en el detail) llega como ApiError -- mismo patrón que el resto de deletes
  return del(`/api/v1/sistemas-evaluacion/${sistemaEvaluacionId}`);
}

export interface PonderacionEvaluacionDatos {
  sistema_evaluacion_id: number;
  descripcion: string;
  ponderacion: number;
}

export async function crearPonderacionEvaluacion(
  guiaId: number,
  datos: PonderacionEvaluacionDatos,
): Promise<PonderacionEvaluacion> {
  return post<PonderacionEvaluacion>(`/api/v1/guias/${guiaId}/ponderaciones-evaluacion`, datos);
}

export async function obtenerPonderacionEvaluacion(id: number): Promise<PonderacionEvaluacion> {
  return get<PonderacionEvaluacion>(`/api/v1/ponderaciones-evaluacion/${id}`);
}

export async function editarPonderacionEvaluacion(
  id: number,
  datos: PonderacionEvaluacionDatos,
): Promise<PonderacionEvaluacion> {
  return put<PonderacionEvaluacion>(`/api/v1/ponderaciones-evaluacion/${id}`, datos);
}

export async function listarPonderacionesEvaluacion(
  guiaId: number,
): Promise<PonderacionEvaluacion[]> {
  return get<PonderacionEvaluacion[]>(`/api/v1/guias/${guiaId}/ponderaciones-evaluacion`);
}

export interface Sesion {
  id: number;
  guia_id: number;
  numero: number;
  tipo: string;
  descripcion: string;
  vinculada: boolean;
}

export interface SesionDatos {
  tipo: string;
  descripcion: string;
}

export interface AbrirPlanificacionDocenteResponse {
  sesiones: Sesion[];
  // Umbral de la regla c3 (discussion #206), para el medidor "N / M sesiones".
  sesiones_minimas: number;
}

export async function listarSesiones(
  guiaId: number,
): Promise<AbrirPlanificacionDocenteResponse> {
  return get<AbrirPlanificacionDocenteResponse>(`/api/v1/guias/${guiaId}/sesiones`);
}

export async function crearSesion(
  guiaId: number,
  datos: SesionDatos,
): Promise<Sesion> {
  return post<Sesion>(`/api/v1/guias/${guiaId}/sesiones`, datos);
}

// generarPlanificacionDocenteGenerica() (familia del issue #184): arranca la
// planificación docente vacía con N sesiones planas CLASE_TEORICA vinculadas
// (N = sesiones_minimas de la guía). 409 si ya hay sesiones.
export async function generarSesionesGenericas(
  guiaId: number,
): Promise<AbrirPlanificacionDocenteResponse> {
  return post<AbrirPlanificacionDocenteResponse>(
    `/api/v1/guias/${guiaId}/sesiones/generar-genericas`,
  );
}

export async function editarSesion(
  id: number,
  datos: SesionDatos,
): Promise<Sesion> {
  return put<Sesion>(`/api/v1/sesiones/${id}`, datos);
}

// duplicar_sesion() (#364): copia tipo+descripcion, inserta la copia justo
// después en la numeración y renumera +1 las posteriores. Devuelve el
// envelope completo ya renumerado, no solo la sesión nueva -- mismo patrón
// que generarSesionesGenericas().
export async function duplicarSesion(
  id: number,
): Promise<AbrirPlanificacionDocenteResponse> {
  return post<AbrirPlanificacionDocenteResponse>(`/api/v1/sesiones/${id}/duplicar`);
}

export interface ReferenciaBibliograficaDatos {
  tipo: string;
  referencia: string;
}

export async function crearReferenciaBibliografica(
  guiaId: number,
  datos: ReferenciaBibliograficaDatos,
): Promise<ReferenciaBibliografica> {
  return post<ReferenciaBibliografica>(`/api/v1/guias/${guiaId}/referencias-bibliograficas`, datos);
}

export async function obtenerReferenciaBibliografica(id: number): Promise<ReferenciaBibliografica> {
  return get<ReferenciaBibliografica>(`/api/v1/referencias-bibliograficas/${id}`);
}

export async function editarReferenciaBibliografica(
  id: number,
  datos: ReferenciaBibliograficaDatos,
): Promise<ReferenciaBibliografica> {
  return put<ReferenciaBibliografica>(`/api/v1/referencias-bibliograficas/${id}`, datos);
}

export async function listarReferenciasBibliograficas(
  guiaId: number,
): Promise<ReferenciaBibliografica[]> {
  return get<ReferenciaBibliografica[]>(`/api/v1/guias/${guiaId}/referencias-bibliograficas`);
}

// --- Importación desde guías hermanas (issue #184) ----------------------------
// Guías Aprobadas de AsignaturaPrograma hermanas (misma Asignatura, otro Programa)
// de las que un Profesor puede copiar bibliografía o planificación docente.

export interface GuiaHermanaImportable {
  guia_id: number;
  programa_codigo: string;
  asignatura_codigo: string;
  asignatura_programa_nombre: string;
  fecha_aprobacion: string | null;
  n_referencias: number;
  n_sesiones: number;
}

export async function listarGuiasImportables(guiaId: number): Promise<GuiaHermanaImportable[]> {
  return get<GuiaHermanaImportable[]>(`/api/v1/guias/${guiaId}/importables`);
}

export async function importarBibliografiaDeGuiaHermana(
  guiaId: number,
  origenGuiaId: number,
): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/importar-bibliografia`, {
    origen_guia_id: origenGuiaId,
  });
}

export async function importarPlanificacionDocenteDeGuiaHermana(
  guiaId: number,
  origenGuiaId: number,
): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/importar-planificacion-docente`, {
    origen_guia_id: origenGuiaId,
  });
}

export async function importarPlanificacionDocenteDesdeTexto(
  guiaId: number,
  texto: string,
): Promise<GuiaResponse> {
  return post<GuiaResponse>(
    `/api/v1/guias/${guiaId}/importar-planificacion-docente-desde-texto`,
    { texto },
  );
}

export async function importarContenidoDeGuiaHermana(
  guiaId: number,
  origenGuiaId: number,
): Promise<GuiaResponse> {
  return post<GuiaResponse>(`/api/v1/guias/${guiaId}/importar-contenido`, {
    origen_guia_id: origenGuiaId,
  });
}

export type Rol = "director_programa" | "profesor" | "admin";

export interface SesionResponse {
  email: string;
  rol: Rol;
  es_tambien_profesor: boolean;
  // discussion #274: señales independientes que abrirInicio() consume para
  // decidir qué secciones muestra ("Mis guías" / "Mis programas").
  es_profesor: boolean;
  dirige_programas: boolean;
}

export async function obtenerSesion(): Promise<SesionResponse> {
  return get<SesionResponse>("/auth/me");
}

export async function cerrarSesion(): Promise<void> {
  await fetch(`${API_BASE}/auth/logout`, { method: "POST", credentials: "include" });
}

export interface Profesor {
  id: number;
  nombre: string | null;
  email: string;
  // issue #471: nullable -- filas legado pueden no tenerla backfilleada
  // (mismo criterio que Programa.facultad_id).
  universidad_id: number | null;
  // Carga docente actual (issue #310). Real solo en listarProfesores(); en el
  // resto de sitios que devuelven Profesor (profesorado anidado de
  // AsignaturaPrograma/Guia) llega a 0 sin significado -- no se muestra ahí.
  num_asignaturas_programa: number;
}

export interface DirectorProgramaResponse {
  profesor_id: number;
  nombre: string | null;
  email: string;
}

export interface ProgramaResponse {
  id: number;
  codigo: string;
  nombre: string;
  estado: string;
  facultad_id: number | null;
  // Issue #492: real solo en obtenerProgramaAdmin() -- el resto de sitios que
  // devuelven ProgramaResponse (vista propia del Director, listado de
  // Facultad) llegan a [] sin significado, mismo criterio que
  // num_asignaturas_programa en Profesor.
  directores: DirectorProgramaResponse[];
}

export interface AsignaturaProgramaResponse {
  id: number;
  nombre: string;
  curso: number;
  caracter: string;
  idioma: string;
  ects: number;
  semestre_default: number;
  contenido: string;
  // Requisitos previos, texto plano leído en vivo por el render de la guía
  // (discussion #259). null == "No aplica".
  requisitos_previos: string | null;
  sesiones_minimas: number;
  estado: string;
  materia_id: number;
  materia_nombre: string;
  programa_id: number | null;
  programa_nombre: string | null;
  asignatura_id: number | null;
}

export interface AsignaturaProgramaConEstadoGuiaResponse extends AsignaturaProgramaResponse {
  profesorado: Profesor[];
  estado_guia: string | null;
}

export interface ProgramaDetalleResponse extends ProgramaResponse {
  asignaturas_programa: AsignaturaProgramaResponse[];
}

export interface MateriaResponse {
  id: number;
  nombre: string;
  programa_id: number | null;
  // Issue #487: real solo en listarMateriasDeProgramaAdmin().
  num_asignaturas_programa: number;
}

export interface MetodologiaDocenteResponse {
  id: number;
  // Issue #655: el catálogo es por Universidad.
  universidad_id: number;
  codigo: string;
  descripcion: string;
}

export interface MetodologiaMateriaResponse {
  materia_id: number;
  metodologia_docente_id: number;
  descripcion_propia: string;
  metodologia_docente: MetodologiaDocenteResponse;
}

export interface ResultadoAprendizajeResponse {
  id: number;
  programa_id: number;
  codigo: string;
  tipo: string;
  descripcion: string;
  numero_asignaturas: number | null;
}

export interface ActividadFormativaMateriaResponse {
  actividad_formativa_id: number;
  codigo: string;
  nombre: string;
  horas: number;
}

export interface MateriaDetalleResponse extends MateriaResponse {
  metodologias_docentes: MetodologiaMateriaResponse[];
  resultados_aprendizaje: ResultadoAprendizajeResponse[];
  asignaturas_programa: AsignaturaProgramaResponse[];
  sistemas_evaluacion: SistemaEvaluacionResponse[];
  actividades_formativas: ActividadFormativaMateriaResponse[];
}

export async function listarProgramas(): Promise<ProgramaResponse[]> {
  return get<ProgramaResponse[]>("/api/v1/programas");
}

export async function obtenerPrograma(programaId: number): Promise<ProgramaDetalleResponse> {
  return get<ProgramaDetalleResponse>(`/api/v1/programas/${programaId}`);
}

export async function listarAsignaturasPrograma(
  programaId: number,
): Promise<AsignaturaProgramaConEstadoGuiaResponse[]> {
  return get<AsignaturaProgramaConEstadoGuiaResponse[]>(
    `/api/v1/programas/${programaId}/asignaturas-programa`,
  );
}

export interface AsignaturaProgramaParaProfesorResponse {
  id: number;
  nombre: string;
  curso: number;
  caracter: string;
  idioma: string;
  ects: number;
  semestre_default: number;
  contenido: string;
  estado: string;
  materia_id: number;
  materia_nombre: string;
  programa_id: number | null;
  programa_nombre: string | null;
  asignatura_codigo: string | null;
  guia_id: number | null;
  estado_guia: string | null;
  comentario_rechazo: string | null;
  comentario_revocacion: string | null;
}

export async function listarMisAsignaturasPrograma(): Promise<AsignaturaProgramaParaProfesorResponse[]> {
  return get<AsignaturaProgramaParaProfesorResponse[]>("/api/v1/mis-asignaturas-programa");
}

export async function listarMaterias(programaId: number): Promise<MateriaResponse[]> {
  return get<MateriaResponse[]>(`/api/v1/programas/${programaId}/materias`);
}

export async function obtenerMateria(materiaId: number): Promise<MateriaDetalleResponse> {
  return get<MateriaDetalleResponse>(`/api/v1/materias/${materiaId}`);
}

// --- ActividadFormativa a nivel Materia (discussion #227) --------------------
// Catálogo institucional seed-estático, sin CRUD -- solo el reparto de horas
// de la materia, en rejilla, un submit.

export interface ActividadFormativaMateriaItem {
  actividad_formativa_id: number;
  horas: number;
}

export async function obtenerActividadesFormativasMateria(
  materiaId: number,
): Promise<ActividadFormativaMateriaResponse[]> {
  return get<ActividadFormativaMateriaResponse[]>(
    `/api/v1/materias/${materiaId}/actividades-formativas`,
  );
}

export async function editarActividadesFormativasMateria(
  materiaId: number,
  actividades: ActividadFormativaMateriaItem[],
): Promise<ActividadFormativaMateriaResponse[]> {
  return put<ActividadFormativaMateriaResponse[]>(
    `/api/v1/materias/${materiaId}/actividades-formativas`,
    { actividades },
  );
}

// consultarEstadoActividadesFormativasMateria() -- medidor de la regla
// AfM = ΣAfAdM, solo lectura, compuesto desde abrirMateria() (discussion #227).
export interface DiscrepanciaActividadFormativaResponse {
  codigo: string;
  nombre: string;
  horas_materia: number;
  horas_asignaturas: number;
  cuadra: boolean;
  diferencia: number;
}

export async function consultarEstadoActividadesFormativasMateria(
  materiaId: number,
): Promise<DiscrepanciaActividadFormativaResponse[]> {
  return get<DiscrepanciaActividadFormativaResponse[]>(
    `/api/v1/materias/${materiaId}/actividades-formativas/validacion`,
  );
}

export async function listarResultadosAprendizaje(
  programaId: number,
): Promise<ResultadoAprendizajeResponse[]> {
  return get<ResultadoAprendizajeResponse[]>(
    `/api/v1/programas/${programaId}/resultados-aprendizaje`,
  );
}

export async function obtenerResultadoAprendizaje(
  resultadoId: number,
): Promise<ResultadoAprendizajeResponse> {
  return get<ResultadoAprendizajeResponse>(`/api/v1/resultados-aprendizaje/${resultadoId}`);
}

export const TIPOS_RESULTADO_APRENDIZAJE = [
  "Conocimientos o contenidos",
  "Competencias o capacidades",
  "Habilidades o destrezas",
] as const;

export interface ResultadoAprendizajeCreate {
  codigo: string;
  tipo: string;
  descripcion: string;
}

export type ResultadoAprendizajeUpdate = ResultadoAprendizajeCreate;

export async function crearResultadoAprendizaje(
  programaId: number,
  datos: ResultadoAprendizajeCreate,
): Promise<ResultadoAprendizajeResponse> {
  return post<ResultadoAprendizajeResponse>(
    `/api/v1/programas/${programaId}/resultados-aprendizaje`,
    datos,
  );
}

export async function editarResultadoAprendizaje(
  resultadoId: number,
  datos: ResultadoAprendizajeUpdate,
): Promise<ResultadoAprendizajeResponse> {
  return put<ResultadoAprendizajeResponse>(
    `/api/v1/resultados-aprendizaje/${resultadoId}`,
    datos,
  );
}

export interface ResultadoAprendizajeAsignacionesResponse {
  materias: string[];
  asignaturas_programa: string[];
}

export async function obtenerAsignacionesResultadoAprendizaje(
  resultadoId: number,
): Promise<ResultadoAprendizajeAsignacionesResponse> {
  return get<ResultadoAprendizajeAsignacionesResponse>(
    `/api/v1/resultados-aprendizaje/${resultadoId}/asignaciones`,
  );
}

export async function eliminarResultadoAprendizaje(resultadoId: number): Promise<void> {
  return del(`/api/v1/resultados-aprendizaje/${resultadoId}`);
}

export async function listarMetodologiasDocentesDisponiblesMateria(
  materiaId: number,
): Promise<MetodologiaDocenteResponse[]> {
  return get<MetodologiaDocenteResponse[]>(
    `/api/v1/materias/${materiaId}/metodologias-docentes/disponibles`,
  );
}

export async function asociarMetodologiaDocenteMateria(
  materiaId: number,
  metodologiaDocenteId: number,
): Promise<MetodologiaMateriaResponse> {
  return post<MetodologiaMateriaResponse>(
    `/api/v1/materias/${materiaId}/metodologias-docentes`,
    { metodologia_docente_id: metodologiaDocenteId },
  );
}

export async function obtenerAsociacionMetodologiaDocenteMateria(
  materiaId: number,
  metodologiaDocenteId: number,
): Promise<MetodologiaMateriaResponse> {
  return get<MetodologiaMateriaResponse>(
    `/api/v1/materias/${materiaId}/metodologias-docentes/${metodologiaDocenteId}`,
  );
}

export async function editarAsociacionMetodologiaDocenteMateria(
  materiaId: number,
  metodologiaDocenteId: number,
  descripcionPropia: string,
): Promise<MetodologiaMateriaResponse> {
  return put<MetodologiaMateriaResponse>(
    `/api/v1/materias/${materiaId}/metodologias-docentes/${metodologiaDocenteId}`,
    { descripcion_propia: descripcionPropia },
  );
}

/** issue #179: nombres de las AsignaturaPrograma que usan la MetodologiaDocente
 * -- [] significa que se puede desasociar. Antes boolean. */
export async function puedeDesasociarMetodologiaDocenteMateria(
  materiaId: number,
  metodologiaDocenteId: number,
): Promise<string[]> {
  return get<string[]>(
    `/api/v1/materias/${materiaId}/metodologias-docentes/${metodologiaDocenteId}/puede-desasociarse`,
  );
}

export async function desasociarMetodologiaDocenteMateria(
  materiaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return del(`/api/v1/materias/${materiaId}/metodologias-docentes/${metodologiaDocenteId}`);
}

export async function listarResultadosAprendizajeDisponiblesMateria(
  materiaId: number,
): Promise<ResultadoAprendizajeResponse[]> {
  return get<ResultadoAprendizajeResponse[]>(
    `/api/v1/materias/${materiaId}/resultados-aprendizaje/disponibles`,
  );
}

export async function asociarResultadoAprendizajeMateria(
  materiaId: number,
  resultadoAprendizajeId: number,
): Promise<void> {
  return post<void>(`/api/v1/materias/${materiaId}/resultados-aprendizaje`, {
    resultado_aprendizaje_id: resultadoAprendizajeId,
  });
}

/** issue #179: nombres de las AsignaturaPrograma que usan el ResultadoAprendizaje
 * -- [] significa que se puede desasociar. Antes boolean. */
export async function puedeDesasociarResultadoAprendizajeMateria(
  materiaId: number,
  resultadoAprendizajeId: number,
): Promise<string[]> {
  return get<string[]>(
    `/api/v1/materias/${materiaId}/resultados-aprendizaje/${resultadoAprendizajeId}/puede-desasociarse`,
  );
}

export async function desasociarResultadoAprendizajeMateria(
  materiaId: number,
  resultadoAprendizajeId: number,
): Promise<void> {
  return del(
    `/api/v1/materias/${materiaId}/resultados-aprendizaje/${resultadoAprendizajeId}`,
  );
}

export interface ActividadFormativaAsignaturaProgramaResponse {
  actividad_formativa_id: number;
  codigo: string;
  nombre: string;
  horas: number;
  porcentaje_presencialidad: number;
}

export interface AsignaturaProgramaDetalleResponse extends AsignaturaProgramaResponse {
  profesorado: Profesor[];
  metodologias_docentes: MetodologiaDocenteResponse[];
  resultados_aprendizaje: ResultadoAprendizajeResponse[];
  actividades_formativas: ActividadFormativaAsignaturaProgramaResponse[];
}

export interface AsignaturaProgramaParaEditarResponse extends AsignaturaProgramaResponse {
  semestre_default_bloqueado: boolean;
}

export interface AsignaturaProgramaUpdate {
  curso: number;
  caracter: string;
  idioma: string;
  semestre_default: number;
  nombre: string;
  ects: number;
  contenido: string;
  // Opcional: "" se normaliza a NULL en el backend (discussion #259).
  requisitos_previos: string;
}

export async function obtenerAsignaturaPrograma(
  asignaturaProgramaId: number,
): Promise<AsignaturaProgramaDetalleResponse> {
  return get<AsignaturaProgramaDetalleResponse>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}`,
  );
}

// --- ActividadFormativa a nivel AsignaturaPrograma (discussion #227) ------------
// Nivel que consume el render de la Guia (sección 4 del formulario oficial).

export interface ActividadFormativaAsignaturaProgramaItem {
  actividad_formativa_id: number;
  horas: number;
  porcentaje_presencialidad: number;
}

export async function obtenerActividadesFormativasAsignaturaPrograma(
  asignaturaProgramaId: number,
): Promise<ActividadFormativaAsignaturaProgramaResponse[]> {
  return get<ActividadFormativaAsignaturaProgramaResponse[]>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/actividades-formativas`,
  );
}

export async function editarActividadesFormativasAsignaturaPrograma(
  asignaturaProgramaId: number,
  actividades: ActividadFormativaAsignaturaProgramaItem[],
): Promise<ActividadFormativaAsignaturaProgramaResponse[]> {
  return put<ActividadFormativaAsignaturaProgramaResponse[]>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/actividades-formativas`,
    { actividades },
  );
}

export interface AsignaturaProgramaPrimaImportableResponse {
  asignatura_programa_id: number;
  nombre: string;
  ects: number;
  total_horas: number;
}

export async function listarPrimasImportablesActividadesFormativas(
  asignaturaProgramaId: number,
): Promise<AsignaturaProgramaPrimaImportableResponse[]> {
  return get<AsignaturaProgramaPrimaImportableResponse[]>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/actividades-formativas/importables`,
  );
}

export async function importarActividadesFormativasDeAsignaturaProgramaPrima(
  asignaturaProgramaId: number,
  origenAsignaturaProgramaId: number,
): Promise<ActividadFormativaAsignaturaProgramaResponse[]> {
  return post<ActividadFormativaAsignaturaProgramaResponse[]>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/actividades-formativas/importar`,
    { origen_asignatura_programa_id: origenAsignaturaProgramaId },
  );
}

export async function obtenerAsignaturaProgramaParaEditar(
  asignaturaProgramaId: number,
): Promise<AsignaturaProgramaParaEditarResponse> {
  return get<AsignaturaProgramaParaEditarResponse>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/para-editar`,
  );
}

export async function editarAsignaturaPrograma(
  asignaturaProgramaId: number,
  datos: AsignaturaProgramaUpdate,
): Promise<AsignaturaProgramaResponse> {
  return put<AsignaturaProgramaResponse>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}`,
    datos,
  );
}

export interface AsignaturaProgramaAdminParaEditarResponse extends AsignaturaProgramaResponse {
  materia_bloqueada: boolean;
  semestre_default_bloqueado: boolean;
}

export interface AsignaturaProgramaAdminUpdate {
  materia_id: number;
  curso: number;
  caracter: string;
  sesiones_minimas: number;
  idioma: string;
  semestre_default: number;
  nombre: string;
  ects: number;
  contenido: string;
  requisitos_previos: string | null;
}

export async function obtenerAsignaturaProgramaAdminParaEditar(
  asignaturaProgramaId: number,
): Promise<AsignaturaProgramaAdminParaEditarResponse> {
  return get<AsignaturaProgramaAdminParaEditarResponse>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/para-editar`,
  );
}

export async function editarAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
  datos: AsignaturaProgramaAdminUpdate,
): Promise<AsignaturaProgramaResponse> {
  return put<AsignaturaProgramaResponse>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}`,
    datos,
  );
}

export async function listarMetodologiasDocentesDisponiblesAsignaturaPrograma(
  asignaturaProgramaId: number,
): Promise<MetodologiaDocenteResponse[]> {
  return get<MetodologiaDocenteResponse[]>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes/disponibles`,
  );
}

export async function asociarMetodologiaDocenteAsignaturaPrograma(
  asignaturaProgramaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return post<void>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes`,
    { metodologia_docente_id: metodologiaDocenteId },
  );
}

export async function quedariaSinMetodologiasTrasDesasociar(
  asignaturaProgramaId: number,
  metodologiaDocenteId: number,
): Promise<boolean> {
  return get<boolean>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes/` +
      `${metodologiaDocenteId}/quedaria-sin-metodologias`,
  );
}

export async function desasociarMetodologiaDocenteAsignaturaPrograma(
  asignaturaProgramaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return del(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes/${metodologiaDocenteId}`,
  );
}

// --- MetodologiaDocente de un Programa (issue #526) -----------------------------

export async function listarMetodologiasDocentesPrograma(
  programaId: number,
): Promise<MetodologiaDocenteResponse[]> {
  return get<MetodologiaDocenteResponse[]>(`/api/v1/programas/${programaId}/metodologias-docentes`);
}

export async function listarMetodologiasDocentesDisponiblesPrograma(
  programaId: number,
): Promise<MetodologiaDocenteResponse[]> {
  return get<MetodologiaDocenteResponse[]>(
    `/api/v1/programas/${programaId}/metodologias-docentes/disponibles`,
  );
}

export async function asociarMetodologiaDocentePrograma(
  programaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return post<void>(`/api/v1/programas/${programaId}/metodologias-docentes`, {
    metodologia_docente_id: metodologiaDocenteId,
  });
}

/** Nombres de las Materia del Programa que usan la MetodologiaDocente -- [] = se
 * puede desasociar. */
export async function puedeDesasociarMetodologiaDocentePrograma(
  programaId: number,
  metodologiaDocenteId: number,
): Promise<string[]> {
  return get<string[]>(
    `/api/v1/programas/${programaId}/metodologias-docentes/${metodologiaDocenteId}/puede-desasociarse`,
  );
}

export async function desasociarMetodologiaDocentePrograma(
  programaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return del(`/api/v1/programas/${programaId}/metodologias-docentes/${metodologiaDocenteId}`);
}

export async function listarResultadosAprendizajeDisponiblesAsignaturaPrograma(
  asignaturaProgramaId: number,
): Promise<ResultadoAprendizajeResponse[]> {
  return get<ResultadoAprendizajeResponse[]>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje/disponibles`,
  );
}

export async function asociarResultadoAprendizajeAsignaturaPrograma(
  asignaturaProgramaId: number,
  resultadoAprendizajeId: number,
): Promise<void> {
  return post<void>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje`,
    { resultado_aprendizaje_id: resultadoAprendizajeId },
  );
}

export async function quedariaSinResultadosTrasDesasociar(
  asignaturaProgramaId: number,
  resultadoAprendizajeId: number,
): Promise<boolean> {
  return get<boolean>(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje/` +
      `${resultadoAprendizajeId}/quedaria-sin-resultados`,
  );
}

export async function desasociarResultadoAprendizajeAsignaturaPrograma(
  asignaturaProgramaId: number,
  resultadoAprendizajeId: number,
): Promise<void> {
  return del(
    `/api/v1/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje/` +
      `${resultadoAprendizajeId}`,
  );
}

export interface UniversidadResponse {
  id: number;
  nombre: string;
  // Issue #487: real solo en listarUniversidades().
  num_facultades: number;
}

export interface FacultadResponse {
  id: number;
  nombre: string;
  universidad_id: number;
  // Issue #487: real solo en listarFacultades().
  num_programas: number;
}

export async function listarUniversidades(): Promise<UniversidadResponse[]> {
  return get<UniversidadResponse[]>("/api/v1/universidades");
}

export async function obtenerUniversidad(universidadId: number): Promise<UniversidadResponse> {
  return get<UniversidadResponse>(`/api/v1/universidades/${universidadId}`);
}

export async function listarFacultades(universidadId: number): Promise<FacultadResponse[]> {
  return get<FacultadResponse[]>(`/api/v1/universidades/${universidadId}/facultades`);
}

export async function crearUniversidad(datos: { nombre: string }): Promise<UniversidadResponse> {
  return post<UniversidadResponse>("/api/v1/universidades", datos);
}

export async function crearFacultadDeUniversidad(
  universidadId: number,
  datos: { nombre: string },
): Promise<FacultadResponse> {
  return post<FacultadResponse>(`/api/v1/universidades/${universidadId}/facultades`, datos);
}

export async function obtenerFacultad(facultadId: number): Promise<FacultadResponse> {
  return get<FacultadResponse>(`/api/v1/facultades/${facultadId}`);
}

// Issue #488: fila plana por AsignaturaPrograma instanciada de este Asignatura
// del catálogo, mismo estilo que AsignaturaImpartidaResponse (Profesor).
export interface AsignaturaProgramaInstanciaResponse {
  asignatura_programa_id: number;
  programa_id: number;
  programa_nombre: string;
  materia_nombre: string;
  curso: number;
  semestre_default: number;
  caracter: string;
}

export interface AsignaturaResponse {
  id: number;
  codigo: string | null;
  nombre: string;
  ects: number | null;
  contenido: string;
  estado: string;
  // Issue #488: real solo en obtenerAsignaturaCatalogo().
  presente_en: AsignaturaProgramaInstanciaResponse[];
}

export async function listarAsignaturasCatalogo(): Promise<AsignaturaResponse[]> {
  return get<AsignaturaResponse[]>("/api/v1/asignaturas");
}

export async function obtenerAsignaturaCatalogo(asignaturaId: number): Promise<AsignaturaResponse> {
  return get<AsignaturaResponse>(`/api/v1/asignaturas/${asignaturaId}`);
}

export interface AsignaturaCreateCatalogo {
  codigo: string;
  nombre: string;
}

export interface AsignaturaUpdateCatalogo {
  nombre: string;
  ects: number;
  contenido: string;
}

export async function crearAsignaturaCatalogo(
  datos: AsignaturaCreateCatalogo,
): Promise<AsignaturaResponse> {
  return post<AsignaturaResponse>("/api/v1/asignaturas", datos);
}

export async function editarAsignaturaCatalogo(
  asignaturaId: number,
  datos: AsignaturaUpdateCatalogo,
): Promise<AsignaturaResponse> {
  return put<AsignaturaResponse>(`/api/v1/asignaturas/${asignaturaId}`, datos);
}

export async function eliminarAsignaturaCatalogo(asignaturaId: number): Promise<AsignaturaResponse> {
  // 200 con el objeto actualizado (estado: "Extinguido"), no 204 -- el
  // recurso sigue existiendo tras el borrado lógico
  return enviar<AsignaturaResponse>("DELETE", `/api/v1/asignaturas/${asignaturaId}`);
}

// --- MetodologiaDocente (catálogo Admin plano: auth require_admin) -----------
// MetodologiaDocenteResponse ya existe arriba (usado por las asociaciones de
// Materia/AsignaturaPrograma); este es el CRUD propio del catálogo. No confundir
// con listarMetodologiasDocentesDisponiblesMateria()/...AsignaturaPrograma(),
// que filtran por disponibilidad de asociación -- otro propósito.

export interface MetodologiaDocenteCreate {
  codigo: string;
  descripcion: string;
}

export interface MetodologiaDocenteUpdate {
  codigo: string;
  descripcion: string;
}

// Issue #655: listar/crear van anidados bajo la Universidad (backend); la pantalla
// se queda en ruta plana con selector -- anidar es cosa del backend.
export async function listarMetodologiasDocentes(
  universidadId: number,
): Promise<MetodologiaDocenteResponse[]> {
  return get<MetodologiaDocenteResponse[]>(
    `/api/v1/universidades/${universidadId}/metodologias-docentes`,
  );
}

export async function obtenerMetodologiaDocente(
  metodologiaDocenteId: number,
): Promise<MetodologiaDocenteResponse> {
  return get<MetodologiaDocenteResponse>(`/api/v1/metodologias-docentes/${metodologiaDocenteId}`);
}

export async function crearMetodologiaDocente(
  universidadId: number,
  datos: MetodologiaDocenteCreate,
): Promise<MetodologiaDocenteResponse> {
  return post<MetodologiaDocenteResponse>(
    `/api/v1/universidades/${universidadId}/metodologias-docentes`,
    datos,
  );
}

export async function editarMetodologiaDocente(
  metodologiaDocenteId: number,
  datos: MetodologiaDocenteUpdate,
): Promise<MetodologiaDocenteResponse> {
  return put<MetodologiaDocenteResponse>(
    `/api/v1/metodologias-docentes/${metodologiaDocenteId}`,
    datos,
  );
}

export async function eliminarMetodologiaDocente(metodologiaDocenteId: number): Promise<void> {
  // 204 si elimina de verdad; 409 (con el detail de las materias asociadas)
  // llega como ApiError -- mismo patrón que el resto de funciones delete
  return del(`/api/v1/metodologias-docentes/${metodologiaDocenteId}`);
}

// --- ActividadFormativa (catálogo Admin por Universidad, issue #655: auth require_admin) ---
// Mismo patrón que MetodologiaDocente: listar/crear anidados bajo la Universidad,
// item por id plano.

export interface ActividadFormativaResponse {
  id: number;
  universidad_id: number;
  codigo: string;
  nombre: string;
}

export interface ActividadFormativaCreate {
  codigo: string;
  nombre: string;
}

export interface ActividadFormativaUpdate {
  codigo: string;
  nombre: string;
}

export async function listarActividadesFormativas(
  universidadId: number,
): Promise<ActividadFormativaResponse[]> {
  return get<ActividadFormativaResponse[]>(
    `/api/v1/universidades/${universidadId}/actividades-formativas`,
  );
}

export async function obtenerActividadFormativa(
  actividadFormativaId: number,
): Promise<ActividadFormativaResponse> {
  return get<ActividadFormativaResponse>(`/api/v1/actividades-formativas/${actividadFormativaId}`);
}

export async function crearActividadFormativa(
  universidadId: number,
  datos: ActividadFormativaCreate,
): Promise<ActividadFormativaResponse> {
  return post<ActividadFormativaResponse>(
    `/api/v1/universidades/${universidadId}/actividades-formativas`,
    datos,
  );
}

export async function editarActividadFormativa(
  actividadFormativaId: number,
  datos: ActividadFormativaUpdate,
): Promise<ActividadFormativaResponse> {
  return put<ActividadFormativaResponse>(
    `/api/v1/actividades-formativas/${actividadFormativaId}`,
    datos,
  );
}

export async function eliminarActividadFormativa(actividadFormativaId: number): Promise<void> {
  // 204 si elimina de verdad; 409 (con el detail de las materias donde está en uso)
  // llega como ApiError
  return del(`/api/v1/actividades-formativas/${actividadFormativaId}`);
}

// --- Programa (variante Admin, anidado bajo Facultad: auth require_admin) -------
// ProgramaResponse ya existe arriba (variante DirectorPrograma de /api/v1/programas);
// la forma del objeto es la misma, solo cambia el namespace de autorización.

export interface ProgramaAdminCreate {
  codigo: string;
  nombre: string;
}

export interface ProgramaAdminUpdate {
  nombre: string;
}

export async function listarProgramasDeFacultad(
  facultadId: number,
): Promise<ProgramaResponse[]> {
  return get<ProgramaResponse[]>(`/api/v1/admin/facultades/${facultadId}/programas`);
}

export async function obtenerProgramaAdmin(programaId: number): Promise<ProgramaResponse> {
  return get<ProgramaResponse>(`/api/v1/admin/programas/${programaId}`);
}

export async function crearProgramaDeFacultad(
  facultadId: number,
  datos: ProgramaAdminCreate,
): Promise<ProgramaResponse> {
  return post<ProgramaResponse>(`/api/v1/admin/facultades/${facultadId}/programas`, datos);
}

export async function editarProgramaAdmin(
  programaId: number,
  datos: ProgramaAdminUpdate,
): Promise<ProgramaResponse> {
  return put<ProgramaResponse>(`/api/v1/admin/programas/${programaId}`, datos);
}

export async function eliminarProgramaAdmin(programaId: number): Promise<ProgramaResponse> {
  // 200 con el objeto actualizado (estado: "Extinguido"), no 204 -- el
  // recurso sigue existiendo tras el borrado lógico
  return enviar<ProgramaResponse>("DELETE", `/api/v1/admin/programas/${programaId}`);
}

// Issue #492: reverso exacto de listarProgramasDisponiblesParaDirigir() (más
// abajo, variante Profesor) -- Profesores que todavía NO dirigen este
// Programa. Profesor ya existe arriba (variante DirectorPrograma de
// /api/v1/profesores); la forma del objeto es la misma.
export async function listarProfesoresDisponiblesParaDirigirPrograma(
  programaId: number,
): Promise<Profesor[]> {
  return get<Profesor[]>(
    `/api/v1/admin/programas/${programaId}/profesores-disponibles-para-dirigir`,
  );
}

// --- Materia (variante Admin, anidada bajo Programa: auth require_admin) --------
// MateriaResponse ya existe arriba (variante DirectorPrograma de
// /api/v1/programas/{programa_id}/materias); la forma del objeto es la misma,
// solo cambia el namespace de autorización.

export interface MateriaAdminDetalleResponse extends MateriaResponse {
  // las mismas colecciones que MateriaDetalleResponse, en solo lectura (Admin
  // ve, no gestiona: eso es de DirectorPrograma), más sistemas_evaluacion, entidad
  // propia de la Materia que MateriaDetalleResponse nunca expuso aquí
  metodologias_docentes: MetodologiaMateriaResponse[];
  resultados_aprendizaje: ResultadoAprendizajeResponse[];
  asignaturas_programa: AsignaturaProgramaResponse[];
  sistemas_evaluacion: SistemaEvaluacionResponse[];
  actividades_formativas: ActividadFormativaMateriaResponse[];
}

export interface MateriaAdminCreate {
  nombre: string;
}

export interface MateriaAdminUpdate {
  nombre: string;
}

export async function listarMateriasDeProgramaAdmin(
  programaId: number,
): Promise<MateriaResponse[]> {
  return get<MateriaResponse[]>(`/api/v1/admin/programas/${programaId}/materias`);
}

export async function crearMateriaAdmin(
  programaId: number,
  datos: MateriaAdminCreate,
): Promise<MateriaResponse> {
  return post<MateriaResponse>(`/api/v1/admin/programas/${programaId}/materias`, datos);
}

export async function obtenerMateriaAdmin(
  materiaId: number,
): Promise<MateriaAdminDetalleResponse> {
  return get<MateriaAdminDetalleResponse>(`/api/v1/admin/materias/${materiaId}`);
}

export async function editarMateriaAdmin(
  materiaId: number,
  datos: MateriaAdminUpdate,
): Promise<MateriaResponse> {
  return put<MateriaResponse>(`/api/v1/admin/materias/${materiaId}`, datos);
}

// --- AsignaturaPrograma (variante Admin, tabla embebida de abrirPrograma()) --------

export interface AsignaturaProgramaAdminCreate {
  materia_id: number;
  asignatura_id: number;
  curso: number;
  caracter: string;
  idioma: string;
  semestre_default: number;
  nombre?: string;
  ects?: number;
  contenido?: string;
  sesiones_minimas?: number;
}

export async function listarAsignaturasProgramaDeProgramaAdmin(
  programaId: number,
): Promise<AsignaturaProgramaResponse[]> {
  return get<AsignaturaProgramaResponse[]>(
    `/api/v1/admin/programas/${programaId}/asignaturas-programa`,
  );
}

export async function crearAsignaturaProgramaAdmin(
  programaId: number,
  datos: AsignaturaProgramaAdminCreate,
): Promise<AsignaturaProgramaResponse> {
  return post<AsignaturaProgramaResponse>(
    `/api/v1/admin/programas/${programaId}/asignaturas-programa`,
    datos,
  );
}

export async function eliminarAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
): Promise<AsignaturaProgramaResponse> {
  // 200 con el objeto actualizado (estado: "Extinguido"), no 204 -- el
  // recurso sigue existiendo tras el borrado lógico; la respuesta lleva el
  // programa_id que la pantalla de confirmación necesita para volver
  return enviar<AsignaturaProgramaResponse>(
    "DELETE",
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}`,
  );
}

// --- Profesor (catálogo Admin top-level: auth require_admin) -----------------
// Profesor ya existe arriba (usado por AsignaturaPrograma.profesorado y las
// GuiaResumenResponse); este es el CRUD propio del catálogo, más las dos
// acciones sobre el rol de DirectorPrograma (definir/quitar) y el selector de
// Programas disponibles para dirigir.

export interface ProgramaDirigido {
  id: number;
  codigo: string;
  nombre: string;
}

export interface AsignaturaImpartida {
  id: number;
  nombre: string;
  programa_codigo: string;
  programa_nombre: string;
}

export interface ProfesorDetalleResponse extends Profesor {
  programas: ProgramaDirigido[];
  asignaturas: AsignaturaImpartida[];
  // issue #436: ya no son campos planos -- es la fila de PerfilProfesorCurso
  // del CursoAcademico activo, o null si el Profesor nunca la rellenó.
  perfil_curso_activo: PerfilProfesorCurso | null;
}

export interface ProfesorCreate {
  nombre: string;
  email: string;
  universidad_id: number;
}

export type ProfesorUpdate = ProfesorCreate;

export async function listarProfesores(): Promise<Profesor[]> {
  return get<Profesor[]>("/api/v1/profesores");
}

export async function obtenerProfesor(profesorId: number): Promise<ProfesorDetalleResponse> {
  return get<ProfesorDetalleResponse>(`/api/v1/profesores/${profesorId}`);
}

export async function crearProfesor(datos: ProfesorCreate): Promise<Profesor> {
  return post<Profesor>("/api/v1/profesores", datos);
}

export async function editarProfesor(
  profesorId: number,
  datos: ProfesorUpdate,
): Promise<Profesor> {
  return put<Profesor>(`/api/v1/profesores/${profesorId}`, datos);
}

export async function eliminarProfesor(profesorId: number): Promise<void> {
  // 204 si elimina de verdad; 409 (con los motivos de bloqueo en el detail)
  // llega como ApiError -- mismo patrón que el resto de funciones delete
  return del(`/api/v1/profesores/${profesorId}`);
}

// --- Mi perfil (autoservicio, issue #423) ---------------------------------

// Escala SIIU 0-5 (issue #429) -- sustituye a FiguraAcreditacion. `null`
// sigue significando "no informado todavía", `0` es una respuesta explícita
// ("sin acreditación") -- nunca comprobar con `? :` (0 es falsy en JS/TS),
// siempre `!= null` / `=== null` explícito.
export type NivelAcreditacionSiiu = 0 | 1 | 2 | 3 | 4 | 5;

export type OrganismoAcreditador = "ANECA" | "OTRO";

// Campos del perfil académico compartidos entre MiPerfil (autoservicio) y
// PerfilProfesorCurso (vista de Admin, issue #436) -- misma forma, la
// diferencia es el contexto (id/curso_academico_id/validado vs. id/email
// propios del Profesor + el gate de sugerencia).
interface CamposPerfilAcademico {
  orcid: string | null;
  // Enlace al CVN público (FECYT), issue #462 -- validado en servidor
  // (dominio *.fecyt.es, "cvnOnline" en la ruta).
  enlace_cvn: string | null;
  // Enlace a una foto ya alojada en otro sitio (issue #466) -- sin subida
  // de archivo, solo exige https:// en servidor.
  enlace_foto: string | null;
  // Enlace al perfil público de Google Scholar (issue #468) -- validado en
  // servidor (dominio scholar.google.<tld>, con "user=" en la query).
  enlace_scholar: string | null;
  es_doctor: boolean;
  universidad_doctorado: string | null;
  anio_doctorado: number | null;
  programa_doctorado: string | null;
  mencion_internacional: boolean;
  nivel_acreditacion_siiu: NivelAcreditacionSiiu | null;
  organismo_acreditador: OrganismoAcreditador | null;
  organismo_acreditador_otro: string | null;
  num_sexenios: number;
  anio_ultimo_sexenio: number | null;
  tramitando_sexenio: boolean;
  num_quinquenios: number;
  anio_ultimo_quinquenio: number | null;
  biografia: string | null;
  // Petición de Calidad (issue #436) -- acumulados a fecha, no
  // incrementales. Fuera del formulario hasta que pySigHor lo pidió tras
  // revisión: sin estos campos el gate no captura lo único nuevo que
  // Calidad quería.
  anios_experiencia_docente: number | null;
  anios_experiencia_docente_virtual: number | null;
  anios_experiencia_profesional: number | null;
  anios_experiencia_investigadora: number | null;
}

export interface MiPerfil extends CamposPerfilAcademico {
  id: number;
  nombre: string | null;
  email: string;
  // Gate de validación por curso (issue #436). `validado` refleja siempre
  // el curso ACTIVO -- si `sugerido_de_curso_anterior` es true, los datos
  // mostrados son de un curso anterior y `validado` viene forzado a false
  // pese a que esa fila sí estuviera validada en su momento.
  validado: boolean;
  sugerido_de_curso_anterior: boolean;
}

export type MiPerfilUpdate = Omit<
  MiPerfil,
  "id" | "email" | "validado" | "sugerido_de_curso_anterior"
>;

// Vista de Admin (routers/profesor.py::_detalle(), issue #436): el perfil
// académico del curso activo de un Profesor, o null si nunca lo rellenó
// para ese curso. Sin sugerido_de_curso_anterior -- el Admin ve
// exactamente lo que hay para el curso activo.
export interface PerfilProfesorCurso extends CamposPerfilAcademico {
  id: number;
  curso_academico_id: number;
  validado: boolean;
}

export async function obtenerMiPerfil(): Promise<MiPerfil> {
  return get<MiPerfil>("/api/v1/mi-perfil");
}

export async function editarMiPerfil(datos: MiPerfilUpdate): Promise<MiPerfil> {
  return put<MiPerfil>("/api/v1/mi-perfil", datos);
}

export async function listarProgramasDisponiblesParaDirigir(
  profesorId: number,
): Promise<ProgramaResponse[]> {
  return get<ProgramaResponse[]>(
    `/api/v1/profesores/${profesorId}/programas-disponibles-para-dirigir`,
  );
}

export async function definirDirectorPrograma(
  profesorId: number,
  programaId: number,
): Promise<ProfesorDetalleResponse> {
  // 200 con el Profesor actualizado (incluye la lista de Programas que dirige);
  // idempotente -- si ya lo dirigía, no duplica ni da error
  return post<ProfesorDetalleResponse>(
    `/api/v1/profesores/${profesorId}/directores-programa`,
    { programa_id: programaId },
  );
}

export async function quitarDirectorPrograma(
  profesorId: number,
  programaId: number,
): Promise<void> {
  // 204 si quita de verdad; 409 si es el único DirectorPrograma del Programa
  // (llega como ApiError con el detail)
  return del(`/api/v1/profesores/${profesorId}/directores-programa/${programaId}`);
}

// --- AsignaturaPrograma: profesorado (variante Admin: require_admin) -----------
// AsignaturaProgramaDetalleResponse ya existe arriba (variante DirectorPrograma de
// /api/v1/asignaturas-programa/{id}); la forma es la misma, solo cambia el
// namespace de autorización -- mismo patrón que Programa/Materia Admin.

export async function obtenerAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
): Promise<AsignaturaProgramaDetalleResponse> {
  return get<AsignaturaProgramaDetalleResponse>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}`,
  );
}

export async function listarProfesoresDisponiblesParaAsignaturaPrograma(
  asignaturaProgramaId: number,
): Promise<Profesor[]> {
  return get<Profesor[]>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/profesores-disponibles`,
  );
}

export async function asignarProfesorAAsignaturaPrograma(
  asignaturaProgramaId: number,
  profesorId: number,
): Promise<void> {
  return post<void>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/profesorado`,
    { profesor_id: profesorId },
  );
}

export async function desasignarProfesorDeAsignaturaPrograma(
  asignaturaProgramaId: number,
  profesorId: number,
): Promise<void> {
  // Sin bloqueo (discussion #33) -- siempre 204, incluso si es el único
  // profesor; la advertencia se calcula en el cliente antes de confirmar
  return del(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/profesorado/${profesorId}`,
  );
}

// --- AsignaturaPrograma: RA, Metodologías y Actividades formativas (variante Admin) ---
// issue #599: espejo de las funciones de Director, apuntando a /api/v1/admin/...

export async function listarResultadosAprendizajeDisponiblesAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
): Promise<ResultadoAprendizajeResponse[]> {
  return get<ResultadoAprendizajeResponse[]>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje/disponibles`,
  );
}

export async function asociarResultadoAprendizajeAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
  resultadoAprendizajeId: number,
): Promise<void> {
  return post<void>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje`,
    { resultado_aprendizaje_id: resultadoAprendizajeId },
  );
}

export async function quedariaSinResultadosTrasDesasociarAdmin(
  asignaturaProgramaId: number,
  resultadoAprendizajeId: number,
): Promise<boolean> {
  return get<boolean>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje/` +
      `${resultadoAprendizajeId}/quedaria-sin-resultados`,
  );
}

export async function desasociarResultadoAprendizajeAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
  resultadoAprendizajeId: number,
): Promise<void> {
  return del(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/resultados-aprendizaje/` +
      `${resultadoAprendizajeId}`,
  );
}

export async function listarMetodologiasDocentesDisponiblesAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
): Promise<MetodologiaDocenteResponse[]> {
  return get<MetodologiaDocenteResponse[]>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes/disponibles`,
  );
}

export async function asociarMetodologiaDocenteAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return post<void>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes`,
    { metodologia_docente_id: metodologiaDocenteId },
  );
}

export async function quedariaSinMetodologiasTrasDesasociarAdmin(
  asignaturaProgramaId: number,
  metodologiaDocenteId: number,
): Promise<boolean> {
  return get<boolean>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes/` +
      `${metodologiaDocenteId}/quedaria-sin-metodologias`,
  );
}

export async function desasociarMetodologiaDocenteAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
  metodologiaDocenteId: number,
): Promise<void> {
  return del(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/metodologias-docentes/${metodologiaDocenteId}`,
  );
}

export async function obtenerActividadesFormativasAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
): Promise<ActividadFormativaAsignaturaProgramaResponse[]> {
  return get<ActividadFormativaAsignaturaProgramaResponse[]>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/actividades-formativas`,
  );
}

export async function editarActividadesFormativasAsignaturaProgramaAdmin(
  asignaturaProgramaId: number,
  actividades: ActividadFormativaAsignaturaProgramaItem[],
): Promise<ActividadFormativaAsignaturaProgramaResponse[]> {
  return put<ActividadFormativaAsignaturaProgramaResponse[]>(
    `/api/v1/admin/asignaturas-programa/${asignaturaProgramaId}/actividades-formativas`,
    { actividades },
  );
}

export interface CopiaSeguridadResponse {
  timestamp: string;
  familia: string;
  archivo: string;
  tamano_bytes: number;
  motivo: string | null;
  esquema_version: number | null;
  disponible: boolean;
}

export async function consultarCopiasSeguridad(): Promise<CopiaSeguridadResponse[]> {
  return get<CopiaSeguridadResponse[]>("/api/v1/copias-seguridad");
}

export async function crearCopiaSeguridad(
  motivo: string | null,
): Promise<CopiaSeguridadResponse> {
  return post<CopiaSeguridadResponse>("/api/v1/copias-seguridad", { motivo });
}

export interface SaludCopiaSeguridadResponse {
  archivo: string;
  salud: "ok" | "danada" | "ilegible" | "no_disponible";
  detalle: string | null;
}

export async function comprobarCopiasSeguridad(): Promise<SaludCopiaSeguridadResponse[]> {
  return post<SaludCopiaSeguridadResponse[]>("/api/v1/copias-seguridad/comprobar", {});
}

export interface RestaurarCopiaSeguridadResponse {
  detalle: string;
}

export async function restaurarCopiaSeguridad(
  archivo: string,
): Promise<RestaurarCopiaSeguridadResponse> {
  return post<RestaurarCopiaSeguridadResponse>("/api/v1/copias-seguridad/restaurar", { archivo });
}

export interface VersionResponse {
  esquema_version: number;
}

export async function obtenerVersion(): Promise<VersionResponse> {
  return get<VersionResponse>("/api/v1/version");
}

export interface AutorHistorialResponse {
  tipo: string; // "profesor" | "director_programa" | "admin"
  id: number;
  nombre: string;
}

export interface HistorialCambioResponse {
  id: number;
  fecha: string;
  guia_id: number;
  asignatura_programa_nombre: string | null;
  programa_id: number | null;
  programa_codigo: string | null;
  campo: string;
  valor_anterior: string;
  valor_nuevo: string;
  comentario: string | null;
  autor: AutorHistorialResponse;
}

export interface AutorIndiceResponse {
  clave: string; // email normalizado, o "admin"
  nombre: string;
}

export interface HistorialCambiosResponse {
  ultimos: HistorialCambioResponse[];
  autores: AutorIndiceResponse[];
}

export async function consultarHistorialCambios(
  // issue #442: sin indicar, histórico completo de todos los cursos
  // (default opuesto al de #441/consultarEstadoGuias).
  cursoAcademicoId?: number,
): Promise<HistorialCambiosResponse> {
  const query = cursoAcademicoId != null ? `?curso=${cursoAcademicoId}` : "";
  return get<HistorialCambiosResponse>(`/api/v1/historial-cambios${query}`);
}

export async function consultarHistorialCambiosDeAutor(
  clave: string,
): Promise<HistorialCambioResponse[]> {
  return get<HistorialCambioResponse[]>(`/api/v1/historial-cambios/autores/${clave}`);
}

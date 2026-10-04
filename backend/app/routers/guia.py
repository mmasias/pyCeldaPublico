from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.auth import (
    get_current_admin_email_opcional,
    get_current_director_programa_id,
    get_current_director_programa_id_opcional,
    get_current_profesor_id,
    get_current_profesor_id_opcional,
    get_current_rol,
)
from app.core.database import get_db
from app.models.guia import LIMITE_CONTENIDO_GUIA, MARCADOR_TABLA, Guia
from app.models.historial_cambio import HistorialCambio
from app.render.guia_docente import render_html, render_pdf
from app.repositories.actividad_formativa import (
    serializar_actividades_formativas_asignatura_programa,
)
from app.repositories.asignatura_programa import AsignaturaProgramaRepository
from app.repositories.curso_academico import CursoAcademicoRepository
from app.repositories.programa import ProgramaRepository
from app.repositories.guia import GuiaRepository
from app.repositories.ponderacion_evaluacion import PonderacionEvaluacionRepository
from app.repositories.referencia_bibliografica import ReferenciaBibliograficaRepository
from app.repositories.sesion import SesionRepository
from app.schemas.guia import (
    AbrirGuiaResponse,
    AsignaturaProgramaDeGuiaResponse,
    EditarSemestreGuiaRequest,
    EditarTextoSistemaEvaluacionRequest,
    GuardarBorradorRequest,
    GuiaResponse,
    GuiaResumenResponse,
    NotificacionResponse,
    RechazarGuiaRequest,
    ResumenCompletitudResponse,
    RevocarAprobacionGuiaRequest,
)

router = APIRouter(prefix="/api/v1", tags=["guias"])

# 10000 -> "10.000" para el mensaje de rechazo (issue #303).
_LIMITE_CONTENIDO_GUIA_TXT = f"{LIMITE_CONTENIDO_GUIA:,}".replace(",", ".")


def _resumen_contenido(texto: str) -> str:
    """El temario es texto largo; HistorialCambio.valor_* es corto (String(50)).
    Se guarda un resumen legible con los espacios colapsados -- el detalle del
    cambio no vive en la auditoría, vive en Guia.contenido."""
    plano = " ".join(texto.split())
    if len(plano) <= 50:
        return plano
    return plano[:47] + "..."


def _es_director_de_la_guia(
    db: Session, guia, director_programa_id: int | None
) -> bool:
    """Rama de DirectorPrograma del acceso: el usuario resuelve a un
    DirectorPrograma que dirige el programa de la Guia."""
    return (
        director_programa_id is not None
        and guia.programa_id is not None
        and ProgramaRepository(db).dirige(guia.programa_id, director_programa_id)
    )


def _tiene_acceso_a_guia(
    db: Session, guia, profesor_id: int | None, director_programa_id: int | None
) -> bool:
    """Un email puede resolver a Profesor y/o DirectorPrograma a la vez
    (roles no exclusivos, ver get_current_rol) -- se concede acceso si
    cualquiera de las dos identidades reales tiene relación con la Guia."""
    if (
        profesor_id is not None
        and guia.asignatura_programa_id is not None
        and AsignaturaProgramaRepository(db).imparte(
            guia.asignatura_programa_id, profesor_id
        )
    ):
        return True

    if _es_director_de_la_guia(db, guia, director_programa_id):
        return True

    return False


def autorizar_escritura_guia(
    db: Session,
    guia,
    profesor_id: int | None,
    director_programa_id: int | None,
    detalle: str = "Guia no encontrada",
) -> bool:
    """Autorización de escritura sobre el contenido de una Guia (issue #612,
    Parte 2 de #601). Devuelve True si quien escribe lo hace como
    DirectorPrograma (corrección excepcional), False si lo hace como Profesor.
    Lanza 404 si ninguna de las dos identidades tiene derecho.

    Si el email resuelve a ambos roles y el Profesor imparte la asignatura,
    gana la rama Profesor (comportamiento previo, sin transición de estado):
    criterio conservador."""
    if (
        profesor_id is not None
        and guia.asignatura_programa_id is not None
        and AsignaturaProgramaRepository(db).imparte(
            guia.asignatura_programa_id, profesor_id
        )
    ):
        return False
    if _es_director_de_la_guia(db, guia, director_programa_id):
        return True
    raise HTTPException(status_code=404, detail=detalle)


def aplicar_transicion_por_correccion_del_director(
    db: Session, guia, director_programa_id: int
) -> None:
    """Regla de transición de estado de #612: Aprobada -> Borrador
    (revocar_aprobacion) y EnRevision -> Rechazada (rechazar), con fila de
    HistorialCambio campo="estado" y autor real del Director. Borrador y
    Rechazada se mantienen. NO hace commit: se invoca justo antes de la
    escritura del contenido, que commitea ambas cosas en una transacción."""
    estado_anterior = guia.estado
    if estado_anterior == "Aprobada":
        guia.revocar_aprobacion()
    elif estado_anterior == "EnRevision":
        guia.rechazar()
    else:
        return
    db.add(
        HistorialCambio.registrar(
            guia_id=guia.id,
            autor_id=director_programa_id,
            campo="estado",
            valor_anterior=estado_anterior,
            valor_nuevo=guia.estado,
            comentario="corrección directa del Director",
        )
    )


@router.get("/guias/{guia_id}", response_model=AbrirGuiaResponse)
def abrir_guia(
    guia_id: int,
    db: Session = Depends(get_db),
    # Profesor (autor) y DirectorPrograma (revisor, Lote C) comparten esta
    # pantalla -- get_current_rol acepta cualquiera de los dos roles.
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> AbrirGuiaResponse:
    guia_repo = GuiaRepository(db)
    ponderacion_repo = PonderacionEvaluacionRepository(db)
    referencia_repo = ReferenciaBibliograficaRepository(db)
    sesion_repo = SesionRepository(db)

    guia = guia_repo.obtener(guia_id)
    if guia is None or not _tiene_acceso_a_guia(
        db, guia, profesor_id, director_programa_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    ponderaciones = ponderacion_repo.listar_vinculadas_de(
        guia
    ) + ponderacion_repo.listar_pendientes_de(guia_id)
    referencias = referencia_repo.listar_vinculadas_de(
        guia
    ) + referencia_repo.listar_pendientes_de(guia_id)
    sesiones = sesion_repo.listar_vinculadas_de(
        guia
    ) + sesion_repo.listar_pendientes_de(guia_id)

    asignatura_programa = (
        AsignaturaProgramaDeGuiaResponse(
            nombre=guia.asignatura_programa.nombre,
            programa_nombre=guia.asignatura_programa.programa_nombre,
            contenido=guia.asignatura_programa.contenido,
            resultados_aprendizaje=guia.asignatura_programa.resultados_aprendizaje,
            metodologias_docentes=guia.asignatura_programa.metodologias_docentes,
            # Solo lectura -- discussion #227. Ya viene precargado por
            # GuiaRepository.obtener() (lo necesita el render), sin consulta
            # nueva; codigo/nombre se aplanan a mano porque viven en la
            # ActividadFormativa anidada, no en la propia fila de asociación.
            actividades_formativas=serializar_actividades_formativas_asignatura_programa(
                guia.asignatura_programa.actividades_formativas
            ),
        )
        if guia.asignatura_programa is not None
        else None
    )

    bloqueo_ponderaciones = guia.bloqueo_ponderaciones()

    return AbrirGuiaResponse(
        id=guia.id,
        estado=guia.estado,
        semestre=guia.semestre,
        # El temario propio de la Guia (fase de impartición), NO
        # guia.asignatura_programa.contenido -- ese sigue siendo la referencia
        # estructural del DirectorPrograma (discussion #191).
        contenido=guia.contenido,
        texto_sistema_evaluacion=guia.texto_sistema_evaluacion,
        sesiones_minimas=guia.sesiones_minimas,
        fecha_creacion=guia.fecha_creacion,
        fecha_ultima_modificacion=guia.fecha_ultima_modificacion,
        fecha_generacion_pdf=guia.fecha_generacion_pdf,
        ponderaciones=ponderaciones,
        referencias=referencias,
        asignatura_programa=asignatura_programa,
        puede_revisar=_es_director_de_la_guia(db, guia, director_programa_id),
        # issue #254: el profesorado en vivo desde la plantilla, no la copia
        # guia.profesorado (esa solo la usa el render del PDF/previsualización).
        profesorado=(
            guia.asignatura_programa.profesorado
            if guia.asignatura_programa is not None
            else []
        ),
        sesiones=sesiones,
        comentario_revision_por_profesorado=guia.comentario_revision_por_profesorado,
        # issue #504: mismos métodos que el gate real de enviar_guia_a_revision
        # (líneas 289-309 más abajo) -- no reimplementa la lógica de negocio.
        resumen_completitud=ResumenCompletitudResponse(
            sin_pendientes=not (
                ponderacion_repo.existe_pendiente_de(guia_id)
                or referencia_repo.existe_pendiente_de(guia_id)
                or sesion_repo.existe_pendiente_de(guia_id)
            ),
            ponderaciones_ok=bloqueo_ponderaciones is None,
            motivo_ponderaciones=bloqueo_ponderaciones,
            planificacion_docente_ok=guia.planificacion_docente_completa(),
            sesiones_vinculadas=guia.sesiones_vinculadas_count(),
        ),
    )


@router.put("/guias/{guia_id}/borrador", response_model=GuiaResponse)
def guardar_borrador_guia(
    guia_id: int,
    datos: GuardarBorradorRequest,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    ponderacion_repo = PonderacionEvaluacionRepository(db)
    referencia_repo = ReferenciaBibliograficaRepository(db)
    sesion_repo = SesionRepository(db)

    guia = guia_repo.obtener(guia_id)
    if guia is None:
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    como_director = autorizar_escritura_guia(
        db, guia, profesor_id, director_programa_id
    )
    autor_id = director_programa_id if como_director else profesor_id

    # Tope de longitud del temario (issue #303): se comprueba antes de tocar
    # nada -- si el contenido pegado se pasa, la petición se rechaza entera,
    # sin vincular/desvincular ponderaciones ni sesiones.
    if datos.contenido is not None and not Guia.contenido_dentro_del_limite(
        datos.contenido
    ):
        raise HTTPException(
            status_code=422,
            detail=(
                f"El contenido supera el límite de {_LIMITE_CONTENIDO_GUIA_TXT} "
                "caracteres"
            ),
        )

    if como_director:
        aplicar_transicion_por_correccion_del_director(db, guia, director_programa_id)

    a_vincular, a_desvincular = guia.sincronizar_ponderaciones(
        datos.ids_ponderaciones_final
    )
    if a_vincular or a_desvincular:
        antes = len([p for p in guia.ponderaciones if p.vinculada])
        despues = antes + len(a_vincular) - len(a_desvincular)
        db.add(
            HistorialCambio.registrar(
                guia_id=guia.id,
                autor_id=autor_id,
                campo="ponderaciones_evaluacion",
                valor_anterior=f"{antes} ponderaciones",
                valor_nuevo=f"{despues} ponderaciones",
                comentario=f"{len(a_vincular)} añadida(s), {len(a_desvincular)} quitada(s)"[:200],
            )
        )
    for id_ in a_vincular:
        ponderacion_repo.vincular(id_, guia)
    for id_ in a_desvincular:
        ponderacion_repo.desvincular(id_)

    a_vincular, a_desvincular = guia.sincronizar_referencias(datos.ids_referencias_final)
    if a_vincular or a_desvincular:
        antes = len([r for r in guia.referencias if r.vinculada])
        despues = antes + len(a_vincular) - len(a_desvincular)
        db.add(
            HistorialCambio.registrar(
                guia_id=guia.id,
                autor_id=autor_id,
                campo="referencias_bibliograficas",
                valor_anterior=f"{antes} referencias",
                valor_nuevo=f"{despues} referencias",
                comentario=f"{len(a_vincular)} añadida(s), {len(a_desvincular)} quitada(s)"[:200],
            )
        )
    for id_ in a_vincular:
        referencia_repo.vincular(id_, guia)
    for id_ in a_desvincular:
        referencia_repo.desvincular(id_)

    a_vincular, a_desvincular = guia.sincronizar_sesiones(datos.ids_sesiones_final)
    for id_ in a_vincular:
        sesion_repo.vincular(id_, guia)
    for id_ in a_desvincular:
        sesion_repo.desvincular(id_)

    if datos.contenido is not None:
        contenido_anterior = guia.actualizar_contenido(datos.contenido)
        if contenido_anterior is not None:
            # Fila de HistorialCambio con campo="contenido": es una edición del
            # Profesor. Guia._ultimo_cambio_historial() ignora estas filas (solo
            # mira campo="estado") para no atribuir el cambio al Director.
            db.add(
                HistorialCambio.registrar(
                    guia_id=guia.id,
                    autor_id=autor_id,
                    campo="contenido",
                    valor_anterior=_resumen_contenido(contenido_anterior),
                    valor_nuevo=_resumen_contenido(datos.contenido),
                    comentario="temario editado",
                )
            )

    guia.confirmar_guardado()
    return guia_repo.actualizar(guia)


@router.post("/guias/{guia_id}/enviar-a-revision", response_model=GuiaResponse)
def enviar_guia_a_revision(
    guia_id: int,
    db: Session = Depends(get_db),
    profesor_id: int = Depends(get_current_profesor_id),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    ponderacion_repo = PonderacionEvaluacionRepository(db)
    referencia_repo = ReferenciaBibliograficaRepository(db)
    sesion_repo = SesionRepository(db)

    guia = guia_repo.obtener(guia_id)
    if guia is None:
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    asignatura_repo = AsignaturaProgramaRepository(db)
    if guia.asignatura_programa_id is None or not asignatura_repo.imparte(
        guia.asignatura_programa_id, profesor_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    if (
        ponderacion_repo.existe_pendiente_de(guia_id)
        or referencia_repo.existe_pendiente_de(guia_id)
        or sesion_repo.existe_pendiente_de(guia_id)
    ):
        raise HTTPException(
            status_code=409, detail="Hay items sin guardar -- guarda el borrador primero"
        )

    bloqueo_ponderaciones = guia.bloqueo_ponderaciones()
    if bloqueo_ponderaciones is not None:
        raise HTTPException(status_code=422, detail=bloqueo_ponderaciones)

    if not guia.planificacion_docente_completa():
        raise HTTPException(
            status_code=422,
            detail=(
                "Planificación docente incompleta: "
                f"{guia.sesiones_vinculadas_count()} de {guia.sesiones_minimas} sesiones"
            ),
        )

    guia.enviar_a_revision()
    return guia_repo.actualizar(guia)


@router.post("/guias/{guia_id}/aprobar", response_model=GuiaResponse)
def aprobar_guia(
    guia_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None or guia.programa_id is None or not ProgramaRepository(db).dirige(
        guia.programa_id, director_programa_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    estado_anterior = guia.estado
    guia.aprobar()

    historial = HistorialCambio.registrar(
        guia_id=guia.id,
        autor_id=director_programa_id,
        campo="estado",
        valor_anterior=estado_anterior,
        valor_nuevo=guia.estado,
        comentario="aprobada sin incidencia",
    )
    db.add(historial)

    return guia_repo.actualizar(guia)


@router.post("/guias/{guia_id}/rechazar", response_model=GuiaResponse)
def rechazar_guia(
    guia_id: int,
    datos: RechazarGuiaRequest,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None or guia.programa_id is None or not ProgramaRepository(db).dirige(
        guia.programa_id, director_programa_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    estado_anterior = guia.estado
    guia.rechazar()

    historial = HistorialCambio.registrar(
        guia_id=guia.id,
        autor_id=director_programa_id,
        campo="estado",
        valor_anterior=estado_anterior,
        valor_nuevo=guia.estado,
        comentario=datos.comentario,
    )
    db.add(historial)

    return guia_repo.actualizar(guia)


@router.post("/guias/{guia_id}/escalar-a-aprobada", response_model=GuiaResponse)
def escalar_guia_a_aprobada(
    guia_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None or guia.programa_id is None or not ProgramaRepository(db).dirige(
        guia.programa_id, director_programa_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    estado_anterior = guia.escalar_a_aprobada()

    historial = HistorialCambio.registrar(
        guia_id=guia.id,
        autor_id=director_programa_id,
        campo="estado",
        valor_anterior=estado_anterior,
        valor_nuevo=guia.estado,
        comentario="escalada a aprobada sin incidencia",
    )
    db.add(historial)

    return guia_repo.actualizar(guia)


@router.post("/guias/{guia_id}/revocar-aprobacion", response_model=GuiaResponse)
def revocar_aprobacion_guia(
    guia_id: int,
    datos: RevocarAprobacionGuiaRequest,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None or guia.programa_id is None or not ProgramaRepository(db).dirige(
        guia.programa_id, director_programa_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    estado_anterior = guia.estado
    guia.revocar_aprobacion()

    historial = HistorialCambio.registrar(
        guia_id=guia.id,
        autor_id=director_programa_id,
        campo="estado",
        valor_anterior=estado_anterior,
        valor_nuevo=guia.estado,
        comentario=datos.comentario,
    )
    db.add(historial)

    return guia_repo.actualizar(guia)


@router.put("/guias/{guia_id}/semestre", response_model=GuiaResponse)
def editar_semestre_guia(
    guia_id: int,
    datos: EditarSemestreGuiaRequest,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> GuiaResponse:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None or guia.programa_id is None or not ProgramaRepository(db).dirige(
        guia.programa_id, director_programa_id
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    guia.actualizar_semestre(datos.semestre)
    guia.regenerar_pdf()

    return guia_repo.actualizar(guia)


@router.put("/guias/{guia_id}/texto-sistema-evaluacion", response_model=GuiaResponse)
def editar_texto_sistema_evaluacion(
    guia_id: int,
    datos: EditarTextoSistemaEvaluacionRequest,
    db: Session = Depends(get_db),
    profesor_id: int = Depends(get_current_profesor_id),
) -> GuiaResponse:
    """issue #610: guardado propio del texto de convocatorias, independiente
    de guardar_borrador_guia. Mismo dueño que el resto de "Gestionar
    evaluación" (Profesor que imparte); Admin/Director quedan fuera (#601)."""
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if (
        guia is None
        or guia.asignatura_programa_id is None
        or not AsignaturaProgramaRepository(db).imparte(
            guia.asignatura_programa_id, profesor_id
        )
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    if datos.texto.count(MARCADOR_TABLA) != 1:
        raise HTTPException(
            status_code=422,
            detail=f"El texto debe contener el marcador {MARCADOR_TABLA} exactamente una vez",
        )

    guia.texto_sistema_evaluacion = datos.texto
    return guia_repo.actualizar(guia)


@router.get("/guias/{guia_id}/pdf")
def descargar_guia_pdf(
    guia_id: int,
    db: Session = Depends(get_db),
    # Actor Admin / Profesor / DirectorPrograma, 404 uniforme -- el RUP de este CU
    # lo documenta desde el origen; la auth real se había quedado en
    # Profesor-only y se alineó al cerrar issue #220 (#238). previsualizar_guia()
    # usa este mismo gate desde #262.
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> Response:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None or not (
        admin_email is not None
        or _tiene_acceso_a_guia(db, guia, profesor_id, director_programa_id)
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    if not guia.tiene_pdf_generado():
        raise HTTPException(status_code=409, detail="PDF no generado todavía")

    # Render real de la plantilla oficial desde la fila Guia (v1, discussion
    # #218): re-render en cada descarga, sin almacenar bytes (D3). El temario
    # es Guia.contenido, NO guia.asignatura_programa.contenido (#191); los RA se
    # leen en vivo de guia.asignatura_programa (P1 = B, deuda en #219).
    return Response(
        content=render_pdf(guia, db), media_type="application/pdf"
    )


@router.get("/guias/{guia_id}/vista")
def previsualizar_guia(
    guia_id: int,
    db: Session = Depends(get_db),
    # Actor Profesor / DirectorPrograma / Admin, 404 uniforme. #218 P3 fijó el
    # modelo "misma auth que descargarGuiaPDF()"; el §3 dejó a Admin diferido
    # del v1 (opción a) solo porque su auth no existía aún en guia.py. #238 la
    # construyó para /pdf (cerró #220); #262 la aplica aquí -- mismo gate que
    # descargar_guia_pdf(). El `get_current_rol` que había aquí daba 403 a la
    # cuenta que no es Profesor ni DirectorPrograma -> bloqueaba justo al Admin.
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> HTMLResponse:
    guia = GuiaRepository(db).obtener(guia_id)
    if guia is None or not (
        admin_email is not None
        or _tiene_acceso_a_guia(db, guia, profesor_id, director_programa_id)
    ):
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    # Cualquier estado (discussion #218, P4). Si la Guia no está Aprobada, la
    # plantilla pinta una banda de aviso de borrador no oficial.
    return HTMLResponse(
        render_html(guia, db, no_oficial=guia.estado != "Aprobada")
    )


@router.get("/programas/{programa_id}/guias", response_model=list[GuiaResumenResponse])
def listar_guias_del_programa(
    programa_id: int,
    curso: int | None = None,
    db: Session = Depends(get_db),
    # issue #262: actor Admin (monitoreo de la beta) además de DirectorPrograma.
    # Gate "admin o dirige el programa", 404 uniforme -- patrón de descargar_guia_pdf
    # (#238/#220) y previsualizar_guia (#263).
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> list[GuiaResumenResponse]:
    dirige = director_programa_id is not None and ProgramaRepository(db).dirige(
        programa_id, director_programa_id
    )
    if not (admin_email is not None or dirige):
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    # issue #441: ?curso= opcional -- sin él, el curso ACTIVO (comportamiento
    # por defecto elegido, distinto del de #442/Auditoría). Con él, cualquier
    # CursoAcademico existente -- pasado (repasar lo hecho) o futuro ya
    # creado pero aún no activado (la tabla sale vacía sin caso especial,
    # sencillamente no hay Guia todavía). 404 si el id pedido no existe.
    curso_repo = CursoAcademicoRepository(db)
    if curso is None:
        curso_academico = curso_repo.activo(
            ProgramaRepository(db).universidad_id_de(programa_id)
        )
        if curso_academico is None:
            raise RuntimeError("No hay ningún CursoAcademico activo")
    else:
        curso_academico = curso_repo.obtener(curso)
        if curso_academico is None:
            raise HTTPException(status_code=404, detail="CursoAcademico no encontrado")

    guia_repo = GuiaRepository(db)
    return [
        GuiaResumenResponse(
            id=guia.id,
            estado=guia.estado,
            semestre=guia.semestre,
            asignatura_programa_nombre=guia.asignatura_programa_nombre,
            asignatura_programa_curso=guia.asignatura_programa_curso,
            asignatura_programa_semestre_default=guia.asignatura_programa_semestre_default,
            # issue #254: profesorado de la plantilla en vivo, no la copia
            # guia.profesorado.
            profesorado=(
                guia.asignatura_programa.profesorado
                if guia.asignatura_programa is not None
                else []
            ),
            ultima_actualizacion=guia.ultima_actualizacion,
            ultima_actualizacion_rol=guia.ultima_actualizacion_rol,
            # issue #262: la fila de la pantalla de Admin deshabilita
            # "Descargar PDF" cuando es False.
            tiene_pdf=guia.tiene_pdf_generado(),
        )
        for guia in guia_repo.listar_del_programa(programa_id, curso_academico.id)
    ]


@router.post(
    "/programas/{programa_id}/notificar-guias-actualizadas",
    response_model=NotificacionResponse,
)
def notificar_guias_actualizadas(
    programa_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> NotificacionResponse:
    if not ProgramaRepository(db).dirige(programa_id, director_programa_id):
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    # Mecanismo de envío (email, cola, lo que sea) fuera de alcance de esta
    # rebanada -- sin Modelo ni Repository, sin tocar la base de datos.
    return NotificacionResponse(detail="Notificación enviada al Admin")

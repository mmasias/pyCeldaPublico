from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.auth import (
    get_current_admin_email_opcional,
    get_current_director_programa_id_opcional,
)
from app.core.database import get_db
from app.models.programa import Programa
from app.repositories.programa import ProgramaRepository
from app.repositories.resultado_aprendizaje import ResultadoAprendizajeRepository
from app.schemas.resultado_aprendizaje import (
    ResultadoAprendizajeAsignacionesResponse,
    ResultadoAprendizajeCreate,
    ResultadoAprendizajeResponse,
    ResultadoAprendizajeUpdate,
)

router = APIRouter(prefix="/api/v1", tags=["resultados-aprendizaje"])


def _verificar_programa_del_director_o_admin(
    db: Session,
    programa_id: int,
    director_programa_id: int | None,
    admin_email: str | None,
) -> Programa:
    """Director del Programa, o Admin (quien construye el Programa)."""
    programa_repo = ProgramaRepository(db)
    programa = programa_repo.obtener(programa_id)
    if programa is None or (
        admin_email is None
        and (director_programa_id is None or not programa_repo.dirige(programa_id, director_programa_id))
    ):
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa


def _verificar_resultado_del_director(
    db: Session,
    resultado_aprendizaje_id: int,
    director_programa_id: int | None,
    admin_email: str | None,
):
    resultado_repo = ResultadoAprendizajeRepository(db)
    resultado = resultado_repo.obtener(resultado_aprendizaje_id)
    if resultado is None:
        raise HTTPException(
            status_code=404, detail="ResultadoAprendizaje no encontrado"
        )
    try:
        _verificar_programa_del_director_o_admin(
            db, resultado.programa_id, director_programa_id, admin_email
        )
    except HTTPException:
        raise HTTPException(
            status_code=404, detail="ResultadoAprendizaje no encontrado"
        )
    return resultado


@router.get(
    "/programas/{programa_id}/resultados-aprendizaje",
    response_model=list[ResultadoAprendizajeResponse],
)
def listar_resultados_aprendizaje_del_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> list[ResultadoAprendizajeResponse]:
    _verificar_programa_del_director_o_admin(
        db, programa_id, director_programa_id, admin_email
    )
    resultado_repo = ResultadoAprendizajeRepository(db)
    resultados = resultado_repo.listar_del_programa(programa_id)
    conteos = resultado_repo.conteo_asignaturas_por_resultado_aprendizaje_del_programa(
        programa_id
    )
    return [
        ResultadoAprendizajeResponse(
            id=ra.id,
            programa_id=ra.programa_id,
            codigo=ra.codigo,
            tipo=ra.tipo,
            descripcion=ra.descripcion,
            numero_asignaturas=conteos.get(ra.id, 0),
        )
        for ra in resultados
    ]


@router.get(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}",
    response_model=ResultadoAprendizajeResponse,
)
def obtener_resultado_aprendizaje(
    resultado_aprendizaje_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> ResultadoAprendizajeResponse:
    return _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_programa_id, admin_email
    )


@router.post(
    "/programas/{programa_id}/resultados-aprendizaje",
    response_model=ResultadoAprendizajeResponse,
    status_code=201,
)
def crear_resultado_aprendizaje(
    programa_id: int,
    datos: ResultadoAprendizajeCreate,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> ResultadoAprendizajeResponse:
    _verificar_programa_del_director_o_admin(
        db, programa_id, director_programa_id, admin_email
    )
    resultado_repo = ResultadoAprendizajeRepository(db)
    return resultado_repo.crear(
        programa_id, datos.codigo, datos.tipo, datos.descripcion
    )


@router.put(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}",
    response_model=ResultadoAprendizajeResponse,
)
def editar_resultado_aprendizaje(
    resultado_aprendizaje_id: int,
    datos: ResultadoAprendizajeUpdate,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> ResultadoAprendizajeResponse:
    resultado = _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_programa_id, admin_email
    )
    resultado.actualizar(datos.codigo, datos.tipo, datos.descripcion)
    return ResultadoAprendizajeRepository(db).actualizar(resultado)


@router.get(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}/asignaciones",
    response_model=ResultadoAprendizajeAsignacionesResponse,
)
def obtener_asignaciones(
    resultado_aprendizaje_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> ResultadoAprendizajeAsignacionesResponse:
    _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_programa_id, admin_email
    )
    resultado_repo = ResultadoAprendizajeRepository(db)
    materias, asignaturas_programa = resultado_repo.asignaciones(
        resultado_aprendizaje_id
    )
    return ResultadoAprendizajeAsignacionesResponse(
        materias=materias, asignaturas_programa=asignaturas_programa
    )


@router.delete(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}",
    status_code=204,
)
def eliminar_resultado_aprendizaje(
    resultado_aprendizaje_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> Response:
    _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_programa_id, admin_email
    )
    resultado_repo = ResultadoAprendizajeRepository(db)

    asignaciones = resultado_repo.nombres_asignaciones(resultado_aprendizaje_id)
    if asignaciones:
        raise HTTPException(
            status_code=409,
            detail=f"ResultadoAprendizaje asignado a: {', '.join(asignaciones)}",
        )

    resultado_repo.eliminar(resultado_aprendizaje_id)
    return Response(status_code=204)

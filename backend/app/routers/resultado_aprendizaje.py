from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.auth import get_current_director_grado_id
from app.core.database import get_db
from app.repositories.grado import GradoRepository
from app.repositories.resultado_aprendizaje import ResultadoAprendizajeRepository
from app.schemas.resultado_aprendizaje import (
    ResultadoAprendizajeAsignacionesResponse,
    ResultadoAprendizajeCreate,
    ResultadoAprendizajeResponse,
    ResultadoAprendizajeUpdate,
)

router = APIRouter(prefix="/api/v1", tags=["resultados-aprendizaje"])


def _verificar_resultado_del_director(
    db: Session, resultado_aprendizaje_id: int, director_grado_id: int
):
    resultado_repo = ResultadoAprendizajeRepository(db)
    resultado = resultado_repo.obtener(resultado_aprendizaje_id)
    if resultado is None or not GradoRepository(db).dirige(
        resultado.grado_id, director_grado_id
    ):
        raise HTTPException(
            status_code=404, detail="ResultadoAprendizaje no encontrado"
        )
    return resultado


@router.get(
    "/grados/{grado_id}/resultados-aprendizaje",
    response_model=list[ResultadoAprendizajeResponse],
)
def listar_resultados_aprendizaje_del_grado(
    grado_id: int,
    db: Session = Depends(get_db),
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> list[ResultadoAprendizajeResponse]:
    if not GradoRepository(db).dirige(grado_id, director_grado_id):
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    resultado_repo = ResultadoAprendizajeRepository(db)
    return resultado_repo.listar_del_grado(grado_id)


@router.get(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}",
    response_model=ResultadoAprendizajeResponse,
)
def obtener_resultado_aprendizaje(
    resultado_aprendizaje_id: int,
    db: Session = Depends(get_db),
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> ResultadoAprendizajeResponse:
    return _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_grado_id
    )


@router.post(
    "/grados/{grado_id}/resultados-aprendizaje",
    response_model=ResultadoAprendizajeResponse,
    status_code=201,
)
def crear_resultado_aprendizaje(
    grado_id: int,
    datos: ResultadoAprendizajeCreate,
    db: Session = Depends(get_db),
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> ResultadoAprendizajeResponse:
    if not GradoRepository(db).dirige(grado_id, director_grado_id):
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    resultado_repo = ResultadoAprendizajeRepository(db)
    return resultado_repo.crear(
        grado_id, datos.codigo, datos.tipo, datos.descripcion
    )


@router.put(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}",
    response_model=ResultadoAprendizajeResponse,
)
def editar_resultado_aprendizaje(
    resultado_aprendizaje_id: int,
    datos: ResultadoAprendizajeUpdate,
    db: Session = Depends(get_db),
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> ResultadoAprendizajeResponse:
    resultado = _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_grado_id
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
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> ResultadoAprendizajeAsignacionesResponse:
    _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_grado_id
    )
    resultado_repo = ResultadoAprendizajeRepository(db)
    materias, asignaturas_grado = resultado_repo.asignaciones(
        resultado_aprendizaje_id
    )
    return ResultadoAprendizajeAsignacionesResponse(
        materias=materias, asignaturas_grado=asignaturas_grado
    )


@router.delete(
    "/resultados-aprendizaje/{resultado_aprendizaje_id}",
    status_code=204,
)
def eliminar_resultado_aprendizaje(
    resultado_aprendizaje_id: int,
    db: Session = Depends(get_db),
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> Response:
    _verificar_resultado_del_director(
        db, resultado_aprendizaje_id, director_grado_id
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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import (
    get_current_director_programa_id_opcional,
    get_current_profesor_id_opcional,
    get_current_rol,
)
from app.core.database import get_db
from app.models.ponderacion_evaluacion import PonderacionEvaluacion
from app.repositories.asignatura_programa import AsignaturaProgramaRepository
from app.repositories.guia import GuiaRepository
from app.repositories.materia import MateriaRepository
from app.repositories.ponderacion_evaluacion import PonderacionEvaluacionRepository
from app.repositories.sistema_evaluacion import SistemaEvaluacionRepository
from app.routers.guia import (
    aplicar_transicion_por_correccion_del_director,
    autorizar_escritura_guia,
)
from app.schemas.ponderacion_evaluacion import (
    PonderacionEvaluacionCreate,
    PonderacionEvaluacionResponse,
    PonderacionEvaluacionUpdate,
)
from app.schemas.sistema_evaluacion import SistemaEvaluacionResponse

router = APIRouter(prefix="/api/v1", tags=["ponderaciones-evaluacion"])


@router.get(
    "/materias/{materia_id}/sistemas-evaluacion",
    response_model=list[SistemaEvaluacionResponse],
)
def listar_sistemas_evaluacion(
    materia_id: int,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
) -> list[SistemaEvaluacionResponse]:
    materia_repo = MateriaRepository(db)
    materia = materia_repo.obtener(materia_id)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia.listar_sistemas_evaluacion()


@router.get(
    "/guias/{guia_id}/sistemas-evaluacion",
    response_model=list[SistemaEvaluacionResponse],
)
def listar_sistemas_evaluacion_de_guia(
    guia_id: int,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> list[SistemaEvaluacionResponse]:
    """Sistemas de evaluación de la Materia de esta Guía -- para que el
    Profesor vea, al gestionar sus ponderaciones, el catálogo completo de
    rangos válidos (no solo los que ya tiene en uso en esta guía)."""
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None:
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    autorizar_escritura_guia(
        db, guia, profesor_id, director_programa_id, "Guia no encontrada"
    )

    asignatura_repo = AsignaturaProgramaRepository(db)
    asignatura_programa = asignatura_repo.obtener(guia.asignatura_programa_id)
    materia = MateriaRepository(db).obtener(asignatura_programa.materia_id)
    return materia.listar_sistemas_evaluacion()


@router.post(
    "/guias/{guia_id}/ponderaciones-evaluacion",
    response_model=PonderacionEvaluacionResponse,
    status_code=201,
)
def crear_ponderacion_evaluacion(
    guia_id: int,
    datos: PonderacionEvaluacionCreate,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> PonderacionEvaluacionResponse:
    guia_repo = GuiaRepository(db)
    guia = guia_repo.obtener(guia_id)
    if guia is None:
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    como_director = autorizar_escritura_guia(
        db, guia, profesor_id, director_programa_id, "Guia no encontrada"
    )

    sistema_repo = SistemaEvaluacionRepository(db)
    ponderacion_repo = PonderacionEvaluacionRepository(db)

    sistema = sistema_repo.obtener(datos.sistema_evaluacion_id)
    if sistema is None:
        raise HTTPException(status_code=404, detail="SistemaEvaluacion no encontrado")

    if not PonderacionEvaluacion.ponderacion_valida(datos.ponderacion):
        raise HTTPException(
            status_code=422,
            detail="La ponderación de un instrumento debe ser mayor que cero",
        )

    if not sistema.validar_maximo(datos.ponderacion):
        raise HTTPException(
            status_code=422,
            detail="La ponderación supera el máximo del sistema de evaluación",
        )

    if como_director:
        aplicar_transicion_por_correccion_del_director(db, guia, director_programa_id)
    return ponderacion_repo.crear(
        guia_id, datos.sistema_evaluacion_id, datos.descripcion, datos.ponderacion
    )


@router.get(
    "/ponderaciones-evaluacion/{ponderacion_id}",
    response_model=PonderacionEvaluacionResponse,
)
def obtener_ponderacion_evaluacion(
    ponderacion_id: int,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> PonderacionEvaluacionResponse:
    ponderacion_repo = PonderacionEvaluacionRepository(db)
    ponderacion = ponderacion_repo.obtener(ponderacion_id)
    if ponderacion is None:
        raise HTTPException(status_code=404, detail="PonderacionEvaluacion no encontrada")

    guia = ponderacion.guia
    autorizar_escritura_guia(
        db, guia, profesor_id, director_programa_id, "PonderacionEvaluacion no encontrada"
    )
    return ponderacion


@router.put(
    "/ponderaciones-evaluacion/{ponderacion_id}",
    response_model=PonderacionEvaluacionResponse,
)
def editar_ponderacion_evaluacion(
    ponderacion_id: int,
    datos: PonderacionEvaluacionUpdate,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> PonderacionEvaluacionResponse:
    sistema_repo = SistemaEvaluacionRepository(db)
    ponderacion_repo = PonderacionEvaluacionRepository(db)

    ponderacion = ponderacion_repo.obtener(ponderacion_id)
    if ponderacion is None:
        raise HTTPException(status_code=404, detail="PonderacionEvaluacion no encontrada")

    guia = ponderacion.guia
    como_director = autorizar_escritura_guia(
        db, guia, profesor_id, director_programa_id, "PonderacionEvaluacion no encontrada"
    )

    sistema = sistema_repo.obtener(datos.sistema_evaluacion_id)
    if sistema is None:
        raise HTTPException(status_code=404, detail="SistemaEvaluacion no encontrado")

    if not PonderacionEvaluacion.ponderacion_valida(datos.ponderacion):
        raise HTTPException(
            status_code=422,
            detail="La ponderación de un instrumento debe ser mayor que cero",
        )

    if not sistema.validar_maximo(datos.ponderacion):
        raise HTTPException(
            status_code=422,
            detail="La ponderación supera el máximo del sistema de evaluación",
        )

    if como_director:
        aplicar_transicion_por_correccion_del_director(db, guia, director_programa_id)
    ponderacion.actualizar(
        datos.sistema_evaluacion_id, datos.descripcion, datos.ponderacion
    )
    return ponderacion_repo.actualizar(ponderacion)


@router.get(
    "/guias/{guia_id}/ponderaciones-evaluacion",
    response_model=list[PonderacionEvaluacionResponse],
)
def listar_ponderaciones_evaluacion(
    guia_id: int,
    db: Session = Depends(get_db),
    _rol: dict[str, str] = Depends(get_current_rol),
    profesor_id: int | None = Depends(get_current_profesor_id_opcional),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> list[PonderacionEvaluacionResponse]:
    guia_repo = GuiaRepository(db)
    ponderacion_repo = PonderacionEvaluacionRepository(db)

    guia = guia_repo.obtener(guia_id)
    if guia is None:
        raise HTTPException(status_code=404, detail="Guia no encontrada")

    autorizar_escritura_guia(
        db, guia, profesor_id, director_programa_id, "Guia no encontrada"
    )

    return ponderacion_repo.listar_vinculadas_de(
        guia
    ) + ponderacion_repo.listar_pendientes_de(guia_id)

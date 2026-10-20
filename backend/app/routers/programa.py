from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.auth import (
    get_current_admin_email_opcional,
    get_current_director_programa_id,
    get_current_director_programa_id_opcional,
    require_admin,
)
from app.core.database import get_db
from app.models.programa import Programa
from app.repositories.asignatura_programa import AsignaturaProgramaRepository
from app.repositories.programa import ProgramaRepository
from app.repositories.profesor import ProfesorRepository
from app.schemas.asignatura_programa import AsignaturaProgramaResponse
from app.schemas.programa import (
    DirectorProgramaResponse,
    ProgramaCreate,
    ProgramaDetalleResponse,
    ProgramaResponse,
    ProgramaUpdate,
)
from app.schemas.profesor import ProfesorResponse

router = APIRouter(prefix="/api/v1", tags=["programas"])


@router.get("/programas", response_model=list[ProgramaResponse])
def listar_programas(
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
) -> list[ProgramaResponse]:
    # discussion #274: una cuenta que no dirige ningún Programa (Profesor puro,
    # ex-director) recibe [] en vez de 403 -- abrirInicio() incluye siempre
    # la sección "Mis programas" y la presenta vacía. Simétrico con
    # /mis-asignaturas-programa.
    if director_programa_id is None:
        return []
    return [
        ProgramaResponse.desde_programa(programa)
        for programa in ProgramaRepository(db).listar_dirigidos_por(director_programa_id)
    ]


@router.get("/programas/{programa_id}", response_model=ProgramaDetalleResponse)
def obtener_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int = Depends(get_current_director_programa_id),
) -> ProgramaDetalleResponse:
    programa_repo = ProgramaRepository(db)
    asignatura_repo = AsignaturaProgramaRepository(db)

    programa = programa_repo.obtener(programa_id)
    if programa is None or not programa_repo.dirige(programa_id, director_programa_id):
        raise HTTPException(status_code=404, detail="Programa no encontrado")

    asignaturas = asignatura_repo.listar_del_programa(programa_id)
    return ProgramaDetalleResponse(
        id=programa.id,
        codigo=programa.codigo,
        nombre=programa.nombre,
        estado=programa.estado,
        facultad_id=programa.facultad_id,
        codigo_ruct=programa.codigo_ruct,
        denominacion_oficial=programa.denominacion_oficial,
        norma=programa.norma,
        asignaturas_programa=[
            AsignaturaProgramaResponse.model_validate(ag) for ag in asignaturas
        ],
    )


@router.get(
    "/admin/facultades/{facultad_id}/programas", response_model=list[ProgramaResponse]
)
def listar_programas_de_la_facultad(
    facultad_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> list[ProgramaResponse]:
    return [
        ProgramaResponse.desde_programa(programa)
        for programa in ProgramaRepository(db).listar_de_la_facultad(facultad_id)
    ]


@router.post(
    "/admin/facultades/{facultad_id}/programas",
    response_model=ProgramaResponse,
    status_code=201,
)
def crear_programa(
    facultad_id: int,
    datos: ProgramaCreate,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> ProgramaResponse:
    repo = ProgramaRepository(db)
    if repo.obtener_por_codigo(datos.codigo) is not None:
        raise HTTPException(
            status_code=409, detail=f"Ya existe un Programa con código {datos.codigo!r}"
        )
    return ProgramaResponse.desde_programa(repo.crear(datos.codigo, datos.nombre, facultad_id))


@router.get("/admin/programas/{programa_id}", response_model=ProgramaResponse)
def obtener_programa_admin(
    programa_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> ProgramaResponse:
    programa_repo = ProgramaRepository(db)
    programa = programa_repo.obtener(programa_id)
    if programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    directores = [
        DirectorProgramaResponse(profesor_id=profesor.id, nombre=profesor.nombre, email=profesor.email)
        for profesor in programa_repo.listar_directores(programa_id)
    ]
    return ProgramaResponse.desde_programa(programa, directores=directores)


@router.put("/admin/programas/{programa_id}", response_model=ProgramaResponse)
def editar_programa(
    programa_id: int,
    datos: ProgramaUpdate,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> ProgramaResponse:
    repo = ProgramaRepository(db)
    programa = repo.obtener(programa_id)
    if programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    programa.actualizar(datos.nombre)
    return ProgramaResponse.desde_programa(repo.actualizar(programa))


@router.delete("/admin/programas/{programa_id}", response_model=ProgramaResponse)
def eliminar_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> ProgramaResponse:
    repo = ProgramaRepository(db)
    programa = repo.obtener(programa_id)
    if programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    programa.extinguir()
    return ProgramaResponse.desde_programa(repo.actualizar(programa))


@router.get(
    "/admin/programas/{programa_id}/profesores-disponibles-para-dirigir",
    response_model=list[ProfesorResponse],
)
def listar_profesores_disponibles_para_dirigir(
    programa_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> list[ProfesorResponse]:
    if ProgramaRepository(db).obtener(programa_id) is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return ProfesorRepository(db).listar_disponibles_para_dirigir_programa(programa_id)

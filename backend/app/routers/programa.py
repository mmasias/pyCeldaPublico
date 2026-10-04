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
from app.repositories.metodologia_docente import (
    MetodologiaDocenteRepository,
    exigir_metodologia_de_la_universidad,
)
from app.repositories.profesor import ProfesorRepository
from app.schemas.asignatura_programa import AsignaturaProgramaResponse
from app.schemas.programa import (
    DirectorProgramaResponse,
    ProgramaCreate,
    ProgramaDetalleResponse,
    ProgramaResponse,
    ProgramaUpdate,
)
from app.schemas.metodologia_docente import (
    AsociarMetodologiaDocenteCreate,
    MetodologiaDocenteResponse,
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


def _verificar_programa_del_director(
    db: Session,
    programa_id: int,
    director_programa_id: int | None,
    admin_email: str | None,
) -> Programa:
    """Director del Programa, o Admin (ProgramaAdmin.tsx gestiona aquí las
    metodologías del Programa con sesión de Admin, sin ser DirectorPrograma)."""
    programa_repo = ProgramaRepository(db)
    programa = programa_repo.obtener(programa_id)
    if programa is None or (
        admin_email is None
        and (director_programa_id is None or not programa_repo.dirige(programa_id, director_programa_id))
    ):
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa


@router.get(
    "/programas/{programa_id}/metodologias-docentes",
    response_model=list[MetodologiaDocenteResponse],
)
def listar_metodologias_docentes_del_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> list[MetodologiaDocenteResponse]:
    _verificar_programa_del_director(
        db, programa_id, director_programa_id, admin_email
    )
    return ProgramaRepository(db).listar_metodologias_docentes_de(programa_id)


@router.get(
    "/programas/{programa_id}/metodologias-docentes/disponibles",
    response_model=list[MetodologiaDocenteResponse],
)
def listar_metodologias_docentes_disponibles_para_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> list[MetodologiaDocenteResponse]:
    _verificar_programa_del_director(
        db, programa_id, director_programa_id, admin_email
    )
    return MetodologiaDocenteRepository(db).listar_disponibles_para_programa(programa_id)


@router.post("/programas/{programa_id}/metodologias-docentes", status_code=204)
def asociar_metodologia_docente_a_programa(
    programa_id: int,
    datos: AsociarMetodologiaDocenteCreate,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> Response:
    _verificar_programa_del_director(
        db, programa_id, director_programa_id, admin_email
    )
    exigir_metodologia_de_la_universidad(
        db,
        ProgramaRepository(db).universidad_id_de(programa_id),
        datos.metodologia_docente_id,
    )
    ProgramaRepository(db).asociar_metodologia_docente(
        programa_id, datos.metodologia_docente_id
    )
    return Response(status_code=204)


@router.get(
    "/programas/{programa_id}/metodologias-docentes/"
    "{metodologia_docente_id}/puede-desasociarse",
    response_model=list[str],
)
def puede_desasociar_metodologia_docente_del_programa(
    programa_id: int,
    metodologia_docente_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> list[str]:
    """Nombres de las Materia en uso -- [] significa que se puede desasociar."""
    programa = _verificar_programa_del_director(
        db, programa_id, director_programa_id, admin_email
    )
    return programa.materias_con_metodologia_docente(metodologia_docente_id)


@router.delete(
    "/programas/{programa_id}/metodologias-docentes/{metodologia_docente_id}",
    status_code=204,
)
def desasociar_metodologia_docente_del_programa(
    programa_id: int,
    metodologia_docente_id: int,
    db: Session = Depends(get_db),
    director_programa_id: int | None = Depends(get_current_director_programa_id_opcional),
    admin_email: str | None = Depends(get_current_admin_email_opcional),
) -> Response:
    programa = _verificar_programa_del_director(
        db, programa_id, director_programa_id, admin_email
    )
    en_uso = programa.materias_con_metodologia_docente(metodologia_docente_id)
    if en_uso:
        nombres = ", ".join(f"Materia {n!r}" for n in en_uso)
        raise HTTPException(status_code=409, detail=f"En uso en: {nombres}")
    ProgramaRepository(db).desasociar_metodologia_docente(
        programa_id, metodologia_docente_id
    )
    return Response(status_code=204)

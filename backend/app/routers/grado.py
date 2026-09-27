from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import (
    get_current_director_grado_id,
    get_current_director_grado_id_opcional,
    require_admin,
)
from app.core.database import get_db
from app.repositories.asignatura_grado import AsignaturaGradoRepository
from app.repositories.grado import GradoRepository
from app.repositories.profesor import ProfesorRepository
from app.schemas.asignatura_grado import AsignaturaGradoResponse
from app.schemas.grado import (
    DirectorGradoResponse,
    GradoCreate,
    GradoDetalleResponse,
    GradoResponse,
    GradoUpdate,
)
from app.schemas.profesor import ProfesorResponse

router = APIRouter(prefix="/api/v1", tags=["grados"])


@router.get("/grados", response_model=list[GradoResponse])
def listar_grados(
    db: Session = Depends(get_db),
    director_grado_id: int | None = Depends(get_current_director_grado_id_opcional),
) -> list[GradoResponse]:
    # discussion #274: una cuenta que no dirige ningún Grado (Profesor puro,
    # ex-director) recibe [] en vez de 403 -- abrirInicio() incluye siempre
    # la sección "Mis grados" y la presenta vacía. Simétrico con
    # /mis-asignaturas-grado.
    if director_grado_id is None:
        return []
    return [
        GradoResponse.desde_grado(grado)
        for grado in GradoRepository(db).listar_dirigidos_por(director_grado_id)
    ]


@router.get("/grados/{grado_id}", response_model=GradoDetalleResponse)
def obtener_grado(
    grado_id: int,
    db: Session = Depends(get_db),
    director_grado_id: int = Depends(get_current_director_grado_id),
) -> GradoDetalleResponse:
    grado_repo = GradoRepository(db)
    asignatura_repo = AsignaturaGradoRepository(db)

    grado = grado_repo.obtener(grado_id)
    if grado is None or not grado_repo.dirige(grado_id, director_grado_id):
        raise HTTPException(status_code=404, detail="Grado no encontrado")

    asignaturas = asignatura_repo.listar_del_grado(grado_id)
    return GradoDetalleResponse(
        id=grado.id,
        codigo=grado.codigo,
        nombre=grado.nombre,
        estado=grado.estado,
        facultad_id=grado.facultad_id,
        asignaturas_grado=[
            AsignaturaGradoResponse.model_validate(ag) for ag in asignaturas
        ],
    )


@router.get(
    "/admin/facultades/{facultad_id}/grados", response_model=list[GradoResponse]
)
def listar_grados_de_la_facultad(
    facultad_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> list[GradoResponse]:
    return [
        GradoResponse.desde_grado(grado)
        for grado in GradoRepository(db).listar_de_la_facultad(facultad_id)
    ]


@router.post(
    "/admin/facultades/{facultad_id}/grados",
    response_model=GradoResponse,
    status_code=201,
)
def crear_grado(
    facultad_id: int,
    datos: GradoCreate,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> GradoResponse:
    repo = GradoRepository(db)
    if repo.obtener_por_codigo(datos.codigo) is not None:
        raise HTTPException(
            status_code=409, detail=f"Ya existe un Grado con código {datos.codigo!r}"
        )
    return GradoResponse.desde_grado(repo.crear(datos.codigo, datos.nombre, facultad_id))


@router.get("/admin/grados/{grado_id}", response_model=GradoResponse)
def obtener_grado_admin(
    grado_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> GradoResponse:
    grado_repo = GradoRepository(db)
    grado = grado_repo.obtener(grado_id)
    if grado is None:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    directores = [
        DirectorGradoResponse(profesor_id=profesor.id, nombre=profesor.nombre, email=profesor.email)
        for profesor in grado_repo.listar_directores(grado_id)
    ]
    return GradoResponse.desde_grado(grado, directores=directores)


@router.put("/admin/grados/{grado_id}", response_model=GradoResponse)
def editar_grado(
    grado_id: int,
    datos: GradoUpdate,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> GradoResponse:
    repo = GradoRepository(db)
    grado = repo.obtener(grado_id)
    if grado is None:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    grado.actualizar(datos.nombre)
    return GradoResponse.desde_grado(repo.actualizar(grado))


@router.delete("/admin/grados/{grado_id}", response_model=GradoResponse)
def eliminar_grado(
    grado_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> GradoResponse:
    repo = GradoRepository(db)
    grado = repo.obtener(grado_id)
    if grado is None:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    grado.extinguir()
    return GradoResponse.desde_grado(repo.actualizar(grado))


@router.get(
    "/admin/grados/{grado_id}/profesores-disponibles-para-dirigir",
    response_model=list[ProfesorResponse],
)
def listar_profesores_disponibles_para_dirigir(
    grado_id: int,
    db: Session = Depends(get_db),
    _email: str = Depends(require_admin),
) -> list[ProfesorResponse]:
    if GradoRepository(db).obtener(grado_id) is None:
        raise HTTPException(status_code=404, detail="Grado no encontrado")
    return ProfesorRepository(db).listar_disponibles_para_dirigir_grado(grado_id)

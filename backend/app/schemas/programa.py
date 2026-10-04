from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from app.schemas.asignatura_programa import AsignaturaProgramaResponse

if TYPE_CHECKING:
    from app.models.programa import Programa


class DirectorProgramaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    profesor_id: int
    nombre: str | None = None
    email: str


class ProgramaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    estado: str
    facultad_id: int | None
    # Issue #492: Directores de Programa, resueltos vía DirectorPrograma.email ->
    # Profesor.email (nunca DirectorPrograma.id, detalle interno -- ver
    # docstring de app/models/director_programa.py). Default []: solo
    # obtener_programa_admin() lo rellena de verdad -- el endpoint del propio
    # Director (GET /programas/{programa_id}) no lo necesita, mismo criterio que
    # #487/#488.
    directores: list[DirectorProgramaResponse] = []

    @classmethod
    def desde_programa(
        cls, programa: "Programa", directores: list[DirectorProgramaResponse] | None = None
    ) -> "ProgramaResponse":
        """Construye explícito, nunca vía model_validate(programa) -- Programa.
        directores es una relación ORM real (list[DirectorPrograma], con `id`/
        `email` propios) de forma incompatible con este campo
        (`profesor_id`/`nombre`/`email`); dejar que `from_attributes`
        recorra esa relación automáticamente rompería con un Programa que ya
        tuviera directores asignados."""
        return cls(
            id=programa.id,
            codigo=programa.codigo,
            nombre=programa.nombre,
            estado=programa.estado,
            facultad_id=programa.facultad_id,
            directores=directores or [],
        )


class ProgramaDetalleResponse(ProgramaResponse):
    asignaturas_programa: list[AsignaturaProgramaResponse]


class ProgramaCreate(BaseModel):
    codigo: str
    nombre: str


class ProgramaUpdate(BaseModel):
    nombre: str

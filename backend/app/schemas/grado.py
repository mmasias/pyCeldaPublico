from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from app.schemas.asignatura_grado import AsignaturaGradoResponse

if TYPE_CHECKING:
    from app.models.grado import Grado


class DirectorGradoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    profesor_id: int
    nombre: str | None = None
    email: str


class GradoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    estado: str
    facultad_id: int | None
    # Issue #492: Directores de Grado, resueltos vía DirectorGrado.email ->
    # Profesor.email (nunca DirectorGrado.id, detalle interno -- ver
    # docstring de app/models/director_grado.py). Default []: solo
    # obtener_grado_admin() lo rellena de verdad -- el endpoint del propio
    # Director (GET /grados/{grado_id}) no lo necesita, mismo criterio que
    # #487/#488.
    directores: list[DirectorGradoResponse] = []

    @classmethod
    def desde_grado(
        cls, grado: "Grado", directores: list[DirectorGradoResponse] | None = None
    ) -> "GradoResponse":
        """Construye explícito, nunca vía model_validate(grado) -- Grado.
        directores es una relación ORM real (list[DirectorGrado], con `id`/
        `email` propios) de forma incompatible con este campo
        (`profesor_id`/`nombre`/`email`); dejar que `from_attributes`
        recorra esa relación automáticamente rompería con un Grado que ya
        tuviera directores asignados."""
        return cls(
            id=grado.id,
            codigo=grado.codigo,
            nombre=grado.nombre,
            estado=grado.estado,
            facultad_id=grado.facultad_id,
            directores=directores or [],
        )


class GradoDetalleResponse(GradoResponse):
    asignaturas_grado: list[AsignaturaGradoResponse]


class GradoCreate(BaseModel):
    codigo: str
    nombre: str


class GradoUpdate(BaseModel):
    nombre: str

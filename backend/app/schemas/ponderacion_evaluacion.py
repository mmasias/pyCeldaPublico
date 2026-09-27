from pydantic import BaseModel, ConfigDict

from app.schemas.sistema_evaluacion import SistemaEvaluacionResponse


class PonderacionEvaluacionCreate(BaseModel):
    sistema_evaluacion_id: int
    descripcion: str
    ponderacion: float


class PonderacionEvaluacionUpdate(BaseModel):
    sistema_evaluacion_id: int
    descripcion: str
    ponderacion: float


class PonderacionEvaluacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    guia_id: int
    sistema_evaluacion_id: int
    sistema_evaluacion: SistemaEvaluacionResponse
    descripcion: str
    ponderacion: float
    vinculada: bool

from typing import Literal

from pydantic import BaseModel, ConfigDict

TipoSistemaEvaluacion = Literal["Evaluación continua", "Evaluación final"]


class SistemaEvaluacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    materia_id: int
    tipo: str
    descripcion: str
    ponderacion_minima: float
    ponderacion_maxima: float


class SistemaEvaluacionCreate(BaseModel):
    tipo: TipoSistemaEvaluacion
    descripcion: str = ""
    ponderacion_minima: float
    ponderacion_maxima: float


class SistemaEvaluacionUpdate(BaseModel):
    tipo: TipoSistemaEvaluacion
    descripcion: str = ""
    ponderacion_minima: float
    ponderacion_maxima: float

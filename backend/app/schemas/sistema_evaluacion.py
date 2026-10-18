from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.core.limites import validar_longitud

TipoSistemaEvaluacion = Literal["Evaluación continua", "Evaluación final"]


class SistemaEvaluacionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    materia_id: int
    codigo: str | None = None
    tipo: str
    descripcion: str
    ponderacion_minima: float
    ponderacion_maxima: float


class _RangoPonderacion(BaseModel):
    ponderacion_minima: float
    ponderacion_maxima: float

    @model_validator(mode="after")
    def _rango_coherente(self):
        # #755: la misma regla que rangoValido() del frontend, ahora también en
        # el servidor (el Director puede crear y editar sistemas). Un rango
        # invertido dejaría toda guía de la materia sin poder enviarse.
        if not 0 <= self.ponderacion_minima <= self.ponderacion_maxima <= 100:
            raise ValueError("La ponderación debe cumplir 0 <= mínima <= máxima <= 100")
        return self


class _DatosSistemaEvaluacion(_RangoPonderacion):
    # Código de la memoria (#772, p. ej. E1), opcional: vacío se guarda como NULL.
    codigo: str | None = None
    tipo: TipoSistemaEvaluacion
    descripcion: str = ""

    @field_validator("codigo")
    @classmethod
    def _codigo(cls, valor: str | None) -> str | None:
        if valor is None:
            return None
        valor = valor.strip()
        return validar_longitud(valor, 20, "El código") or None


class SistemaEvaluacionCreate(_DatosSistemaEvaluacion):
    pass


class SistemaEvaluacionUpdate(_DatosSistemaEvaluacion):
    pass

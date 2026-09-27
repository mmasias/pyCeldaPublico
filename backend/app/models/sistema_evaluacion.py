from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.materia import Materia


class SistemaEvaluacion(Base):
    __tablename__ = "sistemas_evaluacion"

    id: Mapped[int] = mapped_column(primary_key=True)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"))
    tipo: Mapped[str] = mapped_column(String(50))
    descripcion: Mapped[str] = mapped_column(String(200))
    ponderacion_minima: Mapped[float] = mapped_column(Numeric(5, 2))
    ponderacion_maxima: Mapped[float] = mapped_column(Numeric(5, 2))

    materia: Mapped["Materia"] = relationship(back_populates="sistemas_evaluacion")

    def actualizar(
        self,
        tipo: str,
        descripcion: str,
        ponderacion_minima: float,
        ponderacion_maxima: float,
    ) -> None:
        self.tipo = tipo
        self.descripcion = descripcion
        self.ponderacion_minima = ponderacion_minima
        self.ponderacion_maxima = ponderacion_maxima

    def validar_maximo(self, ponderacion: float) -> bool:
        return ponderacion <= float(self.ponderacion_maxima)

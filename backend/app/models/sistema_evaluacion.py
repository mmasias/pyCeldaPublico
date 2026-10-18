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
    # Código de la memoria (#772, p. ej. E1); `descripcion` es su denominación
    # literal. Vacío en los sistemas anteriores a la importación del RUCT.
    codigo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tipo: Mapped[str] = mapped_column(String(50))
    # 300: la denominación literal de la memoria puede pasar de 200 (E4 de GCTA, 232; #768).
    descripcion: Mapped[str] = mapped_column(String(300))
    ponderacion_minima: Mapped[float] = mapped_column(Numeric(5, 2))
    ponderacion_maxima: Mapped[float] = mapped_column(Numeric(5, 2))

    materia: Mapped["Materia"] = relationship(back_populates="sistemas_evaluacion")

    def actualizar(
        self,
        tipo: str,
        descripcion: str,
        ponderacion_minima: float,
        ponderacion_maxima: float,
        codigo: str | None = None,
    ) -> None:
        self.codigo = codigo
        self.tipo = tipo
        self.descripcion = descripcion
        self.ponderacion_minima = ponderacion_minima
        self.ponderacion_maxima = ponderacion_maxima

    def etiqueta(self) -> str:
        """Nombre legible del sistema en mensajes, historial, guía y PDF. Con código de la
        memoria (#768, fase F2): "SE1 Pruebas teóricas finales". Sin código, la regla de
        #285: antepone `descripcion` al `tipo` solo cuando lo distingue."""
        descripcion = (self.descripcion or "").strip()
        if self.codigo:
            return f"{self.codigo} {descripcion}".strip()
        if descripcion and descripcion.lower() != self.tipo.strip().lower():
            return f"{descripcion} ({self.tipo})"
        return self.tipo

    def validar_maximo(self, ponderacion: float) -> bool:
        return ponderacion <= float(self.ponderacion_maxima)

from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.director_grado import DirectorGrado


grados_directores_grado = Table(
    "grados_directores_grado",
    Base.metadata,
    Column("grado_id", ForeignKey("grados.id"), primary_key=True),
    Column("director_grado_id", ForeignKey("directores_grado.id"), primary_key=True),
)


class Grado(Base):
    __tablename__ = "grados"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True)
    nombre: Mapped[str] = mapped_column(String(200))
    estado: Mapped[str] = mapped_column(String(20), default="Vigente")
    facultad_id: Mapped[int | None] = mapped_column(
        ForeignKey("facultades.id"), nullable=True
    )

    directores: Mapped[list["DirectorGrado"]] = relationship(
        secondary=grados_directores_grado
    )

    def actualizar(self, nombre: str) -> None:
        self.nombre = nombre

    def extinguir(self) -> None:
        self.estado = "Extinguido"

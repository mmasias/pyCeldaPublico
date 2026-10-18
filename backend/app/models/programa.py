from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.director_programa import DirectorPrograma
    from app.models.materia import Materia


programas_directores_programa = Table(
    "programas_directores_programa",
    Base.metadata,
    Column("programa_id", ForeignKey("programas.id"), primary_key=True),
    Column("director_programa_id", ForeignKey("directores_programa.id"), primary_key=True),
)

class Programa(Base):
    __tablename__ = "programas"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True)
    nombre: Mapped[str] = mapped_column(String(200))
    estado: Mapped[str] = mapped_column(String(20), default="Vigente")
    facultad_id: Mapped[int | None] = mapped_column(
        ForeignKey("facultades.id"), nullable=True
    )
    programa_padre_id: Mapped[int | None] = mapped_column(
        ForeignKey("programas_padre.id"), nullable=True
    )
    # Identidad RUCT (#772): la escribe solo la importación; solo lectura en la
    # interfaz. `codigo` sigue siendo la sigla de uso interno (GCTA).
    codigo_ruct: Mapped[str | None] = mapped_column(
        String(20), unique=True, nullable=True
    )
    denominacion_oficial: Mapped[str | None] = mapped_column(
        String(300), nullable=True
    )

    directores: Mapped[list["DirectorPrograma"]] = relationship(
        secondary=programas_directores_programa
    )
    materias: Mapped[list["Materia"]] = relationship(
        back_populates="programa", overlaps="programa"
    )

    def actualizar(self, nombre: str) -> None:
        self.nombre = nombre

    def extinguir(self) -> None:
        self.estado = "Extinguido"

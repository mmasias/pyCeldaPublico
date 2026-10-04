from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.director_programa import DirectorPrograma
    from app.models.materia import Materia
    from app.models.metodologia_docente import MetodologiaDocente


programas_directores_programa = Table(
    "programas_directores_programa",
    Base.metadata,
    Column("programa_id", ForeignKey("programas.id"), primary_key=True),
    Column("director_programa_id", ForeignKey("directores_programa.id"), primary_key=True),
)

programas_metodologias_docentes = Table(
    "programas_metodologias_docentes",
    Base.metadata,
    Column("programa_id", ForeignKey("programas.id"), primary_key=True),
    Column(
        "metodologia_docente_id",
        ForeignKey("metodologias_docentes.id"),
        primary_key=True,
    ),
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

    directores: Mapped[list["DirectorPrograma"]] = relationship(
        secondary=programas_directores_programa
    )
    metodologias_docentes: Mapped[list["MetodologiaDocente"]] = relationship(
        secondary=programas_metodologias_docentes
    )
    materias: Mapped[list["Materia"]] = relationship(
        back_populates="programa", overlaps="programa"
    )

    def actualizar(self, nombre: str) -> None:
        self.nombre = nombre

    def extinguir(self) -> None:
        self.estado = "Extinguido"

    def materias_con_metodologia_docente(
        self, metodologia_docente_id: int
    ) -> list[str]:
        """Nombres de las Materia de este Programa que ya usan la
        MetodologiaDocente dada -- guarda de desasociar_metodologia_docente(),
        mismo patrón que Materia.asignaturas_programa_con_metodologia_docente()."""
        return [
            materia.nombre
            for materia in self.materias
            for metodologia_materia in materia.metodologias_materia
            if metodologia_materia.metodologia_docente_id == metodologia_docente_id
        ]

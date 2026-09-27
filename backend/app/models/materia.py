from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.actividad_formativa_materia import ActividadFormativaMateria
    from app.models.asignatura_grado import AsignaturaGrado
    from app.models.grado import Grado
    from app.models.metodologia_materia import MetodologiaMateria
    from app.models.resultado_aprendizaje import ResultadoAprendizaje
    from app.models.sistema_evaluacion import SistemaEvaluacion


materias_resultados_aprendizaje = Table(
    "materias_resultados_aprendizaje",
    Base.metadata,
    Column("materia_id", ForeignKey("materias.id"), primary_key=True),
    Column(
        "resultado_aprendizaje_id",
        ForeignKey("resultados_aprendizaje.id"),
        primary_key=True,
    ),
)


class Materia(Base):
    __tablename__ = "materias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    grado_id: Mapped[int | None] = mapped_column(
        ForeignKey("grados.id"), nullable=True
    )

    grado: Mapped["Grado | None"] = relationship()
    sistemas_evaluacion: Mapped[list["SistemaEvaluacion"]] = relationship(
        back_populates="materia"
    )
    metodologias_materia: Mapped[list["MetodologiaMateria"]] = relationship()
    resultados_aprendizaje: Mapped[list["ResultadoAprendizaje"]] = relationship(
        secondary=materias_resultados_aprendizaje
    )
    asignaturas_grado: Mapped[list["AsignaturaGrado"]] = relationship(
        back_populates="materia"
    )
    actividades_formativas: Mapped[list["ActividadFormativaMateria"]] = (
        relationship()
    )

    def actualizar(self, nombre: str) -> None:
        self.nombre = nombre

    def listar_sistemas_evaluacion(self) -> list["SistemaEvaluacion"]:
        return self.sistemas_evaluacion

    def asignaturas_grado_con_metodologia_docente(
        self, metodologia_docente_id: int
    ) -> list[str]:
        """Nombres de las AsignaturaGrado de esta Materia que ya usan la
        MetodologiaDocente dada -- issue #179: antes tiene_metodologia_docente_en_uso()
        (bool), sin el detalle que desasociarMetodologiaDocenteMateria() necesita
        para nombrar el bloqueo (mismo patrón que
        ResultadoAprendizajeRepository.nombres_asignaciones(), PR #178)."""
        return [
            asignatura_grado.nombre
            for asignatura_grado in self.asignaturas_grado
            for metodologia_docente in asignatura_grado.metodologias_docentes
            if metodologia_docente.id == metodologia_docente_id
        ]

    def asignaturas_grado_con_resultado_aprendizaje(
        self, resultado_aprendizaje_id: int
    ) -> list[str]:
        """Análogo a asignaturas_grado_con_metodologia_docente() (issue #179)."""
        return [
            asignatura_grado.nombre
            for asignatura_grado in self.asignaturas_grado
            for resultado_aprendizaje in asignatura_grado.resultados_aprendizaje
            if resultado_aprendizaje.id == resultado_aprendizaje_id
        ]

    def discrepancias_actividades_formativas(self) -> list[dict]:
        """Regla `AfM = Σ AfAdM` (discussion #227): por cada `ActividadFormativa`,
        `horas` de la materia frente a la suma de `horas` de sus `AsignaturaGrado`.
        Medidor BLANDO -- informa, no bloquea ningún guardado (mismo espíritu
        que `Guia.bloqueo_ponderaciones()`, que sí bloquea; aquí no hay nada que
        bloquear). Recorre las 10 filas de `self.actividades_formativas` en
        orden canónico AF1..AF10, no solo las que tienen horas > 0."""
        horas_por_actividad: dict[int, float] = {}
        for asignatura_grado in self.asignaturas_grado:
            for afag in asignatura_grado.actividades_formativas:
                horas_por_actividad[afag.actividad_formativa_id] = (
                    horas_por_actividad.get(afag.actividad_formativa_id, 0.0)
                    + float(afag.horas)
                )

        resultado = []
        for afm in sorted(
            self.actividades_formativas, key=lambda f: f.actividad_formativa_id
        ):
            horas_materia = float(afm.horas)
            horas_asignaturas = round(
                horas_por_actividad.get(afm.actividad_formativa_id, 0.0), 2
            )
            # Redondeo a 2 decimales antes de comparar: horas_asignaturas suma
            # floats de varias AsignaturaGrado (step="any" en el input, PR#233),
            # el ruido de representación binaria (0.1+0.2 != 0.3) puede dar un
            # falso "Discrepancia" con una comparación exacta -- y sin redondear
            # aquí, el frontend mostraba diferencias tipo +0.10000000000000142.
            diferencia = round(horas_asignaturas - horas_materia, 2)
            resultado.append(
                {
                    "codigo": afm.actividad_formativa.codigo,
                    "nombre": afm.actividad_formativa.nombre,
                    "horas_materia": horas_materia,
                    "horas_asignaturas": horas_asignaturas,
                    "cuadra": diferencia == 0,
                    "diferencia": diferencia,
                }
            )
        return resultado

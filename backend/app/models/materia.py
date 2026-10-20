from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Numeric, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.actividad_formativa_materia import ActividadFormativaMateria
    from app.models.asignatura_programa import AsignaturaPrograma
    from app.models.competencia import Competencia
    from app.models.modulo import Modulo
    from app.models.programa import Programa
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

materias_competencias = Table(
    "materias_competencias",
    Base.metadata,
    Column("materia_id", ForeignKey("materias.id"), primary_key=True),
    Column("competencia_id", ForeignKey("competencias.id"), primary_key=True),
)


# Horas de trabajo del alumno por crédito ECTS (#772).
HORAS_POR_ECTS = 25


class Materia(Base):
    __tablename__ = "materias"
    __table_args__ = (UniqueConstraint("programa_id", "codigo_ruct"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    programa_id: Mapped[int | None] = mapped_column(
        ForeignKey("programas.id"), nullable=True
    )
    # Módulo del Programa al que pertenece (#762), opcional: 0..1.
    modulo_id: Mapped[int | None] = mapped_column(
        ForeignKey("modulos.id"), nullable=True
    )
    # Identidad RUCT (#772): `codMateria` de la memoria y sus ECTS aprobados.
    # Los escribe solo la importación; solo lectura en la interfaz. Los ECTS no
    # siempre son la suma de los de sus AsignaturaPrograma (optatividad).
    codigo_ruct: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ects: Mapped[float | None] = mapped_column(Numeric(5, 1), nullable=True)

    programa: Mapped["Programa | None"] = relationship(back_populates="materias")
    modulo: Mapped["Modulo | None"] = relationship(back_populates="materias")
    sistemas_evaluacion: Mapped[list["SistemaEvaluacion"]] = relationship(
        back_populates="materia"
    )
    metodologias_materia: Mapped[list["MetodologiaMateria"]] = relationship()
    resultados_aprendizaje: Mapped[list["ResultadoAprendizaje"]] = relationship(
        secondary=materias_resultados_aprendizaje
    )
    competencias: Mapped[list["Competencia"]] = relationship(
        secondary=materias_competencias
    )
    asignaturas_programa: Mapped[list["AsignaturaPrograma"]] = relationship(
        back_populates="materia"
    )
    actividades_formativas: Mapped[list["ActividadFormativaMateria"]] = (
        relationship()
    )

    @property
    def modulo_codigo(self) -> str | None:
        return self.modulo.codigo if self.modulo is not None else None

    @property
    def modulo_nombre(self) -> str | None:
        return self.modulo.nombre if self.modulo is not None else None

    def actualizar(self, nombre: str) -> None:
        self.nombre = nombre

    def listar_sistemas_evaluacion(self) -> list["SistemaEvaluacion"]:
        return self.sistemas_evaluacion

    def asignaturas_programa_con_metodologia_docente(
        self, metodologia_docente_id: int
    ) -> list[str]:
        """Nombres de las AsignaturaPrograma de esta Materia que ya usan la
        MetodologiaDocente dada -- issue #179: antes tiene_metodologia_docente_en_uso()
        (bool), sin el detalle que desasociarMetodologiaDocenteMateria() necesita
        para nombrar el bloqueo (mismo patrón que
        ResultadoAprendizajeRepository.nombres_asignaciones(), PR #178)."""
        return [
            asignatura_programa.nombre
            for asignatura_programa in self.asignaturas_programa
            for metodologia_docente in asignatura_programa.metodologias_docentes
            if metodologia_docente.id == metodologia_docente_id
        ]

    def asignaturas_programa_con_resultado_aprendizaje(
        self, resultado_aprendizaje_id: int
    ) -> list[str]:
        """Análogo a asignaturas_programa_con_metodologia_docente() (issue #179)."""
        return [
            asignatura_programa.nombre
            for asignatura_programa in self.asignaturas_programa
            for resultado_aprendizaje in asignatura_programa.resultados_aprendizaje
            if resultado_aprendizaje.id == resultado_aprendizaje_id
        ]

    def asignaturas_programa_con_competencia(self, competencia_id: int) -> list[str]:
        """Análogo a asignaturas_programa_con_resultado_aprendizaje() (#761)."""
        return [
            asignatura_programa.nombre
            for asignatura_programa in self.asignaturas_programa
            for competencia in asignatura_programa.competencias
            if competencia.id == competencia_id
        ]

    def discrepancias_actividades_formativas(self) -> list[dict]:
        """Regla `AfM = Σ AfAdM` (discussion #227): por cada `ActividadFormativa`,
        `horas` de la materia frente a la suma de `horas` de sus `AsignaturaPrograma`.
        Medidor BLANDO -- informa, no bloquea ningún guardado (mismo espíritu
        que `Guia.bloqueo_ponderaciones()`, que sí bloquea; aquí no hay nada que
        bloquear). Recorre todas las filas de `self.actividades_formativas` en orden
        canónico, no solo las que tienen horas > 0.

        Con optatividad (#786) no se compara: cada asignatura lleva 25 h por
        ECTS y la suma de las de la materia supera sus horas por diseño."""
        if self.con_optatividad():
            return []
        horas_por_actividad: dict[int, float] = {}
        for asignatura_programa in self.asignaturas_programa:
            for afag in asignatura_programa.actividades_formativas:
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
            # floats de varias AsignaturaPrograma (step="any" en el input, PR#233),
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

    def comprobacion_horas_ects(self) -> dict | None:
        """Horas de las actividades formativas de la materia frente a
        `HORAS_POR_ECTS` × `ects` (#772). Medidor blando e informativo, como
        `discrepancias_actividades_formativas()`: no reparte ni bloquea nada.
        Sin `ects` (materia sin importar del RUCT) no hay con qué comparar."""
        comprobacion = self._horas_frente_a_ects()
        if comprobacion is None:
            return None
        horas_materia, horas_esperadas = comprobacion
        diferencia = round(horas_materia - horas_esperadas, 2)
        return {
            "ects": float(self.ects),
            "horas_esperadas": horas_esperadas,
            "horas_materia": horas_materia,
            "cuadra": diferencia == 0,
            "diferencia": diferencia,
            "ects_asignaturas": self.ects_asignaturas(),
            "con_optatividad": self.con_optatividad(),
        }

    def ects_asignaturas(self) -> float:
        return round(sum(float(ap.ects or 0) for ap in self.asignaturas_programa), 1)

    def con_optatividad(self) -> bool:
        """La materia suma 25 h por ECTS y sus asignaturas no suman sus ECTS
        (#786): optativas o idiomas alternativos, o asignaturas de la memoria
        en otra materia. Cada asignatura recibe entonces 25 h por ECTS
        (`repartir_horas_asignaturas.py`) y la regla AfM = Σ AfAdM no se
        cumple por diseño. El mismo criterio usa ese script."""
        comprobacion = self._horas_frente_a_ects()
        ects_asignaturas = self.ects_asignaturas()
        # Sin ECTS, sin horas o sin asignaturas con ECTS no hay reparto que
        # comparar: el script tampoco las toca.
        return (
            comprobacion is not None
            and comprobacion[1] > 0
            and comprobacion[0] == comprobacion[1]
            and ects_asignaturas > 0
            and ects_asignaturas != float(self.ects)
        )

    def _horas_frente_a_ects(self) -> tuple[float, float] | None:
        if self.ects is None:
            return None
        return (
            round(sum(float(f.horas) for f in self.actividades_formativas), 2),
            round(float(self.ects) * HORAS_POR_ECTS, 2),
        )

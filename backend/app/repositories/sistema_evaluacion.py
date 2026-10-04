from sqlalchemy.orm import Session

from app.models.asignatura_programa import AsignaturaPrograma
from app.models.guia import Guia
from app.models.ponderacion_evaluacion import PonderacionEvaluacion
from app.models.sistema_evaluacion import SistemaEvaluacion


class SistemaEvaluacionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_de_materia(
        self, materia_id: int
    ) -> list[SistemaEvaluacion]:
        return (
            self.db.query(SistemaEvaluacion)
            .filter_by(materia_id=materia_id)
            .all()
        )

    def obtener(self, sistema_evaluacion_id: int) -> SistemaEvaluacion | None:
        return self.db.get(SistemaEvaluacion, sistema_evaluacion_id)

    def crear(
        self,
        materia_id: int,
        tipo: str,
        descripcion: str,
        ponderacion_minima: float,
        ponderacion_maxima: float,
    ) -> SistemaEvaluacion:
        sistema_evaluacion = SistemaEvaluacion(
            materia_id=materia_id,
            tipo=tipo,
            descripcion=descripcion,
            ponderacion_minima=ponderacion_minima,
            ponderacion_maxima=ponderacion_maxima,
        )
        self.db.add(sistema_evaluacion)
        self.db.commit()
        self.db.refresh(sistema_evaluacion)
        return sistema_evaluacion

    def editar(
        self,
        sistema_evaluacion: SistemaEvaluacion,
        tipo: str,
        descripcion: str,
        ponderacion_minima: float,
        ponderacion_maxima: float,
    ) -> SistemaEvaluacion:
        sistema_evaluacion.actualizar(
            tipo, descripcion, ponderacion_minima, ponderacion_maxima
        )
        self.db.commit()
        self.db.refresh(sistema_evaluacion)
        return sistema_evaluacion

    def nombres_asignaciones(self, sistema_evaluacion_id: int) -> list[str]:
        nombres = (
            self.db.query(AsignaturaPrograma.nombre)
            .join(Guia, Guia.asignatura_programa_id == AsignaturaPrograma.id)
            .join(PonderacionEvaluacion, PonderacionEvaluacion.guia_id == Guia.id)
            .filter(
                PonderacionEvaluacion.sistema_evaluacion_id
                == sistema_evaluacion_id
            )
            .distinct()
            .order_by(AsignaturaPrograma.nombre)
            .all()
        )
        return [f"AsignaturaPrograma '{nombre}'" for (nombre,) in nombres]

    def eliminar(self, sistema_evaluacion_id: int) -> None:
        sistema_evaluacion = self.db.get(
            SistemaEvaluacion, sistema_evaluacion_id
        )
        self.db.delete(sistema_evaluacion)
        self.db.commit()

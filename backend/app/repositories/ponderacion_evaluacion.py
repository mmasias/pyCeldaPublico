from sqlalchemy.orm import Session, joinedload

from app.models.guia import Guia
from app.models.ponderacion_evaluacion import PonderacionEvaluacion


class PonderacionEvaluacionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(
        self,
        guia_id: int,
        sistema_evaluacion_id: int,
        descripcion: str,
        ponderacion: float,
    ) -> PonderacionEvaluacion:
        ponderacion_evaluacion = PonderacionEvaluacion(
            guia_id=guia_id,
            sistema_evaluacion_id=sistema_evaluacion_id,
            descripcion=descripcion,
            ponderacion=ponderacion,
        )
        self.db.add(ponderacion_evaluacion)
        self.db.commit()
        self.db.refresh(ponderacion_evaluacion)
        return ponderacion_evaluacion

    def obtener(self, ponderacion_id: int) -> PonderacionEvaluacion | None:
        return self.db.get(
            PonderacionEvaluacion,
            ponderacion_id,
            options=[joinedload(PonderacionEvaluacion.sistema_evaluacion)],
        )

    def actualizar(self, ponderacion: PonderacionEvaluacion) -> PonderacionEvaluacion:
        self.db.commit()
        self.db.refresh(ponderacion)
        return ponderacion

    def listar_vinculadas_de(self, guia: Guia) -> list[PonderacionEvaluacion]:
        return [p for p in guia.ponderaciones if p.vinculada]

    def listar_pendientes_de(self, guia_id: int) -> list[PonderacionEvaluacion]:
        return (
            self.db.query(PonderacionEvaluacion)
            .filter_by(guia_id=guia_id, vinculada=False)
            .options(joinedload(PonderacionEvaluacion.sistema_evaluacion))
            .all()
        )

    def existe_pendiente_de(self, guia_id: int) -> bool:
        return (
            self.db.query(PonderacionEvaluacion)
            .filter_by(guia_id=guia_id, vinculada=False)
            .first()
            is not None
        )

    def vincular(self, id: int, guia: Guia) -> None:
        ponderacion = self.db.get(PonderacionEvaluacion, id)
        ponderacion.vinculada = True
        self.db.commit()

    def desvincular(self, id: int) -> None:
        ponderacion = self.db.get(PonderacionEvaluacion, id)
        self.db.delete(ponderacion)
        self.db.commit()

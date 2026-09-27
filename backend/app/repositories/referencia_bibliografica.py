from sqlalchemy.orm import Session

from app.models.guia import Guia
from app.models.referencia_bibliografica import ReferenciaBibliografica


class ReferenciaBibliograficaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, guia_id: int, tipo: str, referencia: str) -> ReferenciaBibliografica:
        referencia_bibliografica = ReferenciaBibliografica(
            guia_id=guia_id, tipo=tipo, referencia=referencia
        )
        self.db.add(referencia_bibliografica)
        self.db.commit()
        self.db.refresh(referencia_bibliografica)
        return referencia_bibliografica

    def obtener(self, referencia_id: int) -> ReferenciaBibliografica | None:
        return self.db.get(ReferenciaBibliografica, referencia_id)

    def actualizar(
        self, referencia: ReferenciaBibliografica
    ) -> ReferenciaBibliografica:
        self.db.commit()
        self.db.refresh(referencia)
        return referencia

    def listar_vinculadas_de(self, guia: Guia) -> list[ReferenciaBibliografica]:
        return [r for r in guia.referencias if r.vinculada]

    def listar_pendientes_de(self, guia_id: int) -> list[ReferenciaBibliografica]:
        return (
            self.db.query(ReferenciaBibliografica)
            .filter_by(guia_id=guia_id, vinculada=False)
            .all()
        )

    def existe_pendiente_de(self, guia_id: int) -> bool:
        return (
            self.db.query(ReferenciaBibliografica)
            .filter_by(guia_id=guia_id, vinculada=False)
            .first()
            is not None
        )

    def reemplazar_desde(
        self,
        guia_destino: Guia,
        referencias_origen: list[ReferenciaBibliografica],
    ) -> list[ReferenciaBibliografica]:
        """Issue #184: borra TODAS las ReferenciaBibliografica de la guía
        destino (vinculadas y no, incluidas las tecleadas a mano) y crea copias
        de las de origen -- tipo, referencia y el flag `vinculada` replicado
        fila a fila (no se fuerza a True: un origen escalado vía
        escalarGuiaAAprobada() puede llevar candidatas sin vincular). Borrado
        vía ORM (recorre la colección ya cargada) para no dejar el identity map
        desincronizado. NO hace commit -- forma parte de la transacción atómica
        del handler de importación, que confirma una sola vez al final."""
        for referencia in list(guia_destino.referencias):
            self.db.delete(referencia)
        self.db.flush()
        copias = [
            ReferenciaBibliografica(
                guia_id=guia_destino.id,
                tipo=origen.tipo,
                referencia=origen.referencia,
                vinculada=origen.vinculada,
            )
            for origen in referencias_origen
        ]
        self.db.add_all(copias)
        self.db.flush()
        return copias

    def vincular(self, id: int, guia: Guia) -> None:
        referencia = self.db.get(ReferenciaBibliografica, id)
        referencia.vinculada = True
        self.db.commit()

    def desvincular(self, id: int) -> None:
        referencia = self.db.get(ReferenciaBibliografica, id)
        self.db.delete(referencia)
        self.db.commit()

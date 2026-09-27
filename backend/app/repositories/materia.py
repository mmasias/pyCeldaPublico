from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.asignatura_grado import AsignaturaGrado
from app.models.materia import Materia, materias_resultados_aprendizaje
from app.models.resultado_aprendizaje import ResultadoAprendizaje
from app.repositories.actividad_formativa import poblar_actividades_formativas_materia


class MateriaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def obtener(self, materia_id: int) -> Materia | None:
        return self.db.get(Materia, materia_id)

    def crear(self, nombre: str, grado_id: int) -> Materia:
        materia = Materia(nombre=nombre, grado_id=grado_id)
        self.db.add(materia)
        self.db.flush()
        # Invariante de autopoblado (discussion #227): las 10 ActividadFormativa
        # nacen a 0 con la Materia, atómico con el alta.
        poblar_actividades_formativas_materia(self.db, materia.id)
        self.db.commit()
        self.db.refresh(materia)
        return materia

    def actualizar(self, materia: Materia) -> Materia:
        self.db.commit()
        self.db.refresh(materia)
        return materia

    def listar_del_grado(self, grado_id: int) -> list[Materia]:
        return self.db.query(Materia).filter_by(grado_id=grado_id).all()

    def contar_asignaturas_grado_por_materia(self) -> dict[int, int]:
        """Una sola consulta agregada (GROUP BY sobre asignaturas_grado),
        mismo patrón que ProfesorRepository.contar_asignaturas_por_profesor()
        (issue #310) -- issue #487."""
        filas = (
            self.db.query(AsignaturaGrado.materia_id, func.count(AsignaturaGrado.id))
            .group_by(AsignaturaGrado.materia_id)
            .all()
        )
        return {materia_id: total for materia_id, total in filas}

    def listar_resultados_aprendizaje_de(
        self, materia_id: int
    ) -> list[ResultadoAprendizaje]:
        return (
            self.db.query(ResultadoAprendizaje)
            .join(
                materias_resultados_aprendizaje,
                materias_resultados_aprendizaje.c.resultado_aprendizaje_id
                == ResultadoAprendizaje.id,
            )
            .filter(materias_resultados_aprendizaje.c.materia_id == materia_id)
            .all()
        )

    def listar_resultados_aprendizaje_disponibles(
        self, materia_id: int
    ) -> list[ResultadoAprendizaje]:
        return (
            self.db.query(ResultadoAprendizaje)
            .join(
                Materia,
                Materia.grado_id == ResultadoAprendizaje.grado_id,
            )
            .outerjoin(
                materias_resultados_aprendizaje,
                and_(
                    materias_resultados_aprendizaje.c.resultado_aprendizaje_id
                    == ResultadoAprendizaje.id,
                    materias_resultados_aprendizaje.c.materia_id == materia_id,
                ),
            )
            .filter(
                Materia.id == materia_id,
                materias_resultados_aprendizaje.c.materia_id.is_(None),
            )
            .all()
        )

    def asociar_resultado_aprendizaje(
        self, materia_id: int, resultado_aprendizaje_id: int
    ) -> None:
        self.db.execute(
            materias_resultados_aprendizaje.insert().values(
                materia_id=materia_id,
                resultado_aprendizaje_id=resultado_aprendizaje_id,
            )
        )
        self.db.commit()

    def desasociar_resultado_aprendizaje(
        self, materia_id: int, resultado_aprendizaje_id: int
    ) -> None:
        self.db.execute(
            materias_resultados_aprendizaje.delete().where(
                materias_resultados_aprendizaje.c.materia_id == materia_id,
                materias_resultados_aprendizaje.c.resultado_aprendizaje_id
                == resultado_aprendizaje_id,
            )
        )
        self.db.commit()

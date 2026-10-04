from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.asignatura_programa import (
    AsignaturaPrograma,
    asignaturas_programa_resultados_aprendizaje,
)
from app.models.materia import Materia, materias_resultados_aprendizaje
from app.models.resultado_aprendizaje import ResultadoAprendizaje


class ResultadoAprendizajeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_del_programa(self, programa_id: int) -> list[ResultadoAprendizaje]:
        return (
            self.db.query(ResultadoAprendizaje)
            .filter_by(programa_id=programa_id)
            .all()
        )

    def conteo_asignaturas_por_resultado_aprendizaje_del_programa(self, programa_id: int) -> dict[int, int]:
        filas = (
            self.db.query(
                asignaturas_programa_resultados_aprendizaje.c.resultado_aprendizaje_id,
                func.count(asignaturas_programa_resultados_aprendizaje.c.asignatura_programa_id),
            )
            .join(
                AsignaturaPrograma,
                AsignaturaPrograma.id
                == asignaturas_programa_resultados_aprendizaje.c.asignatura_programa_id,
            )
            .join(Materia, Materia.id == AsignaturaPrograma.materia_id)
            .filter(Materia.programa_id == programa_id)
            .group_by(asignaturas_programa_resultados_aprendizaje.c.resultado_aprendizaje_id)
            .all()
        )
        return dict(filas)

    def obtener(
        self, resultado_aprendizaje_id: int
    ) -> ResultadoAprendizaje | None:
        return self.db.get(ResultadoAprendizaje, resultado_aprendizaje_id)

    def actualizar(
        self, resultado_aprendizaje: ResultadoAprendizaje
    ) -> ResultadoAprendizaje:
        self.db.commit()
        self.db.refresh(resultado_aprendizaje)
        return resultado_aprendizaje

    def crear(
        self, programa_id: int, codigo: str, tipo: str, descripcion: str
    ) -> ResultadoAprendizaje:
        resultado_aprendizaje = ResultadoAprendizaje(
            programa_id=programa_id,
            codigo=codigo,
            tipo=tipo,
            descripcion=descripcion,
        )
        self.db.add(resultado_aprendizaje)
        self.db.commit()
        self.db.refresh(resultado_aprendizaje)
        return resultado_aprendizaje

    def asignaciones(
        self, resultado_aprendizaje_id: int
    ) -> tuple[list[str], list[str]]:
        nombres_materias = [
            nombre
            for (nombre,) in self.db.query(Materia.nombre)
            .join(
                materias_resultados_aprendizaje,
                materias_resultados_aprendizaje.c.materia_id == Materia.id,
            )
            .filter(
                materias_resultados_aprendizaje.c.resultado_aprendizaje_id
                == resultado_aprendizaje_id
            )
            .all()
        ]
        nombres_asignaturas_programa = [
            nombre
            for (nombre,) in self.db.query(AsignaturaPrograma.nombre)
            .join(
                asignaturas_programa_resultados_aprendizaje,
                asignaturas_programa_resultados_aprendizaje.c.asignatura_programa_id
                == AsignaturaPrograma.id,
            )
            .filter(
                asignaturas_programa_resultados_aprendizaje.c.resultado_aprendizaje_id
                == resultado_aprendizaje_id
            )
            .all()
        ]
        return nombres_materias, nombres_asignaturas_programa

    def nombres_asignaciones(self, resultado_aprendizaje_id: int) -> list[str]:
        nombres_materias, nombres_asignaturas_programa = self.asignaciones(
            resultado_aprendizaje_id
        )
        return [f"Materia '{nombre}'" for nombre in nombres_materias] + [
            f"AsignaturaPrograma '{nombre}'" for nombre in nombres_asignaturas_programa
        ]

    def eliminar(self, resultado_aprendizaje_id: int) -> None:
        resultado_aprendizaje = self.db.get(
            ResultadoAprendizaje, resultado_aprendizaje_id
        )
        self.db.delete(resultado_aprendizaje)
        self.db.commit()

    def listar_disponibles_para_asignatura_programa(
        self, asignatura_programa_id: int
    ) -> list[ResultadoAprendizaje]:
        return (
            self.db.query(ResultadoAprendizaje)
            .join(
                materias_resultados_aprendizaje,
                materias_resultados_aprendizaje.c.resultado_aprendizaje_id
                == ResultadoAprendizaje.id,
            )
            .join(
                AsignaturaPrograma,
                AsignaturaPrograma.materia_id
                == materias_resultados_aprendizaje.c.materia_id,
            )
            .outerjoin(
                asignaturas_programa_resultados_aprendizaje,
                and_(
                    asignaturas_programa_resultados_aprendizaje.c.resultado_aprendizaje_id
                    == ResultadoAprendizaje.id,
                    asignaturas_programa_resultados_aprendizaje.c.asignatura_programa_id
                    == asignatura_programa_id,
                ),
            )
            .filter(
                AsignaturaPrograma.id == asignatura_programa_id,
                asignaturas_programa_resultados_aprendizaje.c.asignatura_programa_id.is_(
                    None
                ),
            )
            .all()
        )

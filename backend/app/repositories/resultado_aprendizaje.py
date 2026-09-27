from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.asignatura_grado import (
    AsignaturaGrado,
    asignaturas_grado_resultados_aprendizaje,
)
from app.models.materia import Materia, materias_resultados_aprendizaje
from app.models.resultado_aprendizaje import ResultadoAprendizaje


class ResultadoAprendizajeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_del_grado(self, grado_id: int) -> list[ResultadoAprendizaje]:
        return (
            self.db.query(ResultadoAprendizaje)
            .filter_by(grado_id=grado_id)
            .all()
        )

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
        self, grado_id: int, codigo: str, tipo: str, descripcion: str
    ) -> ResultadoAprendizaje:
        resultado_aprendizaje = ResultadoAprendizaje(
            grado_id=grado_id,
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
        nombres_asignaturas_grado = [
            nombre
            for (nombre,) in self.db.query(AsignaturaGrado.nombre)
            .join(
                asignaturas_grado_resultados_aprendizaje,
                asignaturas_grado_resultados_aprendizaje.c.asignatura_grado_id
                == AsignaturaGrado.id,
            )
            .filter(
                asignaturas_grado_resultados_aprendizaje.c.resultado_aprendizaje_id
                == resultado_aprendizaje_id
            )
            .all()
        ]
        return nombres_materias, nombres_asignaturas_grado

    def nombres_asignaciones(self, resultado_aprendizaje_id: int) -> list[str]:
        nombres_materias, nombres_asignaturas_grado = self.asignaciones(
            resultado_aprendizaje_id
        )
        return [f"Materia '{nombre}'" for nombre in nombres_materias] + [
            f"AsignaturaGrado '{nombre}'" for nombre in nombres_asignaturas_grado
        ]

    def eliminar(self, resultado_aprendizaje_id: int) -> None:
        resultado_aprendizaje = self.db.get(
            ResultadoAprendizaje, resultado_aprendizaje_id
        )
        self.db.delete(resultado_aprendizaje)
        self.db.commit()

    def listar_disponibles_para_asignatura_grado(
        self, asignatura_grado_id: int
    ) -> list[ResultadoAprendizaje]:
        return (
            self.db.query(ResultadoAprendizaje)
            .join(
                materias_resultados_aprendizaje,
                materias_resultados_aprendizaje.c.resultado_aprendizaje_id
                == ResultadoAprendizaje.id,
            )
            .join(
                AsignaturaGrado,
                AsignaturaGrado.materia_id
                == materias_resultados_aprendizaje.c.materia_id,
            )
            .outerjoin(
                asignaturas_grado_resultados_aprendizaje,
                and_(
                    asignaturas_grado_resultados_aprendizaje.c.resultado_aprendizaje_id
                    == ResultadoAprendizaje.id,
                    asignaturas_grado_resultados_aprendizaje.c.asignatura_grado_id
                    == asignatura_grado_id,
                ),
            )
            .filter(
                AsignaturaGrado.id == asignatura_grado_id,
                asignaturas_grado_resultados_aprendizaje.c.asignatura_grado_id.is_(
                    None
                ),
            )
            .all()
        )

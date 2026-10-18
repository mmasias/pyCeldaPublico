from sqlalchemy.orm import Session

from app.models.asignatura_programa import AsignaturaPrograma
from app.models.curso_academico import CursoAcademico
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
        codigo: str | None = None,
    ) -> SistemaEvaluacion:
        sistema_evaluacion = SistemaEvaluacion(
            materia_id=materia_id,
            codigo=codigo,
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
        codigo: str | None = None,
    ) -> SistemaEvaluacion:
        sistema_evaluacion.actualizar(
            tipo, descripcion, ponderacion_minima, ponderacion_maxima, codigo
        )
        self.db.commit()
        self.db.refresh(sistema_evaluacion)
        return sistema_evaluacion

    def guias_que_quedarian_fuera_de_rango(
        self,
        materia_id: int,
        sistema_evaluacion_id: int | None,
        ponderacion_minima: float,
        ponderacion_maxima: float,
    ) -> list[str]:
        """Guarda de crear/editar un SistemaEvaluacion (#755): guías del curso
        activo que ya pasaron la validación de ponderaciones (En revisión o
        Aprobada) y con el rango nuevo dejarían de cumplir la regla de
        Guia.bloqueo_ponderaciones() para este sistema -- suma de sus
        ponderaciones vinculadas en [mínima, máxima]. `sistema_evaluacion_id`
        None = sistema nuevo (sin ponderaciones: cuenta como 0 %). Las guías en
        Borrador o Rechazada no cuentan: se vuelven a validar al enviarlas."""
        guias = (
            self.db.query(Guia)
            .join(AsignaturaPrograma, Guia.asignatura_programa_id == AsignaturaPrograma.id)
            .join(CursoAcademico, Guia.curso_academico_id == CursoAcademico.id)
            .filter(
                AsignaturaPrograma.materia_id == materia_id,
                CursoAcademico.estado == "Activo",
                Guia.estado.in_(["EnRevision", "Aprobada"]),
            )
            .all()
        )
        # Mismo redondeo que la columna Numeric(5, 2) en la que se guardará el rango.
        ponderacion_minima = round(ponderacion_minima, 2)
        ponderacion_maxima = round(ponderacion_maxima, 2)
        fuera = []
        for guia in guias:
            asignado = sum(
                float(p.ponderacion)
                for p in guia.ponderaciones
                if p.vinculada and p.sistema_evaluacion_id == sistema_evaluacion_id
            )
            if asignado < ponderacion_minima or asignado > ponderacion_maxima:
                nombre = guia.asignatura_programa.nombre
                fuera.append(f"{nombre} ({asignado:g} %)")
        return sorted(fuera)

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

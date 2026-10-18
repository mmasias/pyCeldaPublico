from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.director_programa import DirectorPrograma
from app.models.facultad import Facultad
from app.models.programa import Programa, programas_directores_programa
from app.models.profesor import Profesor


class ProgramaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_dirigidos_por(self, director_programa_id: int) -> list[Programa]:
        return (
            self.db.query(Programa)
            .join(
                programas_directores_programa,
                programas_directores_programa.c.programa_id == Programa.id,
            )
            .filter(
                programas_directores_programa.c.director_programa_id == director_programa_id
            )
            .all()
        )

    def listar_de_la_facultad(self, facultad_id: int) -> list[Programa]:
        return self.db.query(Programa).filter(Programa.facultad_id == facultad_id).all()

    def obtener(self, programa_id: int) -> Programa | None:
        return self.db.get(Programa, programa_id)

    def universidad_id_de(self, programa_id: int) -> int:
        """Resuelve la Universidad de un Programa vía Facultad (issue #471) --
        los routers que hoy llaman CursoAcademicoRepository.activo() sin
        argumentos pasan por aquí para obtener el universidad_id. Fail
        loud, nunca adivina: si la cadena Programa -> Facultad está rota
        (programa inexistente, sin facultad_id, o la Facultad no existe),
        levanta RuntimeError -- mismo criterio "invariante rota, no
        controlar" que el resto del proyecto (p. ej. "No hay ningún
        CursoAcademico activo"). Nunca cae a una Universidad "por
        defecto"."""
        programa = self.obtener(programa_id)
        if programa is None or programa.facultad_id is None:
            raise RuntimeError(
                f"No se puede resolver la Universidad del Programa {programa_id} "
                "-- inexistente o sin facultad_id"
            )
        facultad = self.db.get(Facultad, programa.facultad_id)
        if facultad is None:
            raise RuntimeError(
                f"Facultad {programa.facultad_id} no encontrada (Programa {programa_id})"
            )
        return facultad.universidad_id

    def obtener_por_codigo(self, codigo: str) -> Programa | None:
        return self.db.query(Programa).filter(Programa.codigo == codigo).one_or_none()

    def dirige(self, programa_id: int, director_programa_id: int) -> bool:
        return (
            self.db.query(programas_directores_programa)
            .filter(
                programas_directores_programa.c.programa_id == programa_id,
                programas_directores_programa.c.director_programa_id == director_programa_id,
            )
            .first()
            is not None
        )

    def crear(self, codigo: str, nombre: str, facultad_id: int) -> Programa:
        programa = Programa(codigo=codigo, nombre=nombre, facultad_id=facultad_id)
        self.db.add(programa)
        self.db.commit()
        self.db.refresh(programa)
        return programa

    def actualizar(self, programa: Programa) -> Programa:
        self.db.commit()
        self.db.refresh(programa)
        return programa

    def contar_dirigidos_por(self, director_programa_id: int) -> int:
        return (
            self.db.query(func.count())
            .select_from(programas_directores_programa)
            .filter(
                programas_directores_programa.c.director_programa_id == director_programa_id
            )
            .scalar()
            or 0
        )

    def contar_directores(self, programa_id: int) -> int:
        return (
            self.db.query(func.count())
            .select_from(programas_directores_programa)
            .filter(programas_directores_programa.c.programa_id == programa_id)
            .scalar()
            or 0
        )

    def listar_directores(self, programa_id: int) -> list[Profesor]:
        """Issue #492: resuelve cada DirectorPrograma del Programa hacia su
        Profesor vía email (nunca DirectorPrograma.id, detalle interno -- ver
        docstring de app/models/director_programa.py). INNER JOIN, no
        outerjoin: todo DirectorPrograma colgado de un Programa tiene, por
        invariante, un Profesor con el mismo email (definir_director_programa()
        lo crea siempre a partir de profesor.email, y
        motivos_bloqueo_eliminacion() impide borrar un Profesor mientras
        dirija algún Programa)."""
        return (
            self.db.query(Profesor)
            .join(DirectorPrograma, DirectorPrograma.email == Profesor.email)
            .join(
                programas_directores_programa,
                programas_directores_programa.c.director_programa_id == DirectorPrograma.id,
            )
            .filter(programas_directores_programa.c.programa_id == programa_id)
            .all()
        )

    def listar_disponibles_para_dirigir(
        self, director_programa_id: int | None
    ) -> list[Programa]:
        if director_programa_id is None:
            return self.db.query(Programa).all()
        return (
            self.db.query(Programa)
            .outerjoin(
                programas_directores_programa,
                and_(
                    programas_directores_programa.c.programa_id == Programa.id,
                    programas_directores_programa.c.director_programa_id
                    == director_programa_id,
                ),
            )
            .filter(programas_directores_programa.c.director_programa_id.is_(None))
            .all()
        )

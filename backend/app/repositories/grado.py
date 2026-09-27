from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.director_grado import DirectorGrado
from app.models.facultad import Facultad
from app.models.grado import Grado, grados_directores_grado
from app.models.profesor import Profesor


class GradoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def listar_dirigidos_por(self, director_grado_id: int) -> list[Grado]:
        return (
            self.db.query(Grado)
            .join(
                grados_directores_grado,
                grados_directores_grado.c.grado_id == Grado.id,
            )
            .filter(
                grados_directores_grado.c.director_grado_id == director_grado_id
            )
            .all()
        )

    def listar_de_la_facultad(self, facultad_id: int) -> list[Grado]:
        return self.db.query(Grado).filter(Grado.facultad_id == facultad_id).all()

    def obtener(self, grado_id: int) -> Grado | None:
        return self.db.get(Grado, grado_id)

    def universidad_id_de(self, grado_id: int) -> int:
        """Resuelve la Universidad de un Grado vía Facultad (issue #471) --
        los routers que hoy llaman CursoAcademicoRepository.activo() sin
        argumentos pasan por aquí para obtener el universidad_id. Fail
        loud, nunca adivina: si la cadena Grado -> Facultad está rota
        (grado inexistente, sin facultad_id, o la Facultad no existe),
        levanta RuntimeError -- mismo criterio "invariante rota, no
        controlar" que el resto del proyecto (p. ej. "No hay ningún
        CursoAcademico activo"). Nunca cae a una Universidad "por
        defecto"."""
        grado = self.obtener(grado_id)
        if grado is None or grado.facultad_id is None:
            raise RuntimeError(
                f"No se puede resolver la Universidad del Grado {grado_id} "
                "-- inexistente o sin facultad_id"
            )
        facultad = self.db.get(Facultad, grado.facultad_id)
        if facultad is None:
            raise RuntimeError(
                f"Facultad {grado.facultad_id} no encontrada (Grado {grado_id})"
            )
        return facultad.universidad_id

    def obtener_por_codigo(self, codigo: str) -> Grado | None:
        return self.db.query(Grado).filter(Grado.codigo == codigo).one_or_none()

    def dirige(self, grado_id: int, director_grado_id: int) -> bool:
        return (
            self.db.query(grados_directores_grado)
            .filter(
                grados_directores_grado.c.grado_id == grado_id,
                grados_directores_grado.c.director_grado_id == director_grado_id,
            )
            .first()
            is not None
        )

    def crear(self, codigo: str, nombre: str, facultad_id: int) -> Grado:
        grado = Grado(codigo=codigo, nombre=nombre, facultad_id=facultad_id)
        self.db.add(grado)
        self.db.commit()
        self.db.refresh(grado)
        return grado

    def actualizar(self, grado: Grado) -> Grado:
        self.db.commit()
        self.db.refresh(grado)
        return grado

    def contar_dirigidos_por(self, director_grado_id: int) -> int:
        return (
            self.db.query(func.count())
            .select_from(grados_directores_grado)
            .filter(
                grados_directores_grado.c.director_grado_id == director_grado_id
            )
            .scalar()
            or 0
        )

    def contar_directores(self, grado_id: int) -> int:
        return (
            self.db.query(func.count())
            .select_from(grados_directores_grado)
            .filter(grados_directores_grado.c.grado_id == grado_id)
            .scalar()
            or 0
        )

    def listar_directores(self, grado_id: int) -> list[Profesor]:
        """Issue #492: resuelve cada DirectorGrado del Grado hacia su
        Profesor vía email (nunca DirectorGrado.id, detalle interno -- ver
        docstring de app/models/director_grado.py). INNER JOIN, no
        outerjoin: todo DirectorGrado colgado de un Grado tiene, por
        invariante, un Profesor con el mismo email (definir_director_grado()
        lo crea siempre a partir de profesor.email, y
        motivos_bloqueo_eliminacion() impide borrar un Profesor mientras
        dirija algún Grado)."""
        return (
            self.db.query(Profesor)
            .join(DirectorGrado, DirectorGrado.email == Profesor.email)
            .join(
                grados_directores_grado,
                grados_directores_grado.c.director_grado_id == DirectorGrado.id,
            )
            .filter(grados_directores_grado.c.grado_id == grado_id)
            .all()
        )

    def listar_disponibles_para_dirigir(
        self, director_grado_id: int | None
    ) -> list[Grado]:
        if director_grado_id is None:
            return self.db.query(Grado).all()
        return (
            self.db.query(Grado)
            .outerjoin(
                grados_directores_grado,
                and_(
                    grados_directores_grado.c.grado_id == Grado.id,
                    grados_directores_grado.c.director_grado_id
                    == director_grado_id,
                ),
            )
            .filter(grados_directores_grado.c.director_grado_id.is_(None))
            .all()
        )

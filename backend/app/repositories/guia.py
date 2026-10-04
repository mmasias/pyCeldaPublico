from sqlalchemy.orm import Session, joinedload, selectinload

from app.models.actividad_formativa_asignatura_programa import (
    ActividadFormativaAsignaturaPrograma,
)
from app.models.asignatura_programa import AsignaturaPrograma
from app.models.guia import Guia
from app.models.materia import Materia
from app.models.ponderacion_evaluacion import PonderacionEvaluacion


class GuiaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def obtener(self, guia_id: int) -> Guia | None:
        return self.db.get(
            Guia,
            guia_id,
            options=[
                joinedload(Guia.asignatura_programa).selectinload(
                    AsignaturaPrograma.resultados_aprendizaje
                ),
                joinedload(Guia.asignatura_programa).selectinload(
                    AsignaturaPrograma.metodologias_docentes
                ),
                # issue #254: profesorado de la plantilla (lo presenta abrir_guia
                # en vivo) e historial (para el banner de re-revisión por
                # profesorado, comentario_revision_por_profesorado).
                joinedload(Guia.asignatura_programa).selectinload(
                    AsignaturaPrograma.profesorado
                ),
                selectinload(Guia.historial),
                # Actividades formativas de la AsignaturaPrograma (sección 4 del
                # render, discussion #227) -- con el nombre del catálogo.
                joinedload(Guia.asignatura_programa)
                .selectinload(AsignaturaPrograma.actividades_formativas)
                .joinedload(ActividadFormativaAsignaturaPrograma.actividad_formativa),
                # Cascada que recorre el render de la guía docente
                # (discussion #218): Materia -> descripcion_propia de cada
                # MetodologiaMateria y Materia.programa para la titulación.
                joinedload(Guia.asignatura_programa)
                .joinedload(AsignaturaPrograma.materia)
                .selectinload(Materia.metodologias_materia),
                selectinload(Guia.ponderaciones).joinedload(
                    PonderacionEvaluacion.sistema_evaluacion
                ),
                selectinload(Guia.referencias),
                selectinload(Guia.profesorado),
                selectinload(Guia.sesiones),
                # issue #433: cabecera del render (guia_docente.py::_contexto())
                # lee guia.curso_academico en vez de Settings.curso_academico_vigente.
                joinedload(Guia.curso_academico),
            ],
        )

    def crear(
        self,
        programa_id: int,
        asignatura_programa_id: int,
        semestre: int | None,
        curso_academico_id: int,
        contenido: str = "",
        sesiones_minimas: int = 25,
    ) -> Guia:
        # Semilla del temario al nacer la Guia: sin Guia del curso anterior
        # (primer curso de esta AsignaturaPrograma), hereda de
        # AsignaturaPrograma.contenido -- 3 niveles Asignatura -> AsignaturaPrograma ->
        # Guia (discussion #191). Copia puntual, no resolución en vivo.
        # sesiones_minimas es el mismo tipo de snapshot (discussion #206).
        # curso_academico_id (issue #433, columna NOT NULL): el CursoAcademico
        # Activo en el momento de crear la AsignaturaPrograma -- lo resuelve el
        # llamador vía CursoAcademicoRepository.activo().
        guia = Guia(
            estado="Borrador",
            semestre=semestre,
            contenido=contenido,
            sesiones_minimas=sesiones_minimas,
            programa_id=programa_id,
            asignatura_programa_id=asignatura_programa_id,
            curso_academico_id=curso_academico_id,
        )
        self.db.add(guia)
        self.db.commit()
        self.db.refresh(guia)
        return guia

    def actualizar(self, guia: Guia) -> Guia:
        self.db.commit()
        self.db.refresh(guia)
        return guia

    def listar_del_programa(self, programa_id: int, curso_academico_id: int) -> list[Guia]:
        """issue #441: curso_academico_id obligatorio -- sin él, con 2+
        CursoAcademico reales, consultarEstadoGuias() mezclaría guías de
        varios años en la misma tabla sin columna que diga a cuál pertenece
        cada una. El llamador resuelve qué curso (activo por defecto, o el
        pedido vía ?curso=) antes de llamar."""
        return (
            self.db.query(Guia)
            .filter_by(programa_id=programa_id, curso_academico_id=curso_academico_id)
            .options(
                # issue #254: el listado presenta el profesorado de la plantilla
                # en vivo (no la copia guia.profesorado) e historial para
                # ultima_actualizacion_rol (que gana el valor "Administración").
                joinedload(Guia.asignatura_programa).selectinload(
                    AsignaturaPrograma.profesorado
                ),
                selectinload(Guia.historial),
            )
            .all()
        )

    def obtener_por_asignatura_programa(
        self, asignatura_programa_id: int, curso_academico_id: int
    ) -> Guia | None:
        """issue #440: curso_academico_id obligatorio, no opcional -- sin él,
        con 2+ CursoAcademico reales, .first() sin orden podría devolver la
        Guia de un curso equivocado (mecanismo de #254: reenviaría a
        EnRevision la guía del año que no toca). one_or_none() en vez de
        first(): a lo sumo una Guia por (AsignaturaPrograma, CursoAcademico)
        por construcción (crear_asignatura_programa()/activar()) -- si alguna
        vez hubiera dos, es un bug real que debe fallar alto, no elegir en
        silencio."""
        return (
            self.db.query(Guia)
            .filter_by(
                asignatura_programa_id=asignatura_programa_id,
                curso_academico_id=curso_academico_id,
            )
            .one_or_none()
        )

    def listar_por_asignaturas_programa(
        self, asignatura_programa_ids: list[int], curso_academico_id: int
    ) -> list[Guia]:
        """issue #440: curso_academico_id obligatorio -- método compartido
        entre listar_mis_asignaturas_programa() y
        listar_asignaturas_programa_del_programa() (routers/asignatura_programa.py),
        cada uno resuelve el CursoAcademico activo una sola vez por
        request. Sin el filtro, con 2+ CursoAcademico reales, el diccionario
        `asignatura_programa_id -> Guia` que arman los routers se quedaría con
        una guía arbitraria por AsignaturaPrograma (la última que iterase SQL),
        no la del curso vigente."""
        if not asignatura_programa_ids:
            return []
        return (
            self.db.query(Guia)
            .filter(
                Guia.asignatura_programa_id.in_(asignatura_programa_ids),
                Guia.curso_academico_id == curso_academico_id,
            )
            .all()
        )

    def listar_aprobadas_de_asignaturas_programa(
        self, asignatura_programa_ids: list[int], curso_academico_id: int
    ) -> list[Guia]:
        """Guías Aprobadas de un conjunto de AsignaturaPrograma (issue #184: las
        hermanas de la guía destino). issue #443: curso_academico_id
        obligatorio, no opcional -- importar de guía hermana es una acción
        de escritura (reemplaza contenido real de la Guia destino), así que
        el listado de orígenes importables es deliberadamente estrecho:
        solo el CursoAcademico activo, sin selector ?curso= (a diferencia
        de #441/#442, que son de solo lectura y sí navegan por cursos).
        Sin el filtro, con 2+ CursoAcademico reales, la Aprobada del año
        anterior aparecería como origen importable y el POST la aceptaría
        como válida. Precarga referencias, sesiones, historial y el
        catálogo Asignatura de cada una -- lo necesita el listado de
        orígenes importables (recuentos, fecha de aprobación, código de
        asignatura) y la copia posterior."""
        if not asignatura_programa_ids:
            return []
        return (
            self.db.query(Guia)
            .filter(
                Guia.asignatura_programa_id.in_(asignatura_programa_ids),
                Guia.estado == "Aprobada",
                Guia.curso_academico_id == curso_academico_id,
            )
            .options(
                selectinload(Guia.referencias),
                selectinload(Guia.sesiones),
                selectinload(Guia.historial),
                joinedload(Guia.asignatura_programa).joinedload(
                    AsignaturaPrograma.asignatura
                ),
            )
            .all()
        )

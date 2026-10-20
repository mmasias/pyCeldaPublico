import math
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, DateTimeUTC
from app.models.plantilla_evaluacion import (
    LIMITE_INSTRUMENTO_EXTRAORDINARIO,
    componer_texto_convocatorias,
    es_plantilla,
    plantilla_por_caracter,
    usa_campos_extraordinaria,
)

if TYPE_CHECKING:
    from app.models.asignatura_programa import AsignaturaPrograma
    from app.models.curso_academico import CursoAcademico
    from app.models.historial_cambio import HistorialCambio
    from app.models.ponderacion_evaluacion import PonderacionEvaluacion
    from app.models.profesor import Profesor
    from app.models.referencia_bibliografica import ReferenciaBibliografica
    from app.models.sesion import Sesion


# issue #254: la transición Aprobada -> EnRevision que dispara el Admin al
# cambiar el profesorado de la AsignaturaPrograma se registra en HistorialCambio
# con este autor centinela (ningún Profesor/Admin real tiene id 0) y este
# comentario fijo, que además es el texto del banner en la guía.
AUTOR_ADMIN_CENTINELA = 0
COMENTARIO_REVISION_POR_PROFESORADO = (
    "En revisión por cambio en los profesores que la imparten"
)

# Discussion #731 (opción A, sin cambio de esquema): HistorialCambio no guarda
# el rol del autor y los id de Profesor y DirectorPrograma son de tablas
# distintas, así que la autoría de las filas que marcan quién tocó la guía se
# distingue como la de Administración, por un valor fijo:
# - el Profesor que edita una guía Aprobada deja una fila campo="estado"
#   (Aprobada -> Borrador) con COMENTARIO_EDICION_PROFESOR;
# - el Director que corrige una guía en Borrador o Rechazada (sin transición de
#   estado) deja una fila campo=CAMPO_CORRECCION_DIRECTOR.
# La mejora limpia (opción B) es una columna de rol en HistorialCambio, con
# subida de esquema.
COMENTARIO_EDICION_PROFESOR = "edición del Profesor sobre la guía aprobada"
COMENTARIO_CORRECCION_DIRECTOR = "corrección directa del Director"
CAMPO_CORRECCION_DIRECTOR = "correccion_director"


COMENTARIOS_RESERVADOS = (COMENTARIO_EDICION_PROFESOR, COMENTARIO_CORRECCION_DIRECTOR)


def es_edicion_del_profesor(
    campo: str, valor_anterior: str | None, valor_nuevo: str | None, comentario: str | None
) -> bool:
    """Fila de estado Aprobada -> Borrador que deja el Profesor al editar una
    guía aprobada (no es una revocación del Director). El comentario es texto
    libre en rechazar/revocar: esos endpoints rechazan COMENTARIOS_RESERVADOS
    para que un Director no pueda dejar una fila que pase por esta."""
    return (
        campo == "estado"
        and valor_anterior == "Aprobada"
        and valor_nuevo == "Borrador"
        and comentario == COMENTARIO_EDICION_PROFESOR
    )


def _es_edicion_del_profesor(cambio: "HistorialCambio") -> bool:
    return es_edicion_del_profesor(
        cambio.campo, cambio.valor_anterior, cambio.valor_nuevo, cambio.comentario
    )

# Tope de longitud de Guia.contenido (issue #303, hallazgo H-12). Criterio:
# ~2x el máximo real de producción (4.801 caracteres, 108 guías medidas),
# redondeado. Un temario más largo es señal de un pegado accidental que no
# debe llegar al PDF oficial ni a la BD. No hay migración: ninguna guía viva
# lo supera.
LIMITE_CONTENIDO_GUIA = 10_000


guias_profesores = Table(
    "guias_profesores",
    Base.metadata,
    Column("guia_id", ForeignKey("guias.id"), primary_key=True),
    Column("profesor_id", ForeignKey("profesores.id"), primary_key=True),
)


class Guia(Base):
    __tablename__ = "guias"

    id: Mapped[int] = mapped_column(primary_key=True)
    estado: Mapped[str] = mapped_column(String(20), default="Borrador")
    semestre: Mapped[int | None] = mapped_column(nullable=True)
    contenido: Mapped[str] = mapped_column(Text, default="")
    # issue #791 (Patrón B, como contenido/ponderaciones/sesiones): el texto de
    # convocatorias del apartado 5 sale de una plantilla (plantilla_evaluacion.py)
    # con dos campos que la personalizan; nadie lo edita. NULL = la plantilla
    # que corresponde al carácter de la AsignaturaPrograma (ver la propiedad
    # plantilla_evaluacion). activar_curso_academico() clona los tres de la
    # Guia previa.
    plantilla_evaluacion_elegida: Mapped[str | None] = mapped_column(
        "plantilla_evaluacion", String(30), nullable=True
    )
    instrumento_extraordinario: Mapped[str | None] = mapped_column(
        String(300), nullable=True
    )
    porcentaje_recuperable: Mapped[int | None] = mapped_column(nullable=True)
    # Snapshot de AsignaturaPrograma.sesiones_minimas al nacer la Guia (como
    # semestre y contenido -- discussion #206). El mínimo de Sesion vinculadas
    # que exige planificacion_docente_completa() antes de enviar a revisión.
    sesiones_minimas: Mapped[int] = mapped_column(default=25)
    programa_id: Mapped[int | None] = mapped_column(nullable=True)
    asignatura_programa_id: Mapped[int | None] = mapped_column(
        ForeignKey("asignaturas_programa.id"), nullable=True
    )
    # issue #433: el dato siempre existió implícitamente (nunca hubo más de
    # un CursoAcademico en juego), así que a diferencia de las columnas
    # nullable-sin-backfill del proyecto (ORCID, fecha_creacion...) esta nace
    # NOT NULL desde el primer día -- la migración retroactiva backfillea
    # TODAS las Guia existentes contra un único CursoAcademico "2026-2027",
    # sin estado transitorio con NULL permitido (decisión de Manuel,
    # discussion #430).
    curso_academico_id: Mapped[int] = mapped_column(
        ForeignKey("cursos_academicos.id"), nullable=False
    )
    # Nullable, sin backfill (discussion #227, gap de Desarrollo sobre un
    # atributo que modeloDominio.puml y el wireframe de abrirGuia() ya
    # declaraban desde L7): las 108 guías creadas antes de esta columna no
    # tienen ese dato real -- se quedan en NULL, no en una fecha inventada.
    # Las altas nuevas la reciben del default, GuiaRepository.crear() no la
    # pasa explícita.
    fecha_creacion: Mapped[datetime | None] = mapped_column(
        DateTimeUTC, default=lambda: datetime.now(UTC), nullable=True
    )
    fecha_ultima_modificacion: Mapped[datetime] = mapped_column(
        DateTimeUTC, default=lambda: datetime.now(UTC)
    )
    fecha_generacion_pdf: Mapped[datetime | None] = mapped_column(
        DateTimeUTC, nullable=True
    )

    ponderaciones: Mapped[list["PonderacionEvaluacion"]] = relationship(
        back_populates="guia"
    )
    referencias: Mapped[list["ReferenciaBibliografica"]] = relationship(
        back_populates="guia"
    )
    sesiones: Mapped[list["Sesion"]] = relationship(back_populates="guia")
    historial: Mapped[list["HistorialCambio"]] = relationship(back_populates="guia")
    asignatura_programa: Mapped["AsignaturaPrograma | None"] = relationship(
        back_populates="guias"
    )
    # issue #454: back_populates hacia CursoAcademico.guias (la inversa ya
    # estaba declarada en el modelo nuevo) -- cierra la relación bidireccional
    # que necesita CursoAcademico.tiene_guia_asociada().
    curso_academico: Mapped["CursoAcademico"] = relationship(
        back_populates="guias"
    )
    profesorado: Mapped[list["Profesor"]] = relationship(secondary=guias_profesores)

    @property
    def asignatura_programa_nombre(self) -> str | None:
        return self.asignatura_programa.nombre if self.asignatura_programa else None

    @property
    def asignatura_programa_curso(self) -> int | None:
        return self.asignatura_programa.curso if self.asignatura_programa else None

    @property
    def asignatura_programa_semestre_default(self) -> int | None:
        return self.asignatura_programa.semestre_default if self.asignatura_programa else None

    @property
    def plantilla_evaluacion(self) -> str:
        """Plantilla del texto de convocatorias que se aplica: la elegida o,
        si no se ha elegido, la del carácter de la AsignaturaPrograma (#791).
        Un código que ya no existe (dato tocado a mano, plantilla retirada)
        cae también en la del carácter: la guía no deja de abrirse."""
        if es_plantilla(self.plantilla_evaluacion_elegida):
            return self.plantilla_evaluacion_elegida
        return plantilla_por_caracter(
            self.asignatura_programa.caracter if self.asignatura_programa else None
        )

    @property
    def texto_convocatorias(self) -> str:
        """Texto del apartado 5 con los campos sustituidos y el marcador
        [TABLA] donde va la tabla de ponderaciones."""
        return componer_texto_convocatorias(
            self.plantilla_evaluacion,
            self.instrumento_extraordinario,
            self.porcentaje_recuperable,
        )

    def bloqueo_convocatoria(self) -> str | None:
        """Regla c4 de enviarGuiaARevision (#791): si la plantilla tiene los
        campos de la convocatoria extraordinaria, los dos están rellenos.
        Motivo concreto o None si no bloquea."""
        if not usa_campos_extraordinaria(self.plantilla_evaluacion):
            return None
        faltan = []
        if not self.instrumento_extraordinario:
            faltan.append("el instrumento")
        if self.porcentaje_recuperable is None:
            faltan.append("el porcentaje recuperable")
        if not faltan:
            return None
        return f"Convocatoria extraordinaria sin concretar: falta {' y '.join(faltan)}"

    def _instrumentos_evaluacion_final(self) -> list["PonderacionEvaluacion"]:
        return [
            p
            for p in self.ponderaciones
            if p.vinculada
            and p.sistema_evaluacion is not None
            and (p.sistema_evaluacion.tipo or "").strip().lower() == "evaluación final"
        ]

    @property
    def instrumento_extraordinario_sugerido(self) -> str | None:
        """Propuesta para el instrumento: los instrumentos vinculados de los
        sistemas de tipo "Evaluación final", en una redacción que no depende
        del género de su nombre. None si no hay ninguno."""
        nombres = [p.descripcion for p in self._instrumentos_evaluacion_final()]
        if not nombres:
            return None
        if len(nombres) == 1:
            propuesta = f"la prueba de evaluación final ({nombres[0]})"
        else:
            propuesta = (
                "las pruebas de evaluación final ("
                + ", ".join(nombres[:-1])
                + f" y {nombres[-1]})"
            )
        # Que la propuesta se pueda guardar tal cual: sin los nombres si no cabe.
        if len(propuesta) > LIMITE_INSTRUMENTO_EXTRAORDINARIO:
            return propuesta.split(" (")[0]
        return propuesta

    @property
    def porcentaje_recuperable_sugerido(self) -> int | None:
        """Propuesta para el porcentaje: la suma de los instrumentos de
        evaluación final, redondeada a entero. None si no hay ninguno."""
        instrumentos = self._instrumentos_evaluacion_final()
        if not instrumentos:
            return None
        # Redondeo aritmético (50,5 -> 51), no el del banquero de round().
        suma = math.floor(sum(float(p.ponderacion) for p in instrumentos) + 0.5)
        # Solo si se puede guardar tal cual (1-100).
        return suma if 1 <= suma <= 100 else None

    def _ultimo_cambio_historial(self) -> "HistorialCambio | None":
        # Solo las filas que dicen quién tocó la guía cuentan para la autoría:
        # las transiciones de estado (aprobar/rechazar/escalar/revocar, la del
        # Profesor que edita una aprobada y la administrativa de #254) y la
        # corrección del Director sin transición (#731). Las filas de contenido
        # no: su autor_id no dice de qué tabla sale.
        cambios = [
            h for h in self.historial if h.campo in ("estado", CAMPO_CORRECCION_DIRECTOR)
        ]
        if not cambios:
            return None
        return max(cambios, key=lambda h: (h.fecha, h.id or 0))

    @property
    def ultima_actualizacion(self) -> datetime:
        """Máximo entre guardar-borrador (campo propio del modelo) y las filas
        de autoría de HistorialCambio -- ninguna de las dos señales por separado
        cubre el ciclo de vida completo (enviarARevision no toca
        ninguna). Documentado como simplificación conocida, no oculta."""
        ultimo_historial = self._ultimo_cambio_historial()
        if ultimo_historial is not None and ultimo_historial.fecha > self.fecha_ultima_modificacion:
            return ultimo_historial.fecha
        return self.fecha_ultima_modificacion

    @property
    def ultima_actualizacion_rol(self) -> str:
        # >= y no >: una escritura deja su fila de autoría con la misma fecha
        # que pone en fecha_ultima_modificacion (#731,
        # aplicar_regla_de_estado_por_escritura); con > esa fila no contaría.
        ultimo_historial = self._ultimo_cambio_historial()
        if ultimo_historial is not None and ultimo_historial.fecha >= self.fecha_ultima_modificacion:
            # issue #254: la transición Aprobada -> EnRevision administrativa
            # es campo="estado" pero no la hace el Director -- el autor centinela
            # la distingue para no atribuírsela.
            if ultimo_historial.autor_id == AUTOR_ADMIN_CENTINELA:
                return "Administración"
            if _es_edicion_del_profesor(ultimo_historial):
                return "Profesor"
            return "Director"
        return "Profesor"

    @property
    def comentario_revision_por_profesorado(self) -> str | None:
        """Banner de la guía cuando volvió a EnRevisión porque el Admin cambió
        el profesorado de la AsignaturaPrograma (issue #254). Misma mecánica que
        comentario_rechazo/comentario_revocacion: lee la última transición de
        estado y expone su comentario, aquí acotado a la transición
        Aprobada -> EnRevisión con el autor centinela."""
        if self.estado != "EnRevision":
            return None
        ultimo = self._ultimo_cambio_historial()
        if ultimo is None:
            return None
        if (
            ultimo.valor_anterior == "Aprobada"
            and ultimo.valor_nuevo == "EnRevision"
            and ultimo.autor_id == AUTOR_ADMIN_CENTINELA
        ):
            return ultimo.comentario
        return None

    @property
    def comentario_rechazo(self) -> str | None:
        if self.estado != "Rechazada":
            return None
        rechazos = [
            h for h in self.historial if h.campo == "estado" and h.valor_nuevo == "Rechazada"
        ]
        if not rechazos:
            return None
        return max(rechazos, key=lambda h: h.fecha).comentario

    @property
    def comentario_revocacion(self) -> str | None:
        if self.estado != "Borrador":
            return None
        revocaciones = [
            h for h in self.historial if h.campo == "estado" and h.valor_nuevo == "Borrador"
        ]
        if not revocaciones:
            return None
        ultima = max(revocaciones, key=lambda h: (h.fecha, h.id or 0))
        # #731: si la guía volvió a Borrador porque el Profesor la editó, no
        # hay comentario del Director que mostrar (ni el de una revocación de
        # un ciclo anterior).
        if _es_edicion_del_profesor(ultima):
            return None
        return ultima.comentario

    def sincronizar_ponderaciones(
        self, ids_ponderaciones_final: list[int]
    ) -> tuple[list[int], list[int]]:
        todas_las_de_la_guia = {p.id for p in self.ponderaciones}
        vinculadas_actuales = {p.id for p in self.ponderaciones if p.vinculada}
        # Intersección con todas_las_de_la_guia (issue #210): un id inexistente
        # o de otra Guia en el body de PUT /guias/{id}/borrador no debe llegar
        # a vincular() -- se ignora en vez de provocar 500 o mutar una fila ajena.
        deseadas = set(ids_ponderaciones_final) & todas_las_de_la_guia
        a_vincular = list(deseadas - vinculadas_actuales)
        a_desvincular = list(todas_las_de_la_guia - deseadas)
        return a_vincular, a_desvincular

    def sincronizar_referencias(
        self, ids_referencias_final: list[int]
    ) -> tuple[list[int], list[int]]:
        todas_las_de_la_guia = {r.id for r in self.referencias}
        vinculadas_actuales = {r.id for r in self.referencias if r.vinculada}
        # Ver comentario en sincronizar_ponderaciones (issue #210).
        deseadas = set(ids_referencias_final) & todas_las_de_la_guia
        a_vincular = list(deseadas - vinculadas_actuales)
        a_desvincular = list(todas_las_de_la_guia - deseadas)
        return a_vincular, a_desvincular

    def sincronizar_sesiones(
        self, ids_sesiones_final: list[int]
    ) -> tuple[list[int], list[int]]:
        todas_las_de_la_guia = {s.id for s in self.sesiones}
        vinculadas_actuales = {s.id for s in self.sesiones if s.vinculada}
        # Ver comentario en sincronizar_ponderaciones (issue #210).
        deseadas = set(ids_sesiones_final) & todas_las_de_la_guia
        a_vincular = list(deseadas - vinculadas_actuales)
        a_desvincular = list(todas_las_de_la_guia - deseadas)
        return a_vincular, a_desvincular

    @staticmethod
    def contenido_dentro_del_limite(contenido: str) -> bool:
        """Regla de negocio de #303: el temario no puede pasar de
        LIMITE_CONTENIDO_GUIA caracteres. El router traduce el False a un 422
        con mensaje legible."""
        return len(contenido) <= LIMITE_CONTENIDO_GUIA

    def actualizar_contenido(self, contenido: str) -> str | None:
        """Aplica el temario que el Profesor redacta y mantiene cada curso.
        Devuelve el valor anterior si el texto cambió (para registrar la fila de
        HistorialCambio), o None si llega igual -- el historial arranca con la
        primera acción humana real, no con un guardado que no toca nada."""
        if contenido == self.contenido:
            return None
        anterior = self.contenido
        self.contenido = contenido
        return anterior

    def confirmar_guardado(self, ahora: datetime | None = None) -> None:
        self.fecha_ultima_modificacion = ahora or datetime.now(UTC)
        if self.estado == "Aprobada":
            self.estado = "Borrador"

    def bloqueo_ponderaciones(self) -> str | None:
        """Motivo concreto por el que la parte de PonderacionEvaluacion (regla
        c2 de enviarGuiaARevision) bloquea el envío, o None si no bloquea.
        Recorre TODOS los SistemaEvaluacion de la materia -- no solo los que ya
        tienen alguna ponderación vinculada -- tratando como 0% el que no
        tiene ninguna. Un sistema con ponderacion_minima == 0 no bloquea en 0%:
        el rango [0, maxima] lo admite sin caso especial. Antes (issue #208) el
        rango solo se validaba para los sistemas presentes en `vinculadas`, así
        que un sistema requerido en 0% se colaba sin marcar error."""
        vinculadas = [p for p in self.ponderaciones if p.vinculada]
        if not vinculadas:
            return "Rango por sistema de evaluación o suma total incorrectos"
        if sum(float(p.ponderacion) for p in vinculadas) != 100:
            return "Rango por sistema de evaluación o suma total incorrectos"
        por_sistema: dict[int, float] = {}
        for p in vinculadas:
            por_sistema[p.sistema_evaluacion_id] = (
                por_sistema.get(p.sistema_evaluacion_id, 0) + float(p.ponderacion)
            )
        for sistema in self.asignatura_programa.materia.sistemas_evaluacion:
            asignado = por_sistema.get(sistema.id, 0.0)
            minima = float(sistema.ponderacion_minima)
            maxima = float(sistema.ponderacion_maxima)
            if asignado < minima:
                return (
                    f"Falta asignar {minima - asignado:g}% en {sistema.etiqueta()} "
                    f"(mínimo {minima:g}%, asignado {asignado:g}%)"
                )
            if asignado > maxima:
                return (
                    f"Sobra {asignado - maxima:g}% en {sistema.etiqueta()} "
                    f"(máximo {maxima:g}%, asignado {asignado:g}%)"
                )
        return None

    def puede_enviarse_a_revision(self) -> bool:
        return self.bloqueo_ponderaciones() is None

    def sesiones_vinculadas_count(self) -> int:
        return len([s for s in self.sesiones if s.vinculada])

    def planificacion_docente_completa(self) -> bool:
        """Regla c3 de enviarGuiaARevision (discussion #206): la planificación
        docente tiene al menos `sesiones_minimas` Sesion vinculadas. De la misma
        familia agregada que la suma de PonderacionEvaluacion = 100%."""
        return self.sesiones_vinculadas_count() >= self.sesiones_minimas

    def planificacion_docente_vacia(self) -> bool:
        """Precondición de generarPlanificacionDocenteGenerica() (familia del
        issue #184): la planificación docente no tiene ninguna Sesion, ni
        vinculada ni pendiente. Una Guia con la planificación vacía nunca puede
        estar Aprobada -- la regla c3 lo impide."""
        return not self.sesiones

    def enviar_a_revision(self) -> None:
        self.estado = "EnRevision"

    def _sincronizar_profesorado(self) -> None:
        # issue #254: Guia -- Profesor es una copia que se re-deriva de la
        # plantilla AsignaturaPrograma -- Profesor en cada aprobación de la guía
        # activa (misma familia que Guia.contenido: un mantenedor y un ciclo de
        # re-aprobación). Si la Guia no tiene AsignaturaPrograma (columna nullable),
        # no hay plantilla de la que copiar y la copia se queda como está.
        if self.asignatura_programa is not None:
            self.profesorado = list(self.asignatura_programa.profesorado)

    def aprobar(self) -> None:
        # regenerar_pdf() como parte del propio cambio de estado (discussion
        # #224, cierre de Frente B): aprobar pasa a ser el disparador real de
        # "PDF descargable" -- el PDF siempre se re-renderiza en vivo desde
        # esta fila, no hay artefacto que "generar" de verdad.
        self.estado = "Aprobada"
        self.regenerar_pdf()
        self._sincronizar_profesorado()

    def rechazar(self) -> None:
        self.estado = "Rechazada"

    def escalar_a_aprobada(self) -> str:
        estado_anterior = self.estado
        self.estado = "Aprobada"
        self.regenerar_pdf()
        self._sincronizar_profesorado()
        return estado_anterior

    def revocar_aprobacion(self) -> None:
        self.estado = "Borrador"

    def regenerar_pdf(self) -> None:
        if self.estado == "Aprobada":
            self.fecha_generacion_pdf = datetime.now(UTC)

    def tiene_pdf_generado(self) -> bool:
        return self.fecha_generacion_pdf is not None

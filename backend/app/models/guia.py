from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, DateTimeUTC

if TYPE_CHECKING:
    from app.models.asignatura_grado import AsignaturaGrado
    from app.models.curso_academico import CursoAcademico
    from app.models.historial_cambio import HistorialCambio
    from app.models.ponderacion_evaluacion import PonderacionEvaluacion
    from app.models.profesor import Profesor
    from app.models.referencia_bibliografica import ReferenciaBibliografica
    from app.models.sesion import Sesion


# issue #254: la transición Aprobada -> EnRevision que dispara el Admin al
# cambiar el profesorado de la AsignaturaGrado se registra en HistorialCambio
# con este autor centinela (ningún Profesor/Admin real tiene id 0) y este
# comentario fijo, que además es el texto del banner en la guía.
AUTOR_ADMIN_CENTINELA = 0
COMENTARIO_REVISION_POR_PROFESORADO = (
    "En revisión por cambio en los profesores que la imparten"
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
    # Snapshot de AsignaturaGrado.sesiones_minimas al nacer la Guia (como
    # semestre y contenido -- discussion #206). El mínimo de Sesion vinculadas
    # que exige planificacion_docente_completa() antes de enviar a revisión.
    sesiones_minimas: Mapped[int] = mapped_column(default=25)
    grado_id: Mapped[int | None] = mapped_column(nullable=True)
    asignatura_grado_id: Mapped[int | None] = mapped_column(
        ForeignKey("asignaturas_grado.id"), nullable=True
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
    asignatura_grado: Mapped["AsignaturaGrado | None"] = relationship(
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
    def asignatura_grado_nombre(self) -> str | None:
        return self.asignatura_grado.nombre if self.asignatura_grado else None

    @property
    def asignatura_grado_curso(self) -> int | None:
        return self.asignatura_grado.curso if self.asignatura_grado else None

    @property
    def asignatura_grado_semestre_default(self) -> int | None:
        return self.asignatura_grado.semestre_default if self.asignatura_grado else None

    def _ultimo_cambio_historial(self) -> "HistorialCambio | None":
        # Solo las transiciones de estado son señal de "el Director tocó esto"
        # (aprobar/rechazar/escalar/revocar). Las filas campo="contenido" son
        # ediciones del Profesor, ya cubiertas por fecha_ultima_modificacion vía
        # confirmar_guardado() -- no deben desplazar la autoría al Director.
        cambios_estado = [h for h in self.historial if h.campo == "estado"]
        if not cambios_estado:
            return None
        return max(cambios_estado, key=lambda h: h.fecha)

    @property
    def ultima_actualizacion(self) -> datetime:
        """Máximo entre guardar-borrador (Profesor, campo propio del modelo) y
        aprobar/rechazar/escalar/revocar (Director, vía HistorialCambio) --
        ninguna de las dos señales por separado cubre el ciclo de vida
        completo (enviarARevision y editarSemestreGuia no tocan ninguna).
        Documentado como simplificación conocida, no oculta."""
        ultimo_historial = self._ultimo_cambio_historial()
        if ultimo_historial is not None and ultimo_historial.fecha > self.fecha_ultima_modificacion:
            return ultimo_historial.fecha
        return self.fecha_ultima_modificacion

    @property
    def ultima_actualizacion_rol(self) -> str:
        ultimo_historial = self._ultimo_cambio_historial()
        if ultimo_historial is not None and ultimo_historial.fecha > self.fecha_ultima_modificacion:
            # issue #254: la transición Aprobada -> EnRevision administrativa
            # es campo="estado" pero no la hace el Director -- el autor centinela
            # la distingue para no atribuírsela.
            if ultimo_historial.autor_id == AUTOR_ADMIN_CENTINELA:
                return "Administración"
            return "Director"
        return "Profesor"

    @property
    def comentario_revision_por_profesorado(self) -> str | None:
        """Banner de la guía cuando volvió a EnRevisión porque el Admin cambió
        el profesorado de la AsignaturaGrado (issue #254). Misma mecánica que
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
        return max(revocaciones, key=lambda h: h.fecha).comentario

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

    def confirmar_guardado(self) -> None:
        self.fecha_ultima_modificacion = datetime.now(UTC)
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
        for sistema in self.asignatura_grado.materia.sistemas_evaluacion:
            asignado = por_sistema.get(sistema.id, 0.0)
            minima = float(sistema.ponderacion_minima)
            maxima = float(sistema.ponderacion_maxima)
            if asignado < minima:
                return (
                    f"Falta asignar {minima - asignado:g}% en {sistema.tipo} "
                    f"(mínimo {minima:g}%, asignado {asignado:g}%)"
                )
            if asignado > maxima:
                return (
                    f"Sobra {asignado - maxima:g}% en {sistema.tipo} "
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
        # plantilla AsignaturaGrado -- Profesor en cada aprobación de la guía
        # activa (misma familia que Guia.contenido: un mantenedor y un ciclo de
        # re-aprobación). Si la Guia no tiene AsignaturaGrado (columna nullable),
        # no hay plantilla de la que copiar y la copia se queda como está.
        if self.asignatura_grado is not None:
            self.profesorado = list(self.asignatura_grado.profesorado)

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

    def actualizar_semestre(self, semestre: int) -> None:
        self.semestre = semestre

    def regenerar_pdf(self) -> None:
        if self.estado == "Aprobada":
            self.fecha_generacion_pdf = datetime.now(UTC)

    def tiene_pdf_generado(self) -> bool:
        return self.fecha_generacion_pdf is not None

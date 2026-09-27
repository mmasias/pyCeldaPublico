from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.guia import Guia
from app.models.sesion import Sesion


class SesionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def crear(self, guia_id: int, numero: int, tipo: str, descripcion: str) -> Sesion:
        sesion = Sesion(
            guia_id=guia_id,
            numero=numero,
            tipo=tipo,
            descripcion=descripcion,
        )
        self.db.add(sesion)
        self.db.commit()
        self.db.refresh(sesion)
        return sesion

    def siguiente_numero(self, guia_id: int) -> int:
        return (
            self.db.query(func.coalesce(func.max(Sesion.numero), 0) + 1)
            .filter(Sesion.guia_id == guia_id)
            .scalar()
        )

    def obtener(self, sesion_id: int) -> Sesion | None:
        return self.db.get(Sesion, sesion_id)

    def actualizar(self, sesion: Sesion) -> Sesion:
        self.db.commit()
        self.db.refresh(sesion)
        return sesion

    def listar_vinculadas_de(self, guia: Guia) -> list[Sesion]:
        return [s for s in guia.sesiones if s.vinculada]

    def listar_pendientes_de(self, guia_id: int) -> list[Sesion]:
        return (
            self.db.query(Sesion)
            .filter_by(guia_id=guia_id, vinculada=False)
            .all()
        )

    def existe_pendiente_de(self, guia_id: int) -> bool:
        return (
            self.db.query(Sesion)
            .filter_by(guia_id=guia_id, vinculada=False)
            .first()
            is not None
        )

    def reemplazar_desde(
        self, guia_destino: Guia, sesiones_origen: list[Sesion]
    ) -> list[Sesion]:
        """Issue #184: borra TODAS las Sesion de la guía destino y crea copias
        de las de origen renumeradas 1..N en persistencia (orden por el
        `numero` del origen), replicando tipo, descripcion y el flag
        `vinculada` fila a fila. A diferencia de eliminarSesion() -- que
        renumera solo en presentación -- aquí las filas son nuevas y 1..N es su
        valor de alta. NO toca Guia.sesiones_minimas. Borrado vía ORM (recorre
        la colección ya cargada). NO hace commit -- transacción atómica del
        handler de importación."""
        for sesion in list(guia_destino.sesiones):
            self.db.delete(sesion)
        self.db.flush()
        copias = [
            Sesion(
                guia_id=guia_destino.id,
                numero=numero,
                tipo=origen.tipo,
                descripcion=origen.descripcion,
                vinculada=origen.vinculada,
            )
            for numero, origen in enumerate(
                sorted(sesiones_origen, key=lambda s: s.numero), start=1
            )
        ]
        self.db.add_all(copias)
        self.db.flush()
        return copias

    def generar_genericas(self, guia: Guia, cantidad: int) -> list[Sesion]:
        """Familia del issue #184 (arranque en bloque, gemelo de
        reemplazar_desde() pero sin borrado previo -- la precondición
        planificacion_docente_vacia() garantiza que no hay nada que borrar):
        crea `cantidad` Sesion planas CLASE_TEORICA sin descripcion, vinculadas
        directo (acción de arranque, no edición incremental -- cuentan para el
        medidor desde ya), numeradas 1..cantidad EN PERSISTENCIA. NO hace commit
        -- transacción atómica del handler."""
        genericas = [
            Sesion(
                guia_id=guia.id,
                numero=numero,
                tipo="CLASE_TEORICA",
                descripcion="",
                vinculada=True,
            )
            for numero in range(1, cantidad + 1)
        ]
        self.db.add_all(genericas)
        self.db.flush()
        return genericas

    def duplicar(self, sesion_id: int) -> Sesion:
        """Issue #364: inserta una copia de `tipo`+`descripcion` justo
        después del origen, renumerando +1 las sesiones posteriores de la
        misma guía -- primera pieza de "insertar en medio" (acotada: solo
        justo después de X, no reordenamiento general). `Sesion.numero` no
        tiene índice único (confirmado en el issue), así que el orden en que
        se renumera dentro de la transacción es indiferente. Todo en una
        única transacción -- si falla a mitad no queda semi-renumerado.
        Mismo criterio que crear(): no fija `vinculada` explícitamente,
        queda en su default."""
        origen = self.obtener(sesion_id)
        posteriores = (
            self.db.query(Sesion)
            .filter(Sesion.guia_id == origen.guia_id, Sesion.numero > origen.numero)
            .all()
        )
        for sesion in posteriores:
            sesion.numero += 1
        copia = Sesion(
            guia_id=origen.guia_id,
            numero=origen.numero + 1,
            tipo=origen.tipo,
            descripcion=origen.descripcion,
        )
        self.db.add(copia)
        self.db.commit()
        self.db.refresh(copia)
        return copia

    def vincular(self, id: int, guia: Guia) -> None:
        sesion = self.db.get(Sesion, id)
        sesion.vinculada = True
        self.db.commit()

    def desvincular(self, id: int) -> None:
        sesion = self.db.get(Sesion, id)
        self.db.delete(sesion)
        self.db.commit()

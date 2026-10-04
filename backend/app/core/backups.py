import json
import logging
import os
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import engine
from app.schemas.copia_seguridad import CopiaSeguridadResponse, SaludCopiaSeguridadResponse

logger = logging.getLogger(__name__)

NOMBRE_MANIFIESTO_BACKUPS = "backups_manifest.jsonl"


def obtener_version_esquema(db: Session) -> int:
    """Versión del esquema = `PRAGMA user_version` de la BD viva (issue #628).
    Sin constante duplicada en Python: la fuente de verdad es el propio fichero
    `.db`."""
    return db.execute(text("PRAGMA user_version")).scalar() or 0


def ruta_manifiesto_backups() -> Path:
    """Directorio donde vive `pycelda.db` -- `/data` en producción
    (`docker-compose.yml`, `working_dir: /data` + volumen `pycelda-db`),
    derivado del mismo `engine` de `app.core.database` (única fuente de
    verdad del path) en vez de hardcodear un criterio propio. El manifiesto
    (issue #308) lo escribe `Claude-pyCelda-Prometeus` en la raíz de ese mismo
    volumen -- infraestructura, fuera de este repo."""
    return Path(engine.url.database).resolve().parent / NOMBRE_MANIFIESTO_BACKUPS


def _estado_fichero_copia(archivo: str) -> tuple[bool, int | None]:
    """(disponible, esquema_version) leídos del fichero real del volumen
    (issue #677), la misma fuente que `preparar_restauracion()`; el
    `esquema_version` del manifiesto no se usa. Nombre con separadores o
    fichero ausente -> no disponible (sin abrir nada). Fichero que no abre
    como SQLite -> disponible pero versión desconocida (None); nunca excepción."""
    if archivo != Path(archivo).name:
        return False, None
    ruta = ruta_manifiesto_backups().parent / archivo
    if not ruta.is_file():
        return False, None
    try:
        return True, version_esquema_de_fichero(ruta)
    except sqlite3.Error as error:
        logger.warning("Copia %s ilegible como SQLite: %s", archivo, error)
        return True, None


def leer_copias_seguridad() -> list[CopiaSeguridadResponse]:
    """Parseo a la defensiva de `backups_manifest.jsonl` (JSON Lines,
    solo-append, issue #308): el fichero puede no existir todavía (lista
    vacía, no error) y las líneas las escribe un script bash sin validación
    -- una línea con JSON inválido o un campo faltante/con el tipo
    equivocado se salta con un warning, nunca rompe la respuesta entera.
    Orden de salida: timestamp descendente (más reciente primero)."""
    ruta = ruta_manifiesto_backups()
    if not ruta.exists():
        return []

    copias: list[CopiaSeguridadResponse] = []
    for numero_linea, linea in enumerate(
        ruta.read_text(encoding="utf-8").splitlines(), start=1
    ):
        linea = linea.strip()
        if not linea:
            continue
        try:
            datos = json.loads(linea)
            archivo = datos["archivo"]
            if not isinstance(archivo, str):
                raise TypeError("archivo no es str")
            disponible, esquema_version = _estado_fichero_copia(archivo)
            copias.append(
                CopiaSeguridadResponse(
                    timestamp=datos["timestamp"],
                    familia=datos["familia"],
                    archivo=archivo,
                    tamano_bytes=datos["tamano_bytes"],
                    motivo=datos.get("motivo"),
                    esquema_version=esquema_version,
                    disponible=disponible,
                )
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValidationError) as error:
            logger.warning(
                "%s línea %d mal formada, se salta: %s",
                NOMBRE_MANIFIESTO_BACKUPS,
                numero_linea,
                error,
            )
            continue

    copias.sort(key=lambda c: c.timestamp, reverse=True)
    return copias


FAMILIA_PRE_RESTAURACION = "pre_restauracion"
FAMILIA_PUNTUAL = "puntual"


def ruta_bd_viva() -> Path:
    """Fichero `pycelda.db` vivo, derivado del mismo `engine` que
    `ruta_manifiesto_backups()`."""
    return Path(engine.url.database).resolve()


def version_esquema_de_fichero(ruta: Path) -> int:
    """`PRAGMA user_version` del propio `.db` candidato, abierto directamente
    (sin pasar por el engine vivo). No se usa el `esquema_version` del
    manifiesto: lo escribe un script externo y puede desincronizarse."""
    conexion = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    try:
        return conexion.execute("PRAGMA user_version").fetchone()[0] or 0
    finally:
        conexion.close()


def informe_integridad_de_fichero(ruta: Path) -> str:
    """Primera línea del `PRAGMA integrity_check` del `.db` candidato, abierto
    en solo lectura. `"ok"` si está íntegro."""
    conexion = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    try:
        return str(conexion.execute("PRAGMA integrity_check").fetchone()[0])
    finally:
        conexion.close()


def comprobar_salud_copias() -> list[SaludCopiaSeguridadResponse]:
    """Issue #683. `PRAGMA integrity_check` en solo lectura sobre cada copia del
    manifiesto (mismo orden que el listado), con la misma función que usa
    `preparar_restauracion()`. Sin efectos: no borra, no mueve, no escribe el
    manifiesto. Un fallo en una copia no interrumpe las demás; nunca excepción.
    Nombre con separadores o fichero ausente -> `no_disponible` sin abrir nada."""
    resultado: list[SaludCopiaSeguridadResponse] = []
    for copia in leer_copias_seguridad():
        archivo = copia.archivo
        ruta = ruta_manifiesto_backups().parent / archivo
        if archivo != Path(archivo).name or not ruta.is_file():
            resultado.append(
                SaludCopiaSeguridadResponse(archivo=archivo, salud="no_disponible")
            )
            continue
        try:
            version_esquema_de_fichero(ruta)
        except sqlite3.Error as error:
            logger.warning("Copia %s ilegible como SQLite: %s", archivo, error)
            resultado.append(SaludCopiaSeguridadResponse(archivo=archivo, salud="ilegible"))
            continue
        # Cabecera legible: una página interior corrupta puede hacer que
        # SQLite lance en vez de informar; en ambos casos es una copia dañada.
        try:
            informe = informe_integridad_de_fichero(ruta)
        except sqlite3.Error as error:
            informe = str(error)
        if informe == "ok":
            resultado.append(SaludCopiaSeguridadResponse(archivo=archivo, salud="ok"))
        else:
            logger.warning("Copia %s dañada: %s", archivo, informe)
            resultado.append(
                SaludCopiaSeguridadResponse(
                    archivo=archivo,
                    salud="danada",
                    detalle=informe.splitlines()[0] if informe else None,
                )
            )
    return resultado


def resolver_archivo_backup(archivo: str) -> Path:
    """`archivo` tal cual aparece en el manifiesto -> ruta real. Solo se
    aceptan nombres que figuren en el manifiesto (404 si no): evita que el
    body apunte a rutas arbitrarias del sistema de ficheros."""
    if archivo != Path(archivo).name or archivo not in {
        c.archivo for c in leer_copias_seguridad()
    }:
        raise HTTPException(status_code=404, detail="Copia de seguridad no encontrada")
    return ruta_manifiesto_backups().parent / archivo


def _anexar_linea_manifiesto(linea: dict) -> None:
    with ruta_manifiesto_backups().open("a", encoding="utf-8") as f:
        f.write(json.dumps(linea, ensure_ascii=False) + "\n")


def crear_backup_puntual(
    db: Session,
    motivo: str | None = None,
    *,
    familia: str = FAMILIA_PUNTUAL,
    prefijo: str = "pyCelda-puntual",
    origen: Path | None = None,
) -> CopiaSeguridadResponse:
    """Snapshot consistente de la BD viva (API de backup de sqlite3, issue
    #629) + línea nueva en el manifiesto, familia 'puntual', CON
    esquema_version real (a diferencia de los backups que capturan los
    scripts bash hasta que Prometeus los actualice -- este SÍ nace
    restaurable desde el primer momento, issue #629). `familia`, `prefijo`
    y `origen` son solo para que `preparar_restauracion()` reutilice la
    función conservando su familia/nombre de fichero propios (issue #632)."""
    origen = origen or ruta_bd_viva()
    ahora = datetime.now(timezone.utc)
    carpeta = ruta_manifiesto_backups().parent
    base = f"{prefijo}-{ahora.strftime('%Y%m%d-%H%M%S')}"
    nombre, contador = f"{base}.db", 1
    while (carpeta / nombre).exists():
        contador += 1
        nombre = f"{base}-{contador}.db"
    destino = carpeta / nombre
    # API de backup de sqlite3: copia consistente aunque la BD viva esté en uso.
    conexion_origen = sqlite3.connect(origen)
    conexion_destino = sqlite3.connect(destino)
    try:
        conexion_origen.backup(conexion_destino)
    finally:
        conexion_destino.close()
        conexion_origen.close()

    linea = {
        "timestamp": ahora.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "familia": familia,
        "archivo": nombre,
        "tamano_bytes": destino.stat().st_size,
        "motivo": motivo,
        "esquema_version": obtener_version_esquema(db),
    }
    _anexar_linea_manifiesto(linea)
    return CopiaSeguridadResponse(**linea)


def _rechazar_copia_danada(ruta_backup: Path, informe: str) -> NoReturn:
    primera_linea = (informe.splitlines() or [""])[0]
    logger.warning(
        "Restauración rechazada: %s no pasa integrity_check: %s",
        ruta_backup.name,
        primera_linea,
    )
    raise HTTPException(
        status_code=409,
        detail=f"La copia está dañada (integrity_check): no se puede restaurar. {primera_linea}".rstrip(
            ". "
        ),
    )


def preparar_restauracion(
    ruta_backup: Path, db: Session, ruta_bd_actual: Path | None = None
) -> Path:
    """Valida compatibilidad y deja hecha la copia de seguridad de la BD viva
    (familia `pre_restauracion` en el manifiesto) antes de tocar nada.
    404 si el backup no existe; 409 si su `user_version` no coincide con el
    de la BD viva (los backups sin marca, valor 0, nunca son restaurables) o
    si no pasa `PRAGMA integrity_check` (o no abre como SQLite).
    Devuelve la ruta de la copia previa; no sobrescribe la BD viva."""
    if not ruta_backup.is_file():
        raise HTTPException(status_code=404, detail="Copia de seguridad no encontrada")
    try:
        version_backup = version_esquema_de_fichero(ruta_backup)
    except sqlite3.Error as error:
        _rechazar_copia_danada(ruta_backup, str(error))
    version_viva = obtener_version_esquema(db)
    if version_backup != version_viva:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Esquema incompatible: la copia tiene versión {version_backup} "
                f"y la base de datos actual {version_viva}"
            ),
        )
    try:
        informe = informe_integridad_de_fichero(ruta_backup)
    except sqlite3.Error as error:
        _rechazar_copia_danada(ruta_backup, str(error))
    if informe != "ok":
        _rechazar_copia_danada(ruta_backup, informe)

    copia = crear_backup_puntual(
        db,
        motivo=f"antes de restaurar {ruta_backup.name}",
        familia=FAMILIA_PRE_RESTAURACION,
        prefijo="pyCelda-pre-restauracion",
        origen=ruta_bd_actual,
    )
    return ruta_manifiesto_backups().parent / copia.archivo


def ejecutar_restauracion_y_reiniciar(ruta_backup: Path, ruta_bd_viva: Path) -> None:
    """Escribe el backup sobre la BD viva de forma atómica (temporal en el
    mismo directorio + `os.replace`) y termina el proceso: Docker
    (`restart: unless-stopped`) lo reinicia limpio contra el fichero nuevo."""
    temporal = ruta_bd_viva.with_name(ruta_bd_viva.name + ".restaurando")
    try:
        shutil.copyfile(ruta_backup, temporal)
        with temporal.open("rb") as f:
            os.fsync(f.fileno())
        os.replace(temporal, ruta_bd_viva)
    finally:
        temporal.unlink(missing_ok=True)
    # Un -wal/-shm de la BD anterior aplicado al fichero nuevo lo corrompería.
    for sufijo in ("-wal", "-shm"):
        ruta_bd_viva.with_name(ruta_bd_viva.name + sufijo).unlink(missing_ok=True)
    os._exit(0)

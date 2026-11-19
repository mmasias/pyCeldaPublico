"""Registro de accesos (#820): tabla nueva `registros_acceso`; bumpea
`PRAGMA user_version` de 7 a 8.

- `registros_acceso`: una fila por intento de login de Profesor/DirectorPrograma
  en `/auth/callback` (con éxito o rechazado). `create_all()` del arranque del
  backend también la crea; el script la crea igualmente si falta (mismo DDL
  que genera SQLAlchemy), para que el orden entre el deploy y el `apply` no
  importe.
- Sin backfill: la sesión es un JWT sin estado y nunca se persistió nada al
  entrar, no hay dato histórico que recuperar.

Requiere `user_version` = 7 (#808); con otro valor anterior se niega. Si
`user_version` >= 8, no hace nada. Todo en una transacción: si algo falla, la
base queda como estaba. Al final, `foreign_key_check` e `integrity_check`.

Dos modos (sin argumento = `plan`, nunca escribe por defecto):

    python -m app.scripts.migrar_registro_accesos plan
    python -m app.scripts.migrar_registro_accesos apply

Orden: copia de seguridad, `./deploy.sh`, `plan`, `apply` justo después. La
ventana entre el deploy y el `apply` es inocua: `create_all()` ya crea la
tabla al arrancar el backend, y lo único que queda pendiente es el bump de
`user_version`.

Tras el `apply`, los backups anteriores (versión 7, incluido el de antes del
deploy) ya no se restauran desde la aplicación (409 por versión de esquema):
volver atrás exige restaurar a mano el `.db` y desplegar la versión anterior.

    docker compose exec -T backend python -m app.scripts.migrar_registro_accesos plan
    docker compose exec -T backend python -m app.scripts.migrar_registro_accesos apply
"""

from __future__ import annotations

import sys

from sqlalchemy import Engine

from app.core.database import engine as _engine_por_defecto

VERSION_ANTERIOR = 7
VERSION_NUEVA = 8

_CREATE_REGISTROS_ACCESO = (
    "CREATE TABLE registros_acceso ("
    "id INTEGER NOT NULL, "
    "email VARCHAR(200) NOT NULL, "
    "exitoso BOOLEAN NOT NULL, "
    "motivo_rechazo VARCHAR(30), "
    "fecha DATETIME NOT NULL, "
    "PRIMARY KEY (id))"
)


def _tabla_existe(cur, tabla: str) -> bool:
    return (
        cur.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (tabla,)
        ).fetchone()
        is not None
    )


def migrar_registro_accesos(aplicar: bool, engine: Engine | None = None) -> None:
    engine = engine or _engine_por_defecto
    conexion = engine.raw_connection()
    try:
        sqlite = conexion.driver_connection
        sqlite.isolation_level = None
        cur = sqlite.cursor()
        print(f"Modo: {'apply' if aplicar else 'plan (dry-run)'}")
        version = cur.execute("PRAGMA user_version").fetchone()[0] or 0
        print(f"PRAGMA user_version actual: {version}")
        if version >= VERSION_NUEVA:
            print(f"nada que hacer: user_version >= {VERSION_NUEVA}")
            return
        if version < VERSION_ANTERIOR:
            print(
                f"\nuser_version = {version}: se esperaba {VERSION_ANTERIOR} -- faltan "
                "migraciones anteriores (#808). No se toca nada."
            )
            return
        fk_previas = cur.execute("PRAGMA foreign_key_check").fetchall()
        if fk_previas:
            print(
                f"\nLa base ya tiene {len(fk_previas)} violaciones de claves foráneas "
                f"(primeras: {fk_previas[:5]}). Hay que corregirlas antes de migrar. "
                "No se toca nada."
            )
            return

        falta_tabla = not _tabla_existe(cur, "registros_acceso")
        print(
            "Tabla registros_acceso: "
            f"{'falta' if falta_tabla else 'ya existe (creada por create_all() al arrancar)'}"
        )

        accion = "aplicando" if aplicar else "plan: se aplicaría"
        if falta_tabla:
            print(f"{accion} -> CREATE TABLE registros_acceso")
        print(f"{accion} -> PRAGMA user_version = {VERSION_NUEVA}")
        if not aplicar:
            return

        cur.execute("BEGIN IMMEDIATE")
        try:
            if falta_tabla:
                cur.execute(_CREATE_REGISTROS_ACCESO)
            errores_fk = cur.execute("PRAGMA foreign_key_check").fetchall()
            if errores_fk:
                raise RuntimeError(f"foreign_key_check: {errores_fk[:5]}")
            cur.execute(f"PRAGMA user_version = {VERSION_NUEVA}")
            cur.execute("COMMIT")
        except Exception:
            cur.execute("ROLLBACK")
            raise
        integridad = cur.execute("PRAGMA integrity_check").fetchone()[0]
        print(f"integrity_check: {integridad}")
        print(f"PRAGMA user_version = {VERSION_NUEVA} aplicado")
        print("Migración aplicada.")
    finally:
        conexion.close()


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if modo not in ("plan", "apply"):
        print(f"Modo desconocido: {modo!r} -- usa 'plan' o 'apply'")
        raise SystemExit(2)
    migrar_registro_accesos(aplicar=modo == "apply")

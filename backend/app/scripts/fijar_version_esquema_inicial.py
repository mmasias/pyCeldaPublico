"""Baseline de `PRAGMA user_version` (issue #628).

`PRAGMA user_version` es un entero que vive dentro del propio fichero `.db`
(0 de fábrica en SQLite, nunca usado antes en este repo). Es la fuente de
verdad de la versión de esquema: no existe constante equivalente en Python.

Idempotente: si `user_version` ya es distinto de 0 no hace nada; si es 0
ejecuta `PRAGMA user_version = 1`. El `1` representa "el esquema de hoy", no
un intento de reconstruir cuántas migraciones hubo en el pasado.

CONVENCIÓN (política completa en `core/README_version_esquema.md`, fijada en #655):
todo `migrar_*.py` que cambie `models/` debe
terminar con `PRAGMA user_version = N` (N = valor anterior + 1). Los anteriores a #655 no
implementado en los scripts existentes.

Dos modos:

    python -m app.scripts.fijar_version_esquema_inicial plan     (dry-run)
    python -m app.scripts.fijar_version_esquema_inicial apply

Sin argumento equivale a `plan` -- nunca escribe por defecto.

    docker compose exec -T backend python -m app.scripts.fijar_version_esquema_inicial apply
"""

from __future__ import annotations

import sys

from sqlalchemy import Engine, text

from app.core.database import engine as _engine_por_defecto

VERSION_BASELINE = 1


def fijar_version_esquema_inicial(aplicar: bool, engine: Engine | None = None) -> None:
    engine = engine or _engine_por_defecto
    with engine.connect() as conn:
        actual = conn.execute(text("PRAGMA user_version")).scalar() or 0
        print(f"Modo: {'apply' if aplicar else 'plan (dry-run)'}")
        print(f"PRAGMA user_version actual: {actual}")

        if actual != 0:
            print("nada que hacer, versión ya fijada")
            return

        if not aplicar:
            print(f"plan: se aplicaría -> PRAGMA user_version = {VERSION_BASELINE}")
            return

        conn.execute(text(f"PRAGMA user_version = {VERSION_BASELINE}"))
        conn.commit()
        print(f"PRAGMA user_version = {VERSION_BASELINE} aplicado")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if modo not in ("plan", "apply"):
        print(f"Modo desconocido: {modo!r} -- usa 'plan' o 'apply'")
        raise SystemExit(2)
    fijar_version_esquema_inicial(aplicar=modo == "apply")

"""Añade un índice único a `grados.codigo` (issue #148): permitió un
duplicado real en producción (`GIOI` dos veces, distinta `Facultad`) porque
la columna no tenía ninguna restricción de unicidad.

Dos modos:

    python -m app.scripts.migrar_unique_codigo_grado plan     (dry-run, no escribe nada)
    python -m app.scripts.migrar_unique_codigo_grado apply    (crea el índice)

Sin argumento equivale a `plan` -- nunca escribe por defecto.

**No se limpia ningún duplicado automáticamente**: si `apply` encuentra
`codigo` repetidos, aborta sin crear el índice y lista los duplicados --
resolverlos (fusionar, renombrar, eliminar) es una decisión de datos que
corresponde a quien opera, no a este script. El issue reporta que el
duplicado GIOI ya se limpió a mano en producción, pero este script no lo
da por sentado: vuelve a comprobarlo contra la BD real antes de aplicar.

Idempotente: `CREATE UNIQUE INDEX IF NOT EXISTS` -- reejecutar `apply` tras
haberlo aplicado ya es un no-op.
"""

from __future__ import annotations

import sys
from collections import Counter

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import SessionLocal

NOMBRE_INDICE = "ix_grados_codigo"


def _duplicados(sesion: Session) -> dict[str, int]:
    filas = sesion.execute(text("SELECT codigo FROM grados")).scalars().all()
    conteo = Counter(filas)
    return {codigo: n for codigo, n in conteo.items() if n > 1}


def migrar_unique_codigo_grado(aplicar: bool, db: Session | None = None) -> None:
    sesion = db or SessionLocal()
    cerrar = db is None
    try:
        print(f"Modo: {'apply' if aplicar else 'plan (dry-run)'}")
        duplicados = _duplicados(sesion)

        if duplicados:
            print(
                f"BLOQUEADO: {len(duplicados)} codigo(s) duplicado(s) en grados: "
                f"{duplicados} -- resolver antes de crear el índice único."
            )
            if aplicar:
                raise SystemExit(1)
            return

        print("Sin duplicados de codigo -- el índice único se puede crear.")

        if not aplicar:
            print(f"plan: se crearía {NOMBRE_INDICE} (no se ha escrito nada)")
            return

        sesion.execute(
            text(f"CREATE UNIQUE INDEX IF NOT EXISTS {NOMBRE_INDICE} ON grados (codigo)")
        )
        sesion.commit()
        print(f"apply: {NOMBRE_INDICE} creado (o ya existía)")
    finally:
        if cerrar:
            sesion.close()


def main() -> int:
    modo = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if modo not in ("plan", "apply"):
        print(f"Modo desconocido: {modo!r} -- usa 'plan' o 'apply'")
        return 1
    migrar_unique_codigo_grado(aplicar=modo == "apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())

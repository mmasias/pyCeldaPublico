"""Aritmética exacta de ponderaciones (issue #849).

PonderacionEvaluacion.ponderacion y SistemaEvaluacion.ponderacion_minima /
ponderacion_maxima son Numeric(5, 2): se suman y comparan en Decimal, nunca en
float (en float, 3.12 + 72.68 + 4.28 + 19.92 = 100.00000000000001)."""
from decimal import Decimal


def ponderacion_exacta(valor: Decimal | float | str) -> Decimal:
    """Ponderación como Decimal exacto para sumar y comparar (#849). Las
    columnas son Numeric(5, 2) y ya llegan como Decimal desde la BD; un valor
    aún sin persistir (float de la petición) pasa por str() para no arrastrar
    la representación binaria (Decimal(3.12) != Decimal("3.12"))."""
    if isinstance(valor, Decimal):
        return valor
    return Decimal(str(valor))

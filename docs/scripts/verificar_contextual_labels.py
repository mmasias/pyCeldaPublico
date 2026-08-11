#!/usr/bin/env python3
"""Verifica que cada entrada de CONTEXTUAL_LABELS coincide con el texto
literal de un botón dibujado en el wireframes.puml de su CU dueño.

No elimina la doble fuente de verdad entre CONTEXTUAL_LABELS y los
wireframes.puml -- la hace detectable. Propuesta de Z.AI/OpenCode en
discussion #52 (https://github.com/mmasias/pyCelda/discussions/52):
convierte la auditoría manual (hecha dos veces esta sesión) en un
chequeo automático.

Uso:
    python3 docs/scripts/verificar_contextual_labels.py

Sale con código 1 si encuentra alguna entrada cuya etiqueta no aparece
como botón literal en el wireframes.puml de su dueño.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DETAIL_DIR = REPO / "RUP/01-requisitos/03-detalle-casos-uso"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generar_mockup_navegable import CONTEXTUAL_LABELS  # noqa: E402

# Excepciones documentadas: la etiqueta es correcta pero no aparece dibujada
# literalmente en ningún wireframe estático del dueño -- no son bugs, son
# huecos conocidos ya evaluados y aceptados (ver auditoría 11 ago 2026).
KNOWN_EXCEPTIONS = {
    # desasignarProfesorAsignaturaGrado() no tiene wireframe propio (pendiente
    # wireframe); texto fijado a mano en el override, no derivable del dibujo.
    ("abrirAsignaturaGrado", "desasignarProfesorAsignaturaGrado"),
    # escalarGuiaAAprobada()/revocarAprobacionGuia() son botones condicionales
    # de abrirGuia() que solo aparecen en el estado Aprobada -- las dos
    # variantes de wireframe capturadas (Borrador/EnRevision) no lo dibujan;
    # el texto está documentado en prosa en el README del CU, no en el .puml.
    ("abrirGuia", "escalarGuiaAAprobada"),
    ("abrirGuia", "revocarAprobacionGuia"),
}


def extract_buttons(text):
    """Botones literales de un wireframes.puml: [Texto], [ <b>Texto</b> ],
    con o sin prefijo decorativo '+'."""
    buttons = set()
    for m in re.finditer(r"\[\s*(?:<b>)?\+?\s*([^\[\]<]+?)(?:</b>)?\s*\]", text):
        t = m.group(1).strip()
        if t and not t.startswith("http"):
            buttons.add(t)
    return buttons


def main():
    owners = sorted({owner for owner, _ in CONTEXTUAL_LABELS})
    mismatches = []
    skipped = []

    for owner in owners:
        wf_path = DETAIL_DIR / owner / "wireframes.puml"
        if not wf_path.exists():
            skipped.append(owner)
            continue
        real_buttons = extract_buttons(wf_path.read_text(encoding="utf-8"))
        for (o, target), label in CONTEXTUAL_LABELS.items():
            if o != owner:
                continue
            if label not in real_buttons and (owner, target) not in KNOWN_EXCEPTIONS:
                mismatches.append((owner, target, label, sorted(real_buttons)))

    if skipped:
        print(f"[AVISO] {len(skipped)} dueños sin wireframes.puml propio, no verificables: {', '.join(skipped)}")

    if mismatches:
        print(f"\n[FALLO] {len(mismatches)} entradas de CONTEXTUAL_LABELS no coinciden con el wireframe de su dueño:\n")
        for owner, target, label, real in mismatches:
            print(f'  ("{owner}", "{target}"): "{label}"  -- botones reales: {real}')
        sys.exit(1)

    total = sum(1 for owner, _ in CONTEXTUAL_LABELS if owner not in skipped)
    print(f"[OK] {total} entradas verificadas contra su wireframes.puml, sin discrepancias.")


if __name__ == "__main__":
    main()

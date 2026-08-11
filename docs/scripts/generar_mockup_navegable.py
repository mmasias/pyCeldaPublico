#!/usr/bin/env python3
"""Genera mockup navegable por actor desde diagrama de contexto + wireframes SVG.

Uso:
    python3 docs/scripts/generar_mockup_navegable.py <actor>

    <actor>: Admin | Profesor | DirectorGrado (debe existir diagramaContexto<actor>.puml)

Salida: docs/PROPUESTA_WIREFRAME/<actor_lower>/<cu>.md por cada CU detallado del actor.

El script produce la versión "simple" (tabla con solo las transiciones del actor).
La convención completa de "botones visibles sin enlace" se aplica a mano sobre
las páginas con desajuste wireframe-vs-diagrama. Ver README del artefacto.
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DIAGRAMS_DIR = REPO / "RUP/01-requisitos/01-actores-casos-uso"
SVG_DIR = REPO / "images/RUP/01-requisitos/03-detalle-casos-uso"
DETAIL_DIR = REPO / "RUP/01-requisitos/03-detalle-casos-uso"
OUT_BASE = REPO / "docs/PROPUESTA_WIREFRAME"

# Marca que protege una página contra sobreescritura por el script.
# Cualquier página que contenga esta línea en cualquier posición se respeta.
# El editor manual la añade cuando aplica la convención de "botones visibles sin enlace"
# u otros ajustes que el script no sabe producir.
OVERRIDE_MARKER = "<!-- MANUAL OVERRIDE: el script no sobreescribe este fichero -->"

# Etiquetas legibles para acrónimos y casos especiales
LABELS = {
    "iniciarSesion": "Iniciar sesión",
    "cerrarSesion": "Cerrar sesión",
    "generarGuiasPDF": "Generar guías PDF",
    "consultarEstadoGuias": "Consultar estado de guías",
    "reabrirGuiaPorIncidencia": "Reabrir guía por incidencia",
    "completarGestion": "Completar gestión",
    "descargarGuiaPDF": "Descargar guía PDF",
    "definirDirectorGrado": "Definir director de grado",
    "quitarDirectorGrado": "Quitar director de grado",
    "activarCursoAcademico": "Activar curso académico",
    "activarSemestre": "Activar semestre",
    "guardarBorradorGuia": "Guardar borrador de guía",
    "enviarGuiaARevision": "Enviar guía a revisión",
}

# Etiquetas para los sufijos de wireframe cuando hay varios
WIREFRAME_LABELS = {
    "wireframe.svg": None,
    "wireframe-formulario.svg": "Formulario",
    "wireframe-edicion.svg": "Edición",
    "wireframe-confirmacion.svg": "Confirmación",
    "wireframe-bloqueada.svg": "Bloqueada",
    "wireframe-advertencia.svg": "Con advertencia",
    "wireframe-normal.svg": "Caso normal",
    "wireframe-error.svg": "Estado de error",
    "wireframe-exito.svg": "Éxito",
    "wireframe-activado.svg": "Activado",
    "wireframe-generada.svg": "Generada",
    "wireframe-seleccion.svg": "Selección",
}

# Etiquetas dependientes de contexto: (cu_dueño_de_la_pagina, cu_destino) -> texto real
# del boton en el wireframe de cu_dueño. Solo para pares verificados donde ese wireframe
# es realmente la pantalla mostrada en pagina (no un formulario/selector autorreferencial
# que comparte estado destino con la pantalla canonica -- ver auditoria 11 ago 2026).
CONTEXTUAL_LABELS = {
    ("abrirAsignatura", "editarAsignatura"): "Editar",
    ("abrirCursoAcademico", "editarCursoAcademico"): "Editar",
    ("abrirFacultad", "editarFacultad"): "Editar",
    ("abrirGrado", "eliminarAsignaturaGrado"): "Eliminar",
    ("abrirGrado", "editarGrado"): "Editar",
    ("abrirMetodologiaDocente", "editarMetodologiaDocente"): "Editar",
    ("abrirProfesor", "editarProfesor"): "Editar",
    ("abrirProfesor", "quitarDirectorGrado"): "Quitar",
    ("abrirSistemaEvaluacion", "editarSistemaEvaluacion"): "Editar",
    ("abrirUniversidad", "editarUniversidad"): "Editar",
    ("abrirUniversidades", "abrirUniversidad"): "Abrir",
    ("consultarEstadoGuias", "abrirGuia"): "Abrir",
    ("consultarEstadoGuias", "completarGestion"): "Volver al grado",
    ("aprobarGuia", "abrirGuia"): "Abrir",
    ("aprobarGuia", "completarGestion"): "Volver al grado",
    ("rechazarGuia", "abrirGuia"): "Abrir",
    ("rechazarGuia", "completarGestion"): "Volver al grado",
    ("escalarGuiaAAprobada", "abrirGuia"): "Abrir",
    ("escalarGuiaAAprobada", "completarGestion"): "Volver al grado",
    ("revocarAprobacionGuia", "abrirGuia"): "Abrir",
    ("revocarAprobacionGuia", "completarGestion"): "Volver al grado",
    ("reabrirGuiaPorIncidencia", "abrirGuia"): "Abrir",
    ("reabrirGuiaPorIncidencia", "completarGestion"): "Volver al grado",
    ("eliminarPonderacionEvaluacion", "crearPonderacionEvaluacion"): "Crear Ponderación",
    ("eliminarPonderacionEvaluacion", "abrirPonderacionEvaluacion"): "Abrir",
    ("eliminarPonderacionEvaluacion", "abrirGuia"): "Volver a la guía",
    ("eliminarReferenciaBibliografica", "crearReferenciaBibliografica"): "Crear Referencia",
    ("eliminarReferenciaBibliografica", "abrirReferenciaBibliografica"): "Abrir",
    ("eliminarReferenciaBibliografica", "abrirGuia"): "Volver a la guía",
    ("abrirAsignaturasGrado", "abrirGuia"): "Abrir",
    ("abrirPonderacionEvaluacion", "editarPonderacionEvaluacion"): "Editar",
    ("abrirReferenciaBibliografica", "editarReferenciaBibliografica"): "Editar",
    ("abrirResultadoAprendizaje", "editarResultadoAprendizaje"): "Editar",
    ("notificarGuiasActualizadas", "abrirGuia"): "Abrir",
    ("abrirPonderacionesEvaluacion", "abrirGuia"): "Volver a la guía",
    ("abrirPonderacionesEvaluacion", "abrirPonderacionEvaluacion"): "Abrir",
    ("abrirPonderacionesEvaluacion", "eliminarPonderacionEvaluacion"): "Eliminar",
    ("abrirPonderacionesEvaluacion", "crearPonderacionEvaluacion"): "Crear Ponderación",
    ("abrirReferenciasBibliograficas", "abrirGuia"): "Volver a la guía",
    ("abrirReferenciasBibliograficas", "abrirReferenciaBibliografica"): "Abrir",
    ("abrirReferenciasBibliograficas", "eliminarReferenciaBibliografica"): "Eliminar",
    ("abrirReferenciasBibliograficas", "crearReferenciaBibliografica"): "Crear Referencia",
    ("enviarGuiaARevision", "abrirGuia"): "Volver a la guía",
    ("abrirGuia", "abrirPonderacionesEvaluacion"): "Gestionar evaluación",
    ("abrirGuia", "abrirReferenciasBibliograficas"): "Gestionar bibliografía",
    ("abrirGuia", "guardarBorradorGuia"): "Guardar borrador",
    ("abrirGuia", "completarGestion"): "Volver a mis asignaturas",
    ("abrirGuia", "enviarGuiaARevision"): "Enviar a revisión",
    ("abrirGuia", "aprobarGuia"): "Aprobar",
    ("abrirGuia", "rechazarGuia"): "Rechazar",
    ("abrirGuia", "escalarGuiaAAprobada"): "Escalar a aprobada",
    ("abrirGuia", "revocarAprobacionGuia"): "Revocar aprobación",
    ("abrirGuia", "editarSemestreGuia"): "Editar semestre",
    ("abrirGuia", "consultarEstadoGuias"): "Volver al listado de guías",
}

def label(cu, owner_cu=None):
    if owner_cu is not None and (owner_cu, cu) in CONTEXTUAL_LABELS:
        return CONTEXTUAL_LABELS[(owner_cu, cu)]
    if cu in LABELS:
        return LABELS[cu]
    s = re.sub(r"([A-Z])", r" \1", cu).strip().lower()
    return s.capitalize()

def find_wireframes(cu):
    """Devuelve lista de (svg_path, etiqueta) para un CU. Vacío si no existe carpeta o no hay SVGs."""
    svg_folder = SVG_DIR / cu
    if not svg_folder.exists():
        return []
    svgs = sorted(svg_folder.glob("wireframe*.svg"))
    result = []
    for svg in svgs:
        rel = f"/{svg.relative_to(REPO).as_posix()}"
        lbl = WIREFRAME_LABELS.get(svg.name)
        if lbl is None and svg.name != "wireframe.svg":
            suffix = svg.stem.replace("wireframe-", "")
            lbl = suffix.capitalize()
        result.append((rel, lbl))
    return result

def write_page(path, content):
    """Escribe la página salvo si existe y contiene OVERRIDE_MARKER. Devuelve True si escribió."""
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if OVERRIDE_MARKER in existing:
            print(f"  [SKIP] {path.name} (override manual protegido)")
            return False
    path.write_text(content, encoding="utf-8")
    return True

def parse_diagram(path):
    text = path.read_text(encoding="utf-8")
    transitions = []
    for line in text.splitlines():
        m = re.match(r"\s*(\w+)\s*-->\s*(\w+)\s*:\s*(\w+)\(\)", line)
        if m:
            transitions.append((m.group(1), m.group(2), m.group(3)))
    return transitions

def render_page(actor, cu, outgoing, is_placeholder=False):
    lines = [f"# {actor}", "", "<div align=center>", ""]
    if is_placeholder:
        lines.append(f"*Pendiente de detallar: `{cu}()`*")
    else:
        wireframes = find_wireframes(cu)
        if len(wireframes) == 1:
            # Caso único: imagen sin tabla
            svg_path, _ = wireframes[0]
            lines.append(f"![]({svg_path})")
        else:
            # Multi-wireframe: tabla horizontal para comparación visual
            labels = [lbl if lbl else "Vista principal" for _, lbl in wireframes]
            header = "|" + "|".join(f"**{l}**" for l in labels) + "|"
            sep = "|" + "|".join(["---"] * len(wireframes)) + "|"
            row = "|" + "|".join(f"![]({svg_path})" for svg_path, _ in wireframes) + "|"
            lines.extend([header, sep, row])
    lines.extend(["", "|Botón|CdU|", "|---|---|"])
    seen = set()
    for dst, cu_out in outgoing:
        if cu_out == cu:
            continue
        # dedup solo por cu_out: un mismo botón puede tener más de un destino
        # posible (éxito/fracaso, p.ej. enviarGuiaARevision()) sin dejar de ser
        # una sola fila -- es un único clic, no uno por posible desenlace interno.
        if cu_out in seen:
            continue
        seen.add(cu_out)
        lbl = label(cu_out, owner_cu=cu)
        if dst == "SESION_CERRADA":
            lines.append(f"|**{lbl}**|<sub>{cu_out}() (sin página: vuelve a login)</sub>|")
        elif cu_out in detailed_cus and cu_out in cus_in_actor:
            lines.append(f"|[**{lbl}**]({cu_out}.md)|<sub>{cu_out}()</sub>|")
        else:
            lines.append(f"|**{lbl}**|<sub>{cu_out}() (pendiente)</sub>|")
    lines.extend(["", "</div>", ""])
    return "\n".join(lines)

def main(actor):
    diagram_path = DIAGRAMS_DIR / f"diagramaContexto{actor}.puml"
    if not diagram_path.exists():
        sys.exit(f"Diagrama no encontrado: {diagram_path}")

    actor_lower = actor[0].lower() + actor[1:]
    out_dir = OUT_BASE / actor_lower
    out_dir.mkdir(parents=True, exist_ok=True)

    transitions = parse_diagram(diagram_path)
    state_outgoing = {}
    for src, dst, cu in transitions:
        state_outgoing.setdefault(src, []).append((dst, cu))

    # cu -> estado destino (preferir no-self)
    global cu_to_dst, detailed_cus, cus_in_actor
    cu_to_dst = {}
    for src, dst, cu in transitions:
        if cu not in cu_to_dst:
            cu_to_dst[cu] = dst
        elif src != dst and cu_to_dst[cu] == src:
            cu_to_dst[cu] = dst
    # Excepciones conocidas (CU de entrada a hub)
    if actor == "Admin":
        cu_to_dst["iniciarSesion"] = "SISTEMA_DISPONIBLE"
    elif actor == "Profesor":
        cu_to_dst["iniciarSesion"] = "ASIGNATURAS_GRADO_ABIERTO"
    elif actor == "DirectorGrado":
        cu_to_dst["iniciarSesion"] = "GRADOS_ABIERTO"

    cus_in_actor = {cu for _, _, cu in transitions}

    # CU detallados con al menos un wireframe*.svg
    detailed_cus = set()
    for d in DETAIL_DIR.iterdir():
        if d.is_dir():
            svgs = list((SVG_DIR / d.name).glob("wireframe*.svg"))
            if svgs:
                detailed_cus.add(d.name)

    pages = []

    # 1. Identificar CU canónico de entrada para cada estado (excepto SESION_CERRADA)
    state_incoming = {}
    for src, dst, cu in transitions:
        state_incoming.setdefault(dst, []).append((src, cu))

    all_states = set()
    for src, dst, _ in transitions:
        all_states.add(src)
        all_states.add(dst)

    state_to_canonical_cu = {}
    for state in all_states:
        if state == "SESION_CERRADA":
            continue
        incoming = state_incoming.get(state, [])
        if not incoming:
            continue
        # Si hay un CU desde SESION_CERRADA, ese es el canónico (es el aterrizaje)
        canonical = None
        for src, cu in incoming:
            if src == "SESION_CERRADA":
                canonical = cu
                break
        if not canonical:
            for src, cu in incoming:
                if cu.startswith("abrir"):
                    canonical = cu
                    break
        if not canonical:
            canonical = incoming[0][1]
        state_to_canonical_cu[state] = canonical

    # 2. Placeholders para estados cuyo CU canónico no está detallado
    # + forzar placeholder de iniciarSesion (punto de aterrizaje del actor)
    # incluso si el estado destino tiene otro CU canónico detallado.
    forced_placeholders = set()
    if "iniciarSesion" in cus_in_actor and "iniciarSesion" not in detailed_cus:
        forced_placeholders.add("iniciarSesion")

    for state, cu in sorted(state_to_canonical_cu.items()):
        if cu in detailed_cus and cu not in forced_placeholders:
            continue  # ya tiene página propia
        if cu not in cus_in_actor:
            continue
        outgoing = state_outgoing.get(state, [])
        content = render_page(actor, cu, outgoing, is_placeholder=True)
        wrote = write_page(out_dir / f"{cu}.md", content)
        status = "prot" if not wrote else "ok"
        pages.append((cu, False, status))

    # 3. Páginas por CU detallado
    for cu in sorted(detailed_cus & cus_in_actor):
        state_dst = cu_to_dst.get(cu)
        if state_dst is None or state_dst == "SESION_CERRADA":
            continue
        outgoing = state_outgoing.get(state_dst, [])
        content = render_page(actor, cu, outgoing)
        wrote = write_page(out_dir / f"{cu}.md", content)
        status = "prot" if not wrote else "ok"
        pages.append((cu, True, status))

    print(f"[{actor}] {len(pages)} páginas en {out_dir}:")
    ok = sum(1 for _, h, s in pages if h and s == "ok")
    pend = sum(1 for _, h, s in pages if not h and s == "ok")
    prot = sum(1 for _, _, s in pages if s == "prot")
    print(f"  Con SVG generadas: {ok} | Placeholders generados: {pend} | Protegidos (override): {prot}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python3 generar_mockup_navegable.py <Actor>")
    # Globals necesitados por render_page
    detailed_cus = set()
    cus_in_actor = set()
    cu_to_dst = {}
    main(sys.argv[1])

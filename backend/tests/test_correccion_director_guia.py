"""Issue #612 (Parte 2 de #601): DirectorPrograma edita el contenido de una
Guia del Profesor como corrección excepcional. La escritura aplica, antes de
responder, la transición de estado: Aprobada -> Borrador, EnRevision ->
Rechazada, Borrador/Rechazada se mantienen."""

import pytest

from app.core.auth import (
    get_current_director_programa_id_opcional,
    get_current_profesor_id_opcional,
)
from app.main import app
from app.models.guia import Guia
from app.models.historial_cambio import HistorialCambio
from app.models.ponderacion_evaluacion import PonderacionEvaluacion
from app.models.referencia_bibliografica import ReferenciaBibliografica
from app.models.sesion import Sesion

TRANSICIONES = [
    ("Aprobada", "Borrador", True),
    ("EnRevision", "Rechazada", True),
    ("Borrador", "Borrador", False),
    ("Rechazada", "Rechazada", False),
]

CUERPO_VACIO = {
    "ids_ponderaciones_final": [],
    "ids_referencias_final": [],
    "ids_sesiones_final": [],
}


def _como_director(director_id):
    """El actor es un Director puro: sin identidad de Profesor."""
    app.dependency_overrides[get_current_profesor_id_opcional] = lambda: None
    app.dependency_overrides[get_current_director_programa_id_opcional] = (
        lambda: director_id
    )


def _fijar_estado(db_session, guia, estado):
    guia.estado = estado
    db_session.commit()


def _historial_estado(db_session, guia):
    db_session.expire_all()
    return (
        db_session.query(HistorialCambio)
        .filter_by(guia_id=guia.id, campo="estado")
        .all()
    )


def _escribir_contenido(client, guia, _sistema):
    return client.put(
        f"/api/v1/guias/{guia.id}/borrador",
        json={**CUERPO_VACIO, "contenido": "Temario corregido por el Director"},
    )


def _escribir_ponderacion(client, guia, sistema):
    return client.post(
        f"/api/v1/guias/{guia.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema.id,
            "descripcion": "Examen",
            "ponderacion": 30,
        },
    )


def _escribir_referencia(client, guia, _sistema):
    return client.post(
        f"/api/v1/guias/{guia.id}/referencias-bibliograficas",
        json={"tipo": "Basica", "referencia": "Sommerville"},
    )


def _escribir_sesion(client, guia, _sistema):
    return client.post(
        f"/api/v1/guias/{guia.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "Presentación"},
    )


FLUJOS = [
    _escribir_contenido,
    _escribir_ponderacion,
    _escribir_referencia,
    _escribir_sesion,
]


@pytest.mark.parametrize("escribir", FLUJOS)
@pytest.mark.parametrize("estado, esperado, registra", TRANSICIONES)
def test_director_escribe_y_dispara_la_transicion(
    client,
    db_session,
    guia_vinculada,
    director_programa,
    sistema_evaluacion,
    escribir,
    estado,
    esperado,
    registra,
):
    _fijar_estado(db_session, guia_vinculada, estado)
    _como_director(director_programa.id)

    resp = escribir(client, guia_vinculada, sistema_evaluacion)
    assert resp.status_code in (200, 201)

    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == esperado

    filas = _historial_estado(db_session, guia_vinculada)
    if not registra:
        assert filas == []
        return
    assert len(filas) == 1
    fila = filas[0]
    assert fila.autor_id == director_programa.id
    assert fila.valor_anterior == estado
    assert fila.valor_nuevo == esperado
    assert fila.comentario == "corrección directa del Director"


@pytest.mark.parametrize("escribir", FLUJOS)
def test_director_ajeno_recibe_404_sin_cambiar_estado(
    client,
    db_session,
    guia_vinculada,
    otro_director_programa,
    sistema_evaluacion,
    escribir,
):
    _fijar_estado(db_session, guia_vinculada, "Aprobada")
    _como_director(otro_director_programa.id)

    resp = escribir(client, guia_vinculada, sistema_evaluacion)
    assert resp.status_code == 404

    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == "Aprobada"
    assert _historial_estado(db_session, guia_vinculada) == []


@pytest.mark.parametrize("escribir", FLUJOS)
def test_profesor_sigue_igual_sin_transicion_ni_historial_de_estado(
    client, db_session, guia_vinculada, sistema_evaluacion, escribir
):
    """Profesor dueño (override por defecto del fixture `client`): las rutas
    sueltas no tocan el estado; guardarBorrador() conserva su degradado propio
    Aprobada -> Borrador sin fila de estado."""
    _fijar_estado(db_session, guia_vinculada, "EnRevision")

    resp = escribir(client, guia_vinculada, sistema_evaluacion)
    assert resp.status_code in (200, 201)

    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == "EnRevision"
    assert _historial_estado(db_session, guia_vinculada) == []


def test_historial_de_contenido_lleva_autor_del_director(
    client, db_session, guia_vinculada, director_programa
):
    _como_director(director_programa.id)
    resp = client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={**CUERPO_VACIO, "contenido": "Nuevo temario"},
    )
    assert resp.status_code == 200

    fila = (
        db_session.query(HistorialCambio)
        .filter_by(guia_id=guia_vinculada.id, campo="contenido")
        .one()
    )
    assert fila.autor_id == director_programa.id


def test_director_edita_ponderacion_existente_y_revoca_aprobacion(
    client, db_session, guia_vinculada, director_programa, sistema_evaluacion
):
    ponderacion = PonderacionEvaluacion(
        guia_id=guia_vinculada.id,
        sistema_evaluacion_id=sistema_evaluacion.id,
        descripcion="Examen",
        ponderacion=30,
    )
    db_session.add(ponderacion)
    db_session.commit()
    _fijar_estado(db_session, guia_vinculada, "Aprobada")
    _como_director(director_programa.id)

    resp = client.put(
        f"/api/v1/ponderaciones-evaluacion/{ponderacion.id}",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Examen final",
            "ponderacion": 40,
        },
    )
    assert resp.status_code == 200
    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == "Borrador"


def test_director_edita_referencia_existente_y_rechaza_en_revision(
    client, db_session, guia_vinculada, director_programa
):
    referencia = ReferenciaBibliografica(
        guia_id=guia_vinculada.id, tipo="Basica", referencia="Sommerville"
    )
    db_session.add(referencia)
    db_session.commit()
    _fijar_estado(db_session, guia_vinculada, "EnRevision")
    _como_director(director_programa.id)

    resp = client.put(
        f"/api/v1/referencias-bibliograficas/{referencia.id}",
        json={"tipo": "Complementaria", "referencia": "Pressman"},
    )
    assert resp.status_code == 200
    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == "Rechazada"


def test_director_edita_y_duplica_sesion(
    client, db_session, guia_vinculada, director_programa
):
    sesion = Sesion(
        guia_id=guia_vinculada.id,
        numero=1,
        tipo="CLASE_TEORICA",
        descripcion="Intro",
    )
    db_session.add(sesion)
    db_session.commit()
    _como_director(director_programa.id)

    _fijar_estado(db_session, guia_vinculada, "Aprobada")
    resp = client.put(
        f"/api/v1/sesiones/{sesion.id}",
        json={"tipo": "CLASE_TEORICA", "descripcion": "Intro corregida"},
    )
    assert resp.status_code == 200
    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == "Borrador"

    _fijar_estado(db_session, guia_vinculada, "EnRevision")
    resp = client.post(f"/api/v1/sesiones/{sesion.id}/duplicar")
    assert resp.status_code == 200
    db_session.expire_all()
    assert db_session.get(Guia, guia_vinculada.id).estado == "Rechazada"


def test_director_puede_leer_listados_de_su_programa(
    client, db_session, guia_vinculada, director_programa, sistema_evaluacion
):
    _como_director(director_programa.id)
    for ruta in (
        "ponderaciones-evaluacion",
        "referencias-bibliograficas",
        "sistemas-evaluacion",
        "sesiones",
    ):
        resp = client.get(f"/api/v1/guias/{guia_vinculada.id}/{ruta}")
        assert resp.status_code == 200, ruta


def test_director_no_puede_generar_planificacion_generica(
    client, db_session, guia_vinculada, director_programa
):
    """Fuera de alcance de #612: sigue siendo exclusivo de Profesor."""
    from app.core.auth import get_current_profesor_id

    app.dependency_overrides[get_current_profesor_id] = lambda: 99999
    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/sesiones/generar-genericas")
    assert resp.status_code == 404

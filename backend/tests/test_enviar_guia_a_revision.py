from app.core.auth import get_current_profesor_id
from app.main import app
from app.models.sistema_evaluacion import SistemaEvaluacion


def test_enviar_guia_a_revision_rechaza_si_hay_pendientes(
    client, guia_vinculada, sistema_evaluacion
):
    client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "P1",
            "ponderacion": 20,
        },
    )
    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 409


def test_enviar_guia_a_revision_rechaza_si_suma_no_100(
    client, guia_vinculada, sistema_evaluacion
):
    r1 = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "P1",
            "ponderacion": 20,
        },
    )
    id1 = r1.json()["id"]
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={"ids_ponderaciones_final": [id1], "ids_referencias_final": [], "ids_sesiones_final": []},
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 422


def test_enviar_guia_a_revision_exito(client, db_session, guia_vinculada, materia):
    sistema = SistemaEvaluacion(
        materia_id=materia.id,
        tipo="Evaluación continua",
        descripcion="Único",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    db_session.add(sistema)
    db_session.commit()
    db_session.refresh(sistema)

    r1 = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema.id,
            "descripcion": "P1",
            "ponderacion": 100,
        },
    )
    id1 = r1.json()["id"]
    # guia_vinculada.sesiones_minimas == 1: una Sesion vinculada cubre la regla c3.
    rs = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "S1"},
    )
    sid = rs.json()["id"]
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [id1],
            "ids_referencias_final": [],
            "ids_sesiones_final": [sid],
        },
    )

    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [id1],
            "ids_referencias_final": [],
            "ids_sesiones_final": [sid],
            "contenido": "Temario que debe viajar con la guía a revisión",
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "EnRevision"
    # discussion #191: enviarGuiaARevision() arrastra el contenido editado.
    assert resp.json()["contenido"] == "Temario que debe viajar con la guía a revisión"


def test_enviar_guia_a_revision_profesor_no_dueno_devuelve_404(
    client, guia_con_dueno_y_otro
):
    guia, otro = guia_con_dueno_y_otro
    app.dependency_overrides[get_current_profesor_id] = lambda: otro.id

    resp = client.post(f"/api/v1/guias/{guia.id}/enviar-a-revision")
    assert resp.status_code == 404


def test_enviar_guia_a_revision_sin_asignatura_programa_devuelve_404(client, guia):
    resp = client.post(f"/api/v1/guias/{guia.id}/enviar-a-revision")
    assert resp.status_code == 404


def test_enviar_guia_a_revision_rechaza_si_hay_sesion_pendiente(client, guia_vinculada):
    """Bloque 2 de #206: el 409 de "items sin guardar" ahora incluye Sesion.
    Una sesion creada y no guardada en el borrador bloquea el envio, igual que
    una ponderacion o referencia pendiente."""
    client.post(
        f"/api/v1/guias/{guia_vinculada.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "S1"},
    )
    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 409


def test_enviar_guia_a_revision_no_bloquea_si_la_sesion_esta_guardada(
    client, db_session, guia_vinculada, materia
):
    sistema = SistemaEvaluacion(
        materia_id=materia.id,
        tipo="Evaluación continua",
        descripcion="Único",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    db_session.add(sistema)
    db_session.commit()
    db_session.refresh(sistema)

    rp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema.id,
            "descripcion": "P1",
            "ponderacion": 100,
        },
    )
    rs = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "S1"},
    )
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [rp.json()["id"]],
            "ids_referencias_final": [],
            "ids_sesiones_final": [rs.json()["id"]],
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "EnRevision"


def test_enviar_guia_a_revision_rechaza_si_planificacion_docente_incompleta(
    client, db_session, guia_vinculada, materia
):
    """Regla c3 (discussion #206): con c1 (nada pendiente) y c2 (ponderaciones
    OK) satisfechas, la Guia sigue sin poder enviarse si tiene menos de
    sesiones_minimas Sesion vinculadas."""
    guia_vinculada.sesiones_minimas = 3
    db_session.commit()

    sistema = SistemaEvaluacion(
        materia_id=materia.id,
        tipo="Evaluación continua",
        descripcion="Único",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    db_session.add(sistema)
    db_session.commit()
    db_session.refresh(sistema)

    rp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={"sistema_evaluacion_id": sistema.id, "descripcion": "P1", "ponderacion": 100},
    )
    rs = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "S1"},
    )
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [rp.json()["id"]],
            "ids_referencias_final": [],
            "ids_sesiones_final": [rs.json()["id"]],
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 422
    assert "1 de 3" in resp.json()["detail"]


# issue #208: Guia.puede_enviarse_a_revision() solo validaba el rango de los
# SistemaEvaluacion que ya tenían alguna ponderación vinculada -- un sistema
# requerido (ponderacion_minima > 0) en 0% se colaba sin bloquear. Fix:
# Guia.bloqueo_ponderaciones() recorre TODOS los SistemaEvaluacion de la
# materia, tratando como 0% el que no tiene ninguna ponderación vinculada.


def test_enviar_guia_a_revision_sistema_requerido_en_cero_bloquea(
    client, db_session, guia_vinculada, materia_del_programa
):
    sistema_cubierto = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Examen",
        descripcion="Único",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    sistema_sin_asignar = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Prácticas",
        descripcion="Requeridas",
        ponderacion_minima=20,
        ponderacion_maxima=50,
    )
    db_session.add_all([sistema_cubierto, sistema_sin_asignar])
    db_session.commit()

    rp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_cubierto.id,
            "descripcion": "P1",
            "ponderacion": 100,
        },
    )
    # guia_vinculada.sesiones_minimas == 1: cubre c3 para aislar el fallo en c2.
    rs = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "S1"},
    )
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [rp.json()["id"]],
            "ids_referencias_final": [],
            "ids_sesiones_final": [rs.json()["id"]],
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 422
    assert resp.json()["detail"] == (
        "Falta asignar 20% en Prácticas (mínimo 20%, asignado 0%)"
    )


def test_enviar_guia_a_revision_sistema_por_encima_del_maximo_mensaje_sobra(
    client, db_session, guia_vinculada, materia_del_programa
):
    """El maximo de un SistemaEvaluacion se valida por ponderacion individual
    al crearla (validar_maximo), no por suma -- para superarlo hacen falta
    varias ponderaciones bajo el mismo sistema, cada una dentro de su propio
    maximo, cuya suma sí lo excede."""
    sistema_excedido = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Examen",
        descripcion="Excedido",
        ponderacion_minima=0,
        ponderacion_maxima=50,
    )
    sistema_resto = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Prácticas",
        descripcion="Resto",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    db_session.add_all([sistema_excedido, sistema_resto])
    db_session.commit()

    r1 = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_excedido.id,
            "descripcion": "P1",
            "ponderacion": 30,
        },
    )
    r2 = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_excedido.id,
            "descripcion": "P2",
            "ponderacion": 30,
        },
    )
    r3 = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_resto.id,
            "descripcion": "P3",
            "ponderacion": 40,
        },
    )
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [
                r1.json()["id"],
                r2.json()["id"],
                r3.json()["id"],
            ],
            "ids_referencias_final": [],
            "ids_sesiones_final": [],
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 422
    assert resp.json()["detail"] == (
        "Sobra 10% en Examen (máximo 50%, asignado 60%)"
    )


def test_enviar_guia_a_revision_sistema_sin_minimo_en_cero_no_bloquea(
    client, db_session, guia_vinculada, materia_del_programa
):
    sistema_cubierto = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Examen",
        descripcion="Único",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    sistema_opcional_en_cero = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Prácticas",
        descripcion="Opcional",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    db_session.add_all([sistema_cubierto, sistema_opcional_en_cero])
    db_session.commit()

    rp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_cubierto.id,
            "descripcion": "P1",
            "ponderacion": 100,
        },
    )
    rs = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/sesiones",
        json={"tipo": "CLASE_TEORICA", "descripcion": "S1"},
    )
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [rp.json()["id"]],
            "ids_referencias_final": [],
            "ids_sesiones_final": [rs.json()["id"]],
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "EnRevision"


def test_enviar_guia_a_revision_permitido_al_alcanzar_sesiones_minimas(
    client, db_session, guia_vinculada, materia
):
    guia_vinculada.sesiones_minimas = 2
    db_session.commit()

    sistema = SistemaEvaluacion(
        materia_id=materia.id,
        tipo="Evaluación continua",
        descripcion="Único",
        ponderacion_minima=0,
        ponderacion_maxima=100,
    )
    db_session.add(sistema)
    db_session.commit()
    db_session.refresh(sistema)

    rp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={"sistema_evaluacion_id": sistema.id, "descripcion": "P1", "ponderacion": 100},
    )
    sids = [
        client.post(
            f"/api/v1/guias/{guia_vinculada.id}/sesiones",
            json={"tipo": "CLASE_TEORICA", "descripcion": f"S{i}"},
        ).json()["id"]
        for i in range(2)
    ]
    client.put(
        f"/api/v1/guias/{guia_vinculada.id}/borrador",
        json={
            "ids_ponderaciones_final": [rp.json()["id"]],
            "ids_referencias_final": [],
            "ids_sesiones_final": sids,
        },
    )

    resp = client.post(f"/api/v1/guias/{guia_vinculada.id}/enviar-a-revision")
    assert resp.status_code == 200
    assert resp.json()["estado"] == "EnRevision"

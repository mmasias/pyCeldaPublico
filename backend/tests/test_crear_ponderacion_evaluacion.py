from app.core.auth import (
    get_current_director_programa_id_opcional,
    get_current_profesor_id,
    get_current_profesor_id_opcional,
)
from app.main import app
from app.models.sistema_evaluacion import SistemaEvaluacion


def test_listar_sistemas_evaluacion(client, materia, sistema_evaluacion):
    resp = client.get(f"/api/v1/materias/{materia.id}/sistemas-evaluacion")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == sistema_evaluacion.id


def test_listar_sistemas_evaluacion_de_guia(client, db_session, guia_vinculada, materia_del_programa):
    sistema = SistemaEvaluacion(
        materia_id=materia_del_programa.id,
        tipo="Evaluación continua",
        descripcion="Prácticas",
        ponderacion_minima=20,
        ponderacion_maxima=60,
    )
    db_session.add(sistema)
    db_session.commit()

    resp = client.get(f"/api/v1/guias/{guia_vinculada.id}/sistemas-evaluacion")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == sistema.id


def test_crear_ponderacion_evaluacion_dentro_del_maximo(
    client, guia_vinculada, sistema_evaluacion
):
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Examen parcial",
            "ponderacion": 30,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["vinculada"] is False
    assert data["ponderacion"] == 30
    assert data["sistema_evaluacion"]["id"] == sistema_evaluacion.id
    assert data["sistema_evaluacion"]["descripcion"] == sistema_evaluacion.descripcion


def test_crear_ponderacion_evaluacion_supera_el_maximo(
    client, guia_vinculada, sistema_evaluacion
):
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Examen parcial",
            "ponderacion": 90,
        },
    )
    assert resp.status_code == 422


def test_crear_ponderacion_evaluacion_profesor_no_dueno_devuelve_404(
    client, guia_con_dueno_y_otro, sistema_evaluacion
):
    guia, otro = guia_con_dueno_y_otro
    app.dependency_overrides[get_current_profesor_id_opcional] = lambda: otro.id
    app.dependency_overrides[get_current_director_programa_id_opcional] = lambda: None

    resp = client.post(
        f"/api/v1/guias/{guia.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Examen parcial",
            "ponderacion": 30,
        },
    )
    assert resp.status_code == 404


def test_crear_ponderacion_evaluacion_cero_rechazado(
    client, guia_vinculada, sistema_evaluacion
):
    """issue #298: una ponderación de 0 equivale a "el instrumento no existe"."""
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Vacío",
            "ponderacion": 0,
        },
    )
    assert resp.status_code == 422
    assert resp.json()["detail"] == (
        "La ponderación de un instrumento debe ser mayor que cero"
    )


def test_crear_ponderacion_evaluacion_negativo_rechazado(
    client, guia_vinculada, sistema_evaluacion
):
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Negativo",
            "ponderacion": -5,
        },
    )
    assert resp.status_code == 422


def test_crear_ponderacion_evaluacion_fraccion_minima_ok(
    client, guia_vinculada, sistema_evaluacion
):
    """> 0 es estricto pero cualquier valor positivo pasa el suelo."""
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Mínimo",
            "ponderacion": 0.5,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["ponderacion"] == 0.5


def test_crear_ponderacion_evaluacion_en_el_maximo_exacto_ok(
    client, guia_vinculada, sistema_evaluacion
):
    """Opción B (#298): un instrumento en ponderacion_maxima exacta se acepta
    -- el caso "examen final único = 100%" con horquilla [100, 100]."""
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Examen único",
            "ponderacion": 60,
        },
    )
    assert resp.status_code == 201
    assert resp.json()["ponderacion"] == 60


def test_crear_ponderacion_evaluacion_supera_maximo_wording(
    client, guia_vinculada, sistema_evaluacion
):
    """Hallazgo H-10: el 422 del tope dice "sistema de evaluación", no
    "SistemaEvaluacion"."""
    resp = client.post(
        f"/api/v1/guias/{guia_vinculada.id}/ponderaciones-evaluacion",
        json={
            "sistema_evaluacion_id": sistema_evaluacion.id,
            "descripcion": "Pasado",
            "ponderacion": 90,
        },
    )
    assert resp.status_code == 422
    assert resp.json()["detail"] == (
        "La ponderación supera el máximo del sistema de evaluación"
    )

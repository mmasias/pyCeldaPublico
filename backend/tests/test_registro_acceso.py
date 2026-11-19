"""Registro de accesos (#820): /auth/callback escribe una fila por intento
(éxito o rechazo) de Profesor/DirectorPrograma; /auth/admin/callback no
escribe; consultarRegistroAccesos() -- GET /api/v1/registro-accesos -- es de
Admin y devuelve las 25 últimas, más reciente primero."""

from datetime import UTC, datetime, timedelta

import pytest

from app.core.auth import create_admin_session_token, create_session_token, oauth
from app.core.config import get_settings
from app.models.director_programa import DirectorPrograma
from app.models.profesor import Profesor
from app.models.registro_acceso import RegistroAcceso

SESSION_SECRET = "test-session-secret-key-not-real"


@pytest.fixture(autouse=True)
def _session_secret(monkeypatch):
    monkeypatch.setenv("SESSION_SECRET_KEY", SESSION_SECRET)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class _FakeGoogleClient:
    """Sustituye a oauth.google -- sin red (mismo patrón que test_auth.py)."""

    def __init__(self, email: str, hd: str | None = None):
        self._email = email
        self._hd = hd

    async def authorize_access_token(self, request):
        return {"userinfo": {"email": self._email, "hd": self._hd}}


def _registros(db_session):
    db_session.expire_all()
    return db_session.query(RegistroAcceso).order_by(RegistroAcceso.id).all()


# --- escritura: /auth/callback ---------------------------------------------


def test_login_exitoso_de_profesor_registra_fila_exitosa(
    client_real_auth, db_session, monkeypatch
):
    db_session.add(Profesor(email="profesor@uneatlantico.es"))
    db_session.commit()
    monkeypatch.setattr(oauth, "google", _FakeGoogleClient("profesor@uneatlantico.es"))

    resp = client_real_auth.get("/auth/callback", follow_redirects=False)

    assert resp.status_code in (302, 307)
    assert get_settings().session_cookie_name in resp.cookies
    [fila] = _registros(db_session)
    assert fila.email == "profesor@uneatlantico.es"
    assert fila.exitoso is True
    assert fila.motivo_rechazo is None
    assert fila.fecha is not None


def test_login_exitoso_de_director_registra_fila_exitosa(
    client_real_auth, db_session, monkeypatch
):
    db_session.add(DirectorPrograma(email="director@uneatlantico.es"))
    db_session.commit()
    monkeypatch.setattr(oauth, "google", _FakeGoogleClient("director@uneatlantico.es"))

    resp = client_real_auth.get("/auth/callback", follow_redirects=False)

    assert resp.status_code in (302, 307)
    [fila] = _registros(db_session)
    assert (fila.email, fila.exitoso, fila.motivo_rechazo) == (
        "director@uneatlantico.es",
        True,
        None,
    )


def test_rechazo_por_dominio_registra_fuera_de_dominio(
    client_real_auth, db_session, monkeypatch
):
    db_session.add(Profesor(email="profesor@gmail.com"))
    db_session.commit()
    monkeypatch.setenv("GOOGLE_HD", "uneatlantico.es")
    get_settings.cache_clear()
    monkeypatch.setattr(
        oauth, "google", _FakeGoogleClient("profesor@gmail.com", hd="gmail.com")
    )

    resp = client_real_auth.get("/auth/callback", follow_redirects=False)

    assert resp.status_code == 403
    assert get_settings().session_cookie_name not in resp.cookies
    [fila] = _registros(db_session)
    assert (fila.email, fila.exitoso, fila.motivo_rechazo) == (
        "profesor@gmail.com",
        False,
        "fuera_de_dominio",
    )


def test_rechazo_por_cuenta_no_catalogada_registra_no_autorizado(
    client_real_auth, db_session, monkeypatch
):
    monkeypatch.setattr(
        oauth, "google", _FakeGoogleClient("desconocido@uneatlantico.es")
    )

    resp = client_real_auth.get("/auth/callback", follow_redirects=False)

    assert resp.status_code == 403
    [fila] = _registros(db_session)
    assert (fila.email, fila.exitoso, fila.motivo_rechazo) == (
        "desconocido@uneatlantico.es",
        False,
        "no_autorizado",
    )


@pytest.mark.parametrize(
    "email,hd,admins,gdominio",
    [
        ("admin@uneatlantico.es", None, "admin@uneatlantico.es", ""),  # éxito
        ("profesor@uneatlantico.es", None, "admin@uneatlantico.es", ""),  # no en whitelist
        ("admin@gmail.com", "gmail.com", "admin@gmail.com", "uneatlantico.es"),  # dominio
    ],
    ids=["exito", "no_autorizado", "fuera_de_dominio"],
)
def test_login_de_admin_no_escribe_en_el_registro(
    client_real_auth, db_session, monkeypatch, email, hd, admins, gdominio
):
    monkeypatch.setenv("ADMIN_EMAILS", admins)
    monkeypatch.setenv("GOOGLE_HD", gdominio)
    get_settings.cache_clear()
    monkeypatch.setattr(oauth, "google", _FakeGoogleClient(email, hd=hd))

    client_real_auth.get("/auth/admin/callback", follow_redirects=False)

    assert _registros(db_session) == []


# --- lectura: GET /api/v1/registro-accesos ---------------------------------


def test_consulta_sin_cookie_401(client_real_auth):
    resp = client_real_auth.get("/api/v1/registro-accesos")
    assert resp.status_code == 401


def test_consulta_con_sesion_de_profesor_403(client_real_auth):
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.get("/api/v1/registro-accesos")
    assert resp.status_code == 403


def test_consulta_con_sesion_de_admin_200(client_real_auth):
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_admin_session_token("admin@uneatlantico.es"),
    )
    resp = client_real_auth.get("/api/v1/registro-accesos")
    assert resp.status_code == 200
    assert resp.json() == []


def test_consulta_devuelve_como_maximo_25_en_orden_desc(client, db_session):
    base = datetime(2026, 11, 1, 9, 0, tzinfo=UTC)
    for i in range(30):
        db_session.add(
            RegistroAcceso(
                email=f"p{i}@uneatlantico.es",
                exitoso=True,
                fecha=base + timedelta(minutes=i),
            )
        )
    db_session.commit()

    resp = client.get("/api/v1/registro-accesos")

    assert resp.status_code == 200
    datos = resp.json()
    assert len(datos) == 25
    assert [d["email"] for d in datos] == [
        f"p{i}@uneatlantico.es" for i in range(29, 4, -1)
    ]


def test_consulta_desempata_misma_fecha_por_id_desc(client, db_session):
    fecha = datetime(2026, 11, 1, 9, 0, tzinfo=UTC)
    for email in ("a@uneatlantico.es", "b@uneatlantico.es"):
        db_session.add(RegistroAcceso(email=email, exitoso=True, fecha=fecha))
    db_session.commit()

    datos = client.get("/api/v1/registro-accesos").json()

    assert [d["email"] for d in datos] == ["b@uneatlantico.es", "a@uneatlantico.es"]


def test_consulta_resuelve_nombre_por_email_y_cae_al_email_crudo(client, db_session):
    db_session.add(Profesor(email="ana@uneatlantico.es", nombre="Ana Pérez"))
    db_session.add(DirectorPrograma(email="dir@uneatlantico.es"))
    db_session.add(Profesor(email="sinnombre@uneatlantico.es"))
    base = datetime(2026, 11, 1, 9, 0, tzinfo=UTC)
    filas = [
        ("ana@uneatlantico.es", True, None),
        ("dir@uneatlantico.es", True, None),
        ("sinnombre@uneatlantico.es", True, None),
        ("intruso@uneatlantico.es", False, "no_autorizado"),
        ("alguien@gmail.com", False, "fuera_de_dominio"),
    ]
    for i, (email, exitoso, motivo) in enumerate(filas):
        db_session.add(
            RegistroAcceso(
                email=email,
                exitoso=exitoso,
                motivo_rechazo=motivo,
                fecha=base + timedelta(minutes=i),
            )
        )
    db_session.commit()

    datos = client.get("/api/v1/registro-accesos").json()

    assert [(d["nombre"], d["exitoso"], d["motivo_rechazo"]) for d in datos] == [
        ("alguien@gmail.com", False, "fuera_de_dominio"),
        ("intruso@uneatlantico.es", False, "no_autorizado"),
        ("sinnombre@uneatlantico.es", True, None),
        ("dir@uneatlantico.es", True, None),
        ("Ana Pérez", True, None),
    ]

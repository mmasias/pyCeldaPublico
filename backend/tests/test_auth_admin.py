import pytest

from app.core.auth import create_admin_session_token, create_session_token, oauth
from app.core.config import get_settings

SESSION_SECRET = "test-session-secret-key-not-real"


@pytest.fixture(autouse=True)
def _session_secret(monkeypatch):
    monkeypatch.setenv("SESSION_SECRET_KEY", SESSION_SECRET)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


class _FakeGoogleClient:
    def __init__(self, email: str, hd: str | None = None):
        self._email = email
        self._hd = hd

    async def authorize_access_token(self, request):
        return {"userinfo": {"email": self._email, "hd": self._hd}}


# --- require_admin() -- bloqueo real, no solo test feliz --------------------


def test_universidades_sin_cookie_401(client_real_auth):
    resp = client_real_auth.get("/api/v1/universidades")
    assert resp.status_code == 401


def test_universidades_cookie_invalida_401(client_real_auth):
    client_real_auth.cookies.set(
        get_settings().session_cookie_name, "esto-no-es-un-jwt-valido"
    )
    resp = client_real_auth.get("/api/v1/universidades")
    assert resp.status_code == 401


def test_universidades_con_sesion_de_profesor_403(client_real_auth):
    """El <<choice>> real: un token válido pero sin claim rol=admin (el
    mismo tipo de token que emite /auth/callback para Profesor/DirectorGrado)
    tiene que ser rechazado -- no basta con "hay cookie", tiene que ser
    específicamente una sesión de Admin. Ejercita el guard bloqueando a un
    no-Admin de verdad, no solo comprobando que la dependencia existe."""
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.get("/api/v1/universidades")
    assert resp.status_code == 403


def test_crear_universidad_con_sesion_de_profesor_403(client_real_auth):
    """Mismo bloqueo en un endpoint de escritura -- el que más importa dado
    el historial IDOR del proyecto (#86/#96)."""
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.post("/api/v1/universidades", json={"nombre": "x"})
    assert resp.status_code == 403


def test_universidades_con_sesion_de_admin_pasa(client_real_auth):
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_admin_session_token("admin@uneatlantico.es"),
    )
    resp = client_real_auth.get("/api/v1/universidades")
    assert resp.status_code == 200


def test_eliminar_facultad_con_sesion_de_profesor_403(client_real_auth):
    """Mismo bloqueo en el endpoint de borrado."""
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.delete("/api/v1/facultades/1")
    assert resp.status_code == 403


def test_eliminar_asignatura_con_sesion_de_profesor_403(client_real_auth):
    """Mismo bloqueo real en eliminarAsignatura() -- endpoint de escritura,
    aunque el borrado sea lógico (Extinguido), no físico."""
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.delete("/api/v1/asignaturas/1")
    assert resp.status_code == 403


def test_crear_grado_con_sesion_de_profesor_403(client_real_auth):
    """Mismo bloqueo real en crearGrado() -- endpoint de escritura del
    namespace /api/v1/admin/facultades/{facultad_id}/grados, separado del
    /api/v1/grados de DirectorGrado precisamente para no mezclar los dos
    guards. La Facultad 1 no necesita existir: require_admin resuelve
    antes de que el handler toque la BD."""
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.post(
        "/api/v1/admin/facultades/1/grados", json={"codigo": "GII", "nombre": "x"}
    )
    assert resp.status_code == 403


def test_eliminar_grado_con_sesion_de_profesor_403(client_real_auth):
    """Mismo bloqueo real en eliminarGrado() -- endpoint de borrado
    (lógico, Extinguido), mismo guard que el resto de escritura."""
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.delete("/api/v1/admin/grados/1")
    assert resp.status_code == 403


# --- lote Materia/AsignaturaGrado: 401 sin cookie y 403 con sesión de
# profesor para cada uno de los 7 endpoints Admin nuevos. Los identificadores
# no necesitan existir: require_admin resuelve antes de que el handler toque
# la BD (mismo criterio que los tests de Grado de arriba).

_ENDPOINTS_LOTE_MATERIA = [
    ("GET", "/api/v1/admin/grados/1/materias", None),
    ("POST", "/api/v1/admin/grados/1/materias", {"nombre": "x"}),
    ("GET", "/api/v1/admin/materias/1", None),
    ("PUT", "/api/v1/admin/materias/1", {"nombre": "x"}),
    ("GET", "/api/v1/admin/grados/1/asignaturas-grado", None),
    (
        "POST",
        "/api/v1/admin/grados/1/asignaturas-grado",
        {
            "materia_id": 1,
            "asignatura_id": 1,
            "curso": 1,
            "caracter": "Básica",
            "idioma": "Español",
            "semestre_default": 1,
        },
    ),
    ("DELETE", "/api/v1/admin/asignaturas-grado/1", None),
]


@pytest.mark.parametrize(
    "metodo,ruta,cuerpo", _ENDPOINTS_LOTE_MATERIA, ids=[r for _, r, _ in _ENDPOINTS_LOTE_MATERIA]
)
def test_lote_materia_sin_cookie_401(client_real_auth, metodo, ruta, cuerpo):
    resp = client_real_auth.request(metodo, ruta, json=cuerpo)
    assert resp.status_code == 401


@pytest.mark.parametrize(
    "metodo,ruta,cuerpo", _ENDPOINTS_LOTE_MATERIA, ids=[r for _, r, _ in _ENDPOINTS_LOTE_MATERIA]
)
def test_lote_materia_con_sesion_de_profesor_403(
    client_real_auth, metodo, ruta, cuerpo
):
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_session_token("profesor@uneatlantico.es"),
    )
    resp = client_real_auth.request(metodo, ruta, json=cuerpo)
    assert resp.status_code == 403


def test_crear_asignatura_con_sesion_de_admin_pasa(client_real_auth):
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        create_admin_session_token("admin@uneatlantico.es"),
    )
    resp = client_real_auth.post(
        "/api/v1/asignaturas", json={"codigo": "IYA003", "nombre": "Programación I"}
    )
    assert resp.status_code == 201


# --- /auth/admin/login + /auth/admin/callback -------------------------------


def test_callback_admin_rechaza_email_fuera_de_whitelist(
    client_real_auth, monkeypatch
):
    monkeypatch.setenv("ADMIN_EMAILS", "admin@uneatlantico.es")
    get_settings.cache_clear()
    monkeypatch.setattr(oauth, "google", _FakeGoogleClient("profesor@uneatlantico.es"))

    resp = client_real_auth.get("/auth/admin/callback", follow_redirects=False)
    assert resp.status_code == 403


def test_callback_admin_acepta_email_en_whitelist_y_emite_sesion_admin(
    client_real_auth, monkeypatch
):
    monkeypatch.setenv("ADMIN_EMAILS", "admin@uneatlantico.es")
    get_settings.cache_clear()
    monkeypatch.setattr(oauth, "google", _FakeGoogleClient("admin@uneatlantico.es"))

    resp = client_real_auth.get("/auth/admin/callback", follow_redirects=False)
    assert resp.status_code in (302, 307)
    assert resp.headers["location"].endswith("/panel-administracion")
    assert get_settings().session_cookie_name in resp.cookies

    # la cookie emitida es una sesión de Admin real -- ejercita el flujo
    # completo, no solo que /auth/admin/callback devuelva 302
    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        resp.cookies[get_settings().session_cookie_name],
    )
    resp_admin = client_real_auth.get("/api/v1/universidades")
    assert resp_admin.status_code == 200


def test_callback_admin_rechaza_dominio_fuera_de_hd(client_real_auth, monkeypatch):
    monkeypatch.setenv("ADMIN_EMAILS", "admin@gmail.com")
    monkeypatch.setenv("GOOGLE_HD", "uneatlantico.es")
    get_settings.cache_clear()
    monkeypatch.setattr(
        oauth, "google", _FakeGoogleClient("admin@gmail.com", hd="gmail.com")
    )

    resp = client_real_auth.get("/auth/admin/callback", follow_redirects=False)
    assert resp.status_code == 403


def test_callback_normal_no_emite_sesion_valida_para_endpoints_de_admin(
    client_real_auth, db_session, monkeypatch
):
    """Aislamiento entre los dos flujos: la cookie que emite /auth/callback
    (Profesor/DirectorGrado) no sirve para require_admin, ni siquiera si el
    email también está en ADMIN_EMAILS -- son dos caminos de código
    físicamente separados, la cookie de uno no autoriza en el otro."""
    from app.models.profesor import Profesor

    db_session.add(Profesor(email="profesor@uneatlantico.es"))
    db_session.commit()
    monkeypatch.setenv("ADMIN_EMAILS", "profesor@uneatlantico.es")
    get_settings.cache_clear()
    monkeypatch.setattr(oauth, "google", _FakeGoogleClient("profesor@uneatlantico.es"))

    resp = client_real_auth.get("/auth/callback", follow_redirects=False)
    assert resp.status_code in (302, 307)

    client_real_auth.cookies.set(
        get_settings().session_cookie_name,
        resp.cookies[get_settings().session_cookie_name],
    )
    resp_admin = client_real_auth.get("/api/v1/universidades")
    assert resp_admin.status_code == 403

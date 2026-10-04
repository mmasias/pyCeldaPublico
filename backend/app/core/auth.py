"""Login real con Google OAuth2/OIDC -- discussion #62.

Sin auto-registro: el email de la cuenta de Google tiene que coincidir con
un Profesor o DirectorPrograma ya existente en la base de datos (creados por
Admin vía crearProfesor()/definirDirectorPrograma(), fuera de esta rebanada) --
si no hay coincidencia, el login se rechaza. Restringido al dominio
institucional de Workspace (parámetro `hd` de Google OAuth).

Sesión vía JWT en cookie httpOnly, firmado con SESSION_SECRET_KEY -- sin
almacén de sesión en servidor, coherente con el perfil de despliegue (VPS
propio + Tailscale, un solo mantenedor, mínima carga operativa).
"""

import time

from authlib.integrations.starlette_client import OAuth
from fastapi import Depends, HTTPException, Request
from joserfc import jwt
from joserfc.errors import JoseError
from joserfc.jwk import OctKey
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.repositories.director_programa import DirectorProgramaRepository
from app.repositories.programa import ProgramaRepository
from app.repositories.profesor import ProfesorRepository

oauth = OAuth()
oauth.register(
    name="google",
    client_id=get_settings().google_client_id,
    client_secret=get_settings().google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

_CLAIMS_REGISTRY = jwt.JWTClaimsRegistry(exp={"essential": True})


def _session_key() -> OctKey:
    return OctKey.import_key(get_settings().session_secret_key)


def create_session_token(email: str) -> str:
    settings = get_settings()
    payload = {"email": email, "exp": int(time.time()) + settings.session_max_age_seconds}
    return jwt.encode({"alg": "HS256"}, payload, _session_key())


def create_admin_session_token(email: str) -> str:
    """Igual que create_session_token, pero con el claim `rol=admin` explícito
    -- no hay tabla Admin que re-consultar en cada petición (ver
    RUP/03-diseño/casos-uso/iniciarSesion/README.md), así que el rol se fija
    en el propio token en el momento del login."""
    settings = get_settings()
    payload = {
        "email": email,
        "rol": "admin",
        "exp": int(time.time()) + settings.session_max_age_seconds,
    }
    return jwt.encode({"alg": "HS256"}, payload, _session_key())


def decode_session_token(token: str) -> str | None:
    try:
        decoded = jwt.decode(token, _session_key())
        _CLAIMS_REGISTRY.validate(decoded.claims)
    except JoseError:
        return None
    return decoded.claims.get("email")


def _email_from_cookie(request: Request) -> str:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if token is None:
        raise HTTPException(status_code=401, detail="Sin sesión -- inicia sesión con Google")
    email = decode_session_token(token)
    if email is None:
        raise HTTPException(status_code=401, detail="Sesión inválida o caducada")
    return email


def get_current_profesor_id(request: Request, db: Session = Depends(get_db)) -> int:
    email = _email_from_cookie(request)
    profesor = ProfesorRepository(db).obtener_por_email(email)
    if profesor is None:
        raise HTTPException(status_code=403, detail="Cuenta sin Profesor asociado")
    return profesor.id


def get_current_director_programa_id(request: Request, db: Session = Depends(get_db)) -> int:
    email = _email_from_cookie(request)
    director = DirectorProgramaRepository(db).obtener_por_email(email)
    if director is None:
        raise HTTPException(status_code=403, detail="Cuenta sin DirectorPrograma asociado")
    return director.id


def get_current_profesor_id_opcional(
    request: Request, db: Session = Depends(get_db)
) -> int | None:
    """Como get_current_profesor_id, pero sin exigir el rol -- para
    endpoints compartidos con DirectorPrograma (abrirGuia()) donde un email
    puede no tener Profesor asociado sin que eso sea un 403."""
    email = _email_from_cookie(request)
    profesor = ProfesorRepository(db).obtener_por_email(email)
    return profesor.id if profesor is not None else None


def get_current_director_programa_id_opcional(
    request: Request, db: Session = Depends(get_db)
) -> int | None:
    """Como get_current_director_programa_id, pero sin exigir el rol -- ver
    get_current_profesor_id_opcional."""
    email = _email_from_cookie(request)
    director = DirectorProgramaRepository(db).obtener_por_email(email)
    return director.id if director is not None else None


def _decoded_admin_claims(request: Request) -> dict:
    """Decodifica y valida el JWT de sesión, sin comprobar el rol todavía --
    helper compartido entre require_admin() y su variante opcional. Los
    mismos dos 401 que ya lanzaba require_admin() antes de mirar el claim
    `rol`."""
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if token is None:
        raise HTTPException(status_code=401, detail="Sin sesión -- inicia sesión con Google")
    try:
        decoded = jwt.decode(token, _session_key())
        _CLAIMS_REGISTRY.validate(decoded.claims)
    except JoseError:
        raise HTTPException(status_code=401, detail="Sesión inválida o caducada")
    return decoded.claims


def require_admin(request: Request) -> str:
    """Autorización de Admin, sin pasar por get_current_rol() -- ese
    dependency solo resuelve Profesor/DirectorPrograma. Admin no tiene tabla
    real (ver AdminRepository, sin uso, en Análisis de iniciarSesion()); el
    rol viene fijado en el propio token por create_admin_session_token(),
    emitido solo por /auth/admin/callback tras validar la whitelist
    ADMIN_EMAILS. Devuelve el email de la cuenta autorizada."""
    claims = _decoded_admin_claims(request)
    if claims.get("rol") != "admin":
        raise HTTPException(status_code=403, detail="Cuenta sin rol de Admin")
    return claims["email"]


def get_current_admin_email_opcional(request: Request) -> str | None:
    """Como require_admin(), pero sin exigir rol=admin -- devuelve None en
    vez de 403 cuando la sesión es válida pero de otro rol (Profesor o
    DirectorPrograma). Compone con _tiene_acceso_a_guia() en endpoints
    compartidos entre los tres actores (descargarGuiaPDF(), discussion
    #224, cierre de issue #220) -- mismo criterio que
    get_current_profesor_id_opcional/get_current_director_programa_id_opcional."""
    claims = _decoded_admin_claims(request)
    return claims["email"] if claims.get("rol") == "admin" else None


def get_current_rol(request: Request, db: Session = Depends(get_db)) -> dict[str, str | bool]:
    """Resuelve el rol de la sesión para el enrutado post-login del frontend
    y para pintar las secciones de abrirInicio() -- discussion #274.

    Rama `admin` (issue #314): el claim `rol=admin` del token, fijado por
    create_admin_session_token() en el login de Admin, corta aquí sin
    consultar Profesor/DirectorPrograma -- mismo criterio que require_admin()/
    get_current_admin_email_opcional(), unas líneas más arriba. Antes de
    este fix, un Admin puro (sin fila en ninguna de las dos tablas) caía al 403 de abajo y RequireSession lo
    expulsaba a "/"; un Admin que además tuviera fila Profesor/DirectorPrograma
    resolvía en silencio como `profesor`/`director_programa`, nunca `admin` --
    efecto secundario deliberado de este fix: ahora siempre resuelve `admin`.

    Un email puede resolver a DirectorPrograma y/o Profesor (`DirectorPrograma --|>
    Profesor` en el modelo de dominio, roles independientes no exclusivos). El
    rol `director_programa` requiere dirigir >= 1 Programa (fila en `directores_programa`
    Y pertenencia a la colección `directores` de algún Programa): una fila
    huérfana de ex-director (tras quitarDirectorPrograma(), que nunca la borra)
    cae a `profesor`, y aun sin impartir sigue resolviendo con éxito -- una
    cuenta autenticada y reconocida por el catálogo NUNCA se expulsa con 403,
    la capacidad ausente la absorbe abrirInicio() como sección vacía.

    `es_profesor` y `dirige_programas` son las dos señales independientes que
    abrirInicio() consume para decidir qué secciones muestra. `es_tambien_
    profesor` se conserva para las pantallas de deep link (/programas,
    /mis-asignaturas-programa)."""
    claims = _decoded_admin_claims(request)
    if claims.get("rol") == "admin":
        return {
            "email": claims["email"],
            "rol": "admin",
            "es_tambien_profesor": False,
            "es_profesor": False,
            "dirige_programas": False,
        }

    email = claims["email"]
    es_profesor = ProfesorRepository(db).obtener_por_email(email) is not None
    director = DirectorProgramaRepository(db).obtener_por_email(email)
    dirige_programas = (
        director is not None
        and ProgramaRepository(db).contar_dirigidos_por(director.id) > 0
    )

    if dirige_programas:
        rol = "director_programa"
    elif es_profesor or director is not None:
        rol = "profesor"
    else:
        raise HTTPException(status_code=403, detail="Cuenta sin rol asociado")

    return {
        "email": email,
        "rol": rol,
        "es_tambien_profesor": rol == "director_programa" and es_profesor,
        "es_profesor": es_profesor,
        "dirige_programas": dirige_programas,
    }

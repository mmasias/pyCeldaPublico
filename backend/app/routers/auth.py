from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.auth import create_admin_session_token, create_session_token, get_current_rol, oauth
from app.core.config import get_settings
from app.core.database import get_db
from app.repositories.director_programa import DirectorProgramaRepository
from app.repositories.profesor import ProfesorRepository

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def me(sesion: dict[str, str | bool] = Depends(get_current_rol)) -> dict[str, str | bool]:
    return sesion


@router.get("/login")
async def login(request: Request):
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=500, detail="Login con Google sin configurar")
    return await oauth.google.authorize_redirect(
        request, settings.oauth_redirect_uri, hd=settings.google_hd or None
    )


@router.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo") or await oauth.google.userinfo(token=token)
    email = userinfo["email"]

    if settings.google_hd and userinfo.get("hd") != settings.google_hd:
        raise HTTPException(
            status_code=403, detail="Cuenta fuera del dominio institucional"
        )

    conocido = (
        ProfesorRepository(db).obtener_por_email(email) is not None
        or DirectorProgramaRepository(db).obtener_por_email(email) is not None
    )
    if not conocido:
        raise HTTPException(
            status_code=403, detail="Cuenta no autorizada -- sin auto-registro"
        )

    response = RedirectResponse(url=settings.frontend_url)
    response.set_cookie(
        settings.session_cookie_name,
        create_session_token(email),
        httponly=True,
        max_age=settings.session_max_age_seconds,
        samesite="lax",
        secure=not settings.oauth_redirect_uri.startswith("http://localhost"),
    )
    return response


@router.post("/logout")
def logout():
    settings = get_settings()
    response = RedirectResponse(url=settings.frontend_url)
    response.delete_cookie(settings.session_cookie_name)
    return response


@router.get("/admin/login")
async def login_admin(request: Request):
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=500, detail="Login con Google sin configurar")
    return await oauth.google.authorize_redirect(
        request, settings.oauth_admin_redirect_uri, hd=settings.google_hd or None
    )


@router.get("/admin/callback")
async def callback_admin(request: Request):
    settings = get_settings()
    token = await oauth.google.authorize_access_token(request)
    userinfo = token.get("userinfo") or await oauth.google.userinfo(token=token)
    email = userinfo["email"]

    if settings.google_hd and userinfo.get("hd") != settings.google_hd:
        raise HTTPException(
            status_code=403, detail="Cuenta fuera del dominio institucional"
        )

    if email not in settings.admin_emails:
        raise HTTPException(
            status_code=403, detail="Cuenta no autorizada -- sin auto-registro"
        )

    response = RedirectResponse(url=f"{settings.frontend_url}/panel-administracion")
    response.set_cookie(
        settings.session_cookie_name,
        create_admin_session_token(email),
        httponly=True,
        max_age=settings.session_max_age_seconds,
        samesite="lax",
        secure=not settings.oauth_redirect_uri.startswith("http://localhost"),
    )
    return response

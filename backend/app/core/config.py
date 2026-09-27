import os
from functools import lru_cache

from pydantic import BaseModel, Field, model_validator


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


class Settings(BaseModel):
    google_client_id: str = Field(default_factory=lambda: _env("GOOGLE_CLIENT_ID"))
    google_client_secret: str = Field(default_factory=lambda: _env("GOOGLE_CLIENT_SECRET"))
    google_hd: str = Field(default_factory=lambda: _env("GOOGLE_HD"))
    session_secret_key: str = Field(default_factory=lambda: _env("SESSION_SECRET_KEY"))
    session_cookie_name: str = "pycelda_session"
    session_max_age_seconds: int = 60 * 60 * 12  # 12h
    oauth_redirect_uri: str = Field(
        default_factory=lambda: _env(
            "OAUTH_REDIRECT_URI", "http://localhost:8000/auth/callback"
        )
    )
    frontend_url: str = Field(
        default_factory=lambda: _env("FRONTEND_URL", "http://localhost:5173")
    )
    oauth_admin_redirect_uri: str = Field(
        default_factory=lambda: _env(
            "OAUTH_ADMIN_REDIRECT_URI", "http://localhost:8000/auth/admin/callback"
        )
    )
    admin_emails: list[str] = Field(
        default_factory=lambda: [
            e.strip() for e in _env("ADMIN_EMAILS").split(",") if e.strip()
        ]
    )

    @model_validator(mode="after")
    def _validar_secretos_en_produccion(self) -> "Settings":
        if self.oauth_redirect_uri.startswith("http://localhost"):
            return self
        faltantes = [
            nombre
            for nombre, valor in [
                ("SESSION_SECRET_KEY", self.session_secret_key),
                ("GOOGLE_CLIENT_ID", self.google_client_id),
                ("GOOGLE_CLIENT_SECRET", self.google_client_secret),
            ]
            if not valor
        ]
        if faltantes:
            raise RuntimeError(
                "Configuración inválida para producción -- faltan variables de entorno "
                f"obligatorias: {', '.join(faltantes)}"
            )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()

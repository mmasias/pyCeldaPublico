"""obtenerVersion() -- issue #628. Versión del esquema de BD (`PRAGMA
user_version`), sin auth: se consulta desde las pantallas de login, antes de
iniciar sesión, igual que `__APP_VERSION__`."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.backups import obtener_version_esquema
from app.core.database import get_db
from app.schemas.version import VersionResponse

router = APIRouter(prefix="/api/v1", tags=["version"])


@router.get("/version", response_model=VersionResponse)
def obtener_version(db: Session = Depends(get_db)) -> VersionResponse:
    return VersionResponse(esquema_version=obtener_version_esquema(db))

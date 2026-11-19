"""obtenerVersion() -- issue #628. Versión del esquema de BD (`PRAGMA
user_version`), sin auth: se consulta desde las pantallas de login, antes de
iniciar sesión, igual que `__APP_VERSION__`.

El campo `version` se añade para que el frontal del ecosistema pueda mostrar
versión + esquema de cada servicio sin casos especiales (contrato de
mmasias/pyPULSO#22): se lee del paquete instalado, mismo número que
`pyproject.toml` y que `__APP_VERSION__` del frontend (ambos se bumpean a la
vez, ver DEPLOY.md)."""

from importlib.metadata import version as version_del_paquete

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.backups import obtener_version_esquema
from app.core.database import get_db
from app.schemas.version import VersionResponse

router = APIRouter(prefix="/api/v1", tags=["version"])


@router.get("/version", response_model=VersionResponse)
def obtener_version(db: Session = Depends(get_db)) -> VersionResponse:
    return VersionResponse(
        version=version_del_paquete("pycelda-backend"),
        esquema_version=obtener_version_esquema(db),
    )

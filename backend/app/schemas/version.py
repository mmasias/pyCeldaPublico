from pydantic import BaseModel


class VersionResponse(BaseModel):
    esquema_version: int

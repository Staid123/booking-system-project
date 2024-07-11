from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

BASE_DIR = Path(__file__)


private_key_path: Path = BASE_DIR.parent / "certs" / "jwt-private.pem"
public_key_path: Path = BASE_DIR.parent / "certs" / "jwt-public.pem"


class PostgresDatabaseURL(BaseModel):
    url: str


class AuthJWT(BaseModel):
    private_key: str = private_key_path.read_text()
    public_key: str = public_key_path.read_text()
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    auth_jwt: AuthJWT = AuthJWT()
    db: PostgresDatabaseURL


settings: Settings = Settings()
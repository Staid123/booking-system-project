from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

REVIEW_SERVICE_DIR = Path(__file__).parent


private_key_path: Path = REVIEW_SERVICE_DIR / "certs" / "jwt-private.pem"
public_key_path: Path = REVIEW_SERVICE_DIR / "certs" / "jwt-public.pem"


class PostgresDatabaseURL(BaseModel):
    url: str
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWT(BaseModel):
    private_key: str = private_key_path.read_text()
    public_key: str = public_key_path.read_text()
    algorithm: str = "RS256"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    auth_jwt: AuthJWT = AuthJWT()
    db: PostgresDatabaseURL


settings: Settings = Settings()
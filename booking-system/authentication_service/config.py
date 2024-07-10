from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class PostgresDatabaseSettings(BaseModel):
    host: str
    port: int
    name: str
    user: str
    password: str
    url: str

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWT(BaseModel):
    private_key: Optional[str] = None
    public_key: Optional[str] = None
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

    @staticmethod
    def read_key(file_path: Path) -> str:
        with open(file_path, 'r') as file:
            return file.read()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.private_key is None and 'private_key_path' in kwargs:
            self.private_key = self.read_key(kwargs['private_key_path'])
        if self.public_key is None and 'public_key_path' in kwargs:
            self.public_key = self.read_key(kwargs['public_key_path'])

        
        
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )
    auth_jwt: AuthJWT = AuthJWT(
        private_key_path="certs" / "jwt-private.pem",
        public_key_path="certs" / "jwt-public.pem"
    )
    db: PostgresDatabaseSettings


settings = Settings()
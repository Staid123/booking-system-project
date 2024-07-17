from pydantic import BaseModel, ConfigDict


class TokenPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True, strict=True)
    
    type: str
    sub: str
    exp: int
    username: str
    email: str
    admin: bool
    jti: bytes
    iat: int
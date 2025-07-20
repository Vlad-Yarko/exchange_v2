from typing import Optional
from datetime import datetime, timedelta, UTC

from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidSubjectError

from src.config import settings


class Token:
    algorithm = 'RS256'
    
    def create_token(self, payload: dict) -> str:
        token = encode(
            payload=payload,
            key=settings.PRIVATE_KEY,
            algorithm=self.algorithm
        )
        return token

    def decode_token(self, token: str) -> dict:
        decoded_token = decode(
            jwt=token,
            key=settings.PUBLIC_KEY,
            algorithms=[self.algorithm]
        )
        return decoded_token

    def create_access_token(self, id: str) -> str:
        now = datetime.now(UTC)
        iat = int(now.timestamp())
        exp = int((now + timedelta(minutes=15)).timestamp())
        payload = {
            'sub': id,
            'iat': iat,
            'exp': exp
        }
        token = self.create_token(payload)
        return token

    def create_refresh_token(self, id: str, expiration: Optional[int] = None) -> str:
        now = datetime.now(UTC)
        iat = int(now.timestamp())
        exp = int((now + timedelta(days=30)).timestamp()) if not expiration else expiration
        payload = {
            'sub': id,
            'iat': iat,
            'exp': exp
        }
        token = self.create_token(payload)
        return token

    def validate_token(self, token: Optional[str]) -> Optional[dict]:
        if not token:
            return None
        try:
            payload = self.decode_token(token)
        except (ExpiredSignatureError, DecodeError, InvalidSubjectError):
            return None
        return payload


token_worker = Token()

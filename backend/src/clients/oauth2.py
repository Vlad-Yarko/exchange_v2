from typing import Optional

from src.utils.client import JSONClient
from src.constants.oauth2 import GOOGLE_TOKEN_BASE_URL, GOOGLE_TOKEN_ENDPOINT_URl, GOOGLE_REDIRECT_URI
from src.config import settings


class Oauth2Client(JSONClient):
    def __init__(
        self
    ):
        super().__init__(
            base_url=GOOGLE_TOKEN_BASE_URL
        )
        
    async def get_google_data(self, code: str) -> Optional[dict]:
        self.endpoint = GOOGLE_TOKEN_ENDPOINT_URl
        self.payload = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "code": code
        }
        data = await self.post()
        return data

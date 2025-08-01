import urllib.parse

from src.constants.oauth2 import GOOGLE_URL_REDIRECT, GOOGLE_REDIRECT_URI
from src.config import settings


class Oauth2:
    def __init__(self):
        pass
    
    def google_url_redirect(self) -> str:
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": " ".join([
                "openid",
                "profile",
                "email"
            ]),
            # "access_type": "offline"
            # "state": ""
        }
        str_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return f"{GOOGLE_URL_REDIRECT}?{str_params}"
    
    
oauth2 = Oauth2()

from typing import Optional

from src.utils.client import JSONClient
from src.enums.currency import URLEnum
from src.config import settings


class CurrencyClient(JSONClient):
    def __init__(
        self
    ):
        super().__init__(
            base_url=URLEnum.BASE_URL.value
        )
        
    async def get_symbol_price(self, symbol1: str, symbol2: str) -> Optional[dict]:
        self.endpoint = URLEnum.PRICE_ENDPOINT.value
        self.params = {
            'access_key': settings.EXCHANGERATE_API_KEY,
            'source': symbol1,
            'currencies': symbol2
        }
        data = await self.get()
        return data
        

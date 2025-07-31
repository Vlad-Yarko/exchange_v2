from typing import Optional

from src.utils.client import JSONClient
from src.enums.crypto import URLEnum


class CryptoClient(JSONClient):
    def __init__(
        self
    ):
        super().__init__(
            base_url=URLEnum.BASE_URL.value
        )
        
    async def get_symbol_price(self, symbol: str) -> Optional[dict]:
        self.endpoint = URLEnum.PRICE_ENDPOINT.value
        self.params = {
            "symbol": symbol
        }
        data = await self.get()
        return data

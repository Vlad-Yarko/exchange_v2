from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository


class CurrencyService(Service):
    def __init__(
        self,
        session: AsyncSession,
        currency_repo: Repository
    ):
        super().__init__()
        self.session = session
        self.currency_repo = currency_repo
        self.single_repo = currency_repo

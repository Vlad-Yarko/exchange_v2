from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.service import Service
from src.utils.repository import Repository


class CryptoService(Service):
    def __init__(
        self,
        session: AsyncSession,
        crypto_repo: Repository
    ):
        super().__init__()
        self.session = session
        self.crypto_repo = crypto_repo
        self.single_repo = crypto_repo

from src.utils.repository import SQLAlchemyRepository
from src.models import CryptoSubscribe


class CryptoSubscribeRepository(SQLAlchemyRepository):
    model = CryptoSubscribe

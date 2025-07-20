from src.utils.repository import SQLAlchemyRepository
from src.models import Crypto


class CryptoRepository(SQLAlchemyRepository):
    model = Crypto

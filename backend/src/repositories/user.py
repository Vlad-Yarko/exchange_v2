from src.utils.repository import SQLAlchemyRepository
from src.models import User


class UserRepository(SQLAlchemyRepository):
    model = User
